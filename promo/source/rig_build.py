"""Cut the front-view mascot into rig layers (ears, head, body, waving arm, eye patches).
All layers keep the full canvas size so they overlay 1:1; pivots are in canvas pixels."""
import sys, json, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
B = sys.argv[1]
im = np.asarray(Image.open(f"{B}/assets/mascot-front.png").convert('RGBA')).copy()
H, W = im.shape[:2]; A = im[..., 3] > 8
ys, xs = np.mgrid[0:H, 0:W]

def below_poly(pts):
    """mask of pixels below a polyline y(x) (linear interpolation, clamped)"""
    px = np.array([p[0] for p in pts], float); py = np.array([p[1] for p in pts], float)
    yl = np.interp(np.arange(W), px, py)
    return ys > yl[None, :]

HAT_TOP = [(0, 640), (40, 600), (120, 520), (240, 462), (400, 432), (520, 424), (660, 436), (800, 478), (900, 540), (1000, 650), (1039, 700)]
HEAD_BOT = [(0, 1330), (120, 1322), (200, 1312), (300, 1316), (420, 1322), (520, 1322), (640, 1316), (760, 1306), (860, 1300), (960, 1310), (1039, 1330)]
above_hat = ~below_poly(HAT_TOP)
ears = A & above_hat
head = A & ~above_hat & ~below_poly(HEAD_BOT)
body = A & below_poly(HEAD_BOT)
R, G, Bc = [im[..., i].astype(int) for i in range(3)]
pink = (R - G) > 55
ARM_POLY = [(790, 1366), (850, 1392), (900, 1446), (942, 1500), (972, 1560), (988, 1620), (978, 1672), (952, 1704), (915, 1720), (885, 1718), (852, 1698), (818, 1652), (793, 1592), (776, 1540), (762, 1480), (752, 1420), (750, 1378)]
pm = np.zeros((H, W), np.uint8); cv2.fillPoly(pm, [np.array(ARM_POLY, np.int32)], 1)
strongpink = ((R - G) > 85) & (R > 170)
arm = body & (pm > 0)
# keep only the big arm blob
n, lab = cv2.connectedComponents(arm.astype(np.uint8))
if n > 2:
    sizes = [(lab == i).sum() for i in range(1, n)]; arm = lab == (1 + int(np.argmax(sizes)))
arm = cv2.dilate(arm.astype(np.uint8), np.ones((3, 3))) .astype(bool) & body
body_noarm = body & ~arm

def layer(mask, src=im, feather=1.2):
    out = src.copy(); a = (mask * 255).astype(np.uint8)
    a = np.asarray(Image.fromarray(a).filter(ImageFilter.GaussianBlur(feather)))
    out[..., 3] = np.minimum(src[..., 3], a); return Image.fromarray(out)

fur = (214, 204, 201)  # light fur tone
# body layer: fill the area hidden behind the head + the shoulder socket with fur colour
bodyL = layer(body_noarm)
fill = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(fill)
d.ellipse([270, 1190, 770, 1390], fill=fur + (255,))
d.ellipse([772, 1380, 860, 1500], fill=fur + (255,))
fill = fill.filter(ImageFilter.GaussianBlur(10))
bodyL = Image.alpha_composite(fill, bodyL)

# ears: extend down under the hat so rotation never shows a gap
earmask = ears.copy(); im_ext = im.copy()
for x in range(W):
    col = np.where(ears[:, x])[0]
    if len(col):
        y0 = col.max(); earmask[y0:min(H, y0 + 90), x] = True
        im_ext[y0:min(H, y0 + 90), x, :3] = im[max(0, y0 - 6), x, :3]; im_ext[y0:min(H, y0 + 90), x, 3] = 255
earL = layer(earmask & (xs < 520), im_ext); earR = layer(earmask & (xs >= 520), im_ext)
headL = layer(head); armL = layer(arm, feather=.8)

# eye patches (inpainted skin + drawn closed-eye line)
rgb = cv2.cvtColor(im[..., :3], cv2.COLOR_RGB2BGR)
lum = im[..., :3].mean(2)
def measure(x0, x1, y0, y1):
    reg = (lum < 120) & A; reg[:y0] = 0; reg[y1:] = 0; reg[:, :x0] = 0; reg[:, x1:] = 0
    yy, xx = np.where(reg); return (int((xx.min() + xx.max()) / 2), int((yy.min() + yy.max()) / 2)), (int((xx.max() - xx.min()) / 2), int((yy.max() - yy.min()) / 2))
EYEM = {'L': measure(200, 470, 840, 1060), 'R': measure(560, 830, 840, 1060)}
EYES = {k: v[0] for k, v in EYEM.items()}
print('eyes', EYEM)
def eye_patch(c, kind):
    cx, cy = c; k = 'L' if c == EYES['L'] else 'R'; rx, ry = EYEM[k][1]; rx += 20; ry += 20
    m = np.zeros((H, W), np.uint8); cv2.ellipse(m, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
    fillc = cv2.inpaint(rgb, m, 25, cv2.INPAINT_TELEA)
    sm = cv2.GaussianBlur(fillc, (0, 0), 14); mm = cv2.GaussianBlur(m, (0, 0), 8)[..., None] / 255.0
    fillc = (fillc * (1 - mm) + sm * mm).astype(np.uint8)
    patch = cv2.cvtColor(fillc, cv2.COLOR_BGR2RGB)
    out = np.zeros((H, W, 4), np.uint8); out[..., :3] = patch
    am = np.zeros((H, W), np.uint8); cv2.ellipse(am, (cx, cy), (rx + 8, ry + 8), 0, 0, 360, 255, -1)
    out[..., 3] = cv2.GaussianBlur(am, (0, 0), 6)
    img = Image.fromarray(out); d = ImageDraw.Draw(img)
    col = (58, 30, 34, 255)
    if kind == 'wink':   # happy ^ shape
        pts = [(cx - 62, cy + 18), (cx - 30, cy - 6), (cx, cy - 14), (cx + 30, cy - 6), (cx + 62, cy + 18)]
    else:                # relaxed closed eye
        pts = [(cx - 64, cy + 2), (cx - 32, cy + 16), (cx, cy + 20), (cx + 32, cy + 16), (cx + 64, cy + 2)]
    d.line(pts, fill=col, width=11, joint='curve')
    for p in (pts[0], pts[-1]): d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], fill=col)
    # little lashes on the outer corner
    side = -1 if c == EYES['L'] else 1; ex, ey = pts[-1] if side > 0 else pts[0]
    d.line([(ex, ey), (ex + 20 * side, ey - 14)], fill=col, width=7); d.line([(ex - 4 * side, ey + 2), (ex + 22 * side, ey + 6)], fill=col, width=6)
    return img
# glasses layer: grey metal frame, drawn above the eye patches
mx = im[..., :3].max(2).astype(int); mn = im[..., :3].min(2).astype(int)
gl = A & ((mx - mn) < 26) & (lum > 120) & (ys > 760) & (ys < 1160)
for k, (c, (rx, ry)) in EYEM.items():
    e = np.zeros((H, W), np.uint8); cv2.ellipse(e, c, (rx + 4, ry + 4), 0, 0, 360, 1, -1); gl &= e == 0
glassesL = layer(gl, feather=.7)
out = f"{B}/assets/rig"; import os; os.makedirs(out, exist_ok=True)
glassesL.save(f"{out}/glasses.png")
for name, imgL in [('body', bodyL), ('earL', earL), ('earR', earR), ('head', headL), ('arm', armL)]: imgL.save(f"{out}/{name}.png")
for k, c in EYES.items():
    eye_patch(c, 'wink').save(f"{out}/eye{k}_wink.png"); eye_patch(c, 'blink').save(f"{out}/eye{k}_blink.png")
piv = dict(W=W, H=H, earL=[300, 480], earR=[745, 470], head=[520, 1300], arm=[800, 1415])
json.dump(piv, open(f"{out}/pivots.json", 'w')); print('ok', piv, 'arm px', int(arm.sum()), 'fur', fur)
