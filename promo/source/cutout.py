import sys,numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage
src,dst=sys.argv[1],sys.argv[2]
im=np.asarray(Image.open(src).convert('RGB')).astype(float)
lum=im.max(2)
fg=lum>38
fg=ndimage.binary_fill_holes(ndimage.binary_closing(fg,iterations=3))
lab,n=ndimage.label(fg);sizes=ndimage.sum(fg,lab,range(1,n+1));keep=lab==(np.argmax(sizes)+1)
keep=ndimage.binary_fill_holes(keep)
a=Image.fromarray((keep*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.6))
out=Image.fromarray(im.astype(np.uint8)).convert('RGBA');out.putalpha(a)
out=out.crop(out.getbbox());out.save(dst);print(dst,out.size)
