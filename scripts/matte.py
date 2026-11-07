#!/usr/bin/env python3
"""Portrait matte (person cutout) for a folder of frames with MODNet (ONNX).
Usage: matte.py <frames_dir> <out_dir>   -> writes 8-bit grayscale PNG mattes, same names."""
import sys
from pathlib import Path
import cv2
import numpy as np
import onnxruntime as ort

MODEL = Path(__file__).resolve().parent.parent / "tools-models/modnet/onnx/model.onnx"


def main(src, dst):
    sess = ort.InferenceSession(str(MODEL), providers=["CPUExecutionProvider"])
    inp = sess.get_inputs()[0].name
    out = Path(dst); out.mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(src).glob("*.png")):
        im = cv2.cvtColor(cv2.imread(str(f)), cv2.COLOR_BGR2RGB)
        h, w = im.shape[:2]
        rh, rw = 672, 384  # multiples of 32, keeps 9:16-ish ratio
        x = cv2.resize(im, (rw, rh), interpolation=cv2.INTER_AREA).astype(np.float32)
        x = (x / 255.0 - 0.5) / 0.5
        x = x.transpose(2, 0, 1)[None]
        m = sess.run(None, {inp: x})[0][0][0]
        m = cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(str(out / f.name), np.clip(m * 255, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
