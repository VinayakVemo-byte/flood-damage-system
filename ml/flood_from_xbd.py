import cv2
import numpy as np
import os

OUT = "runtime/outputs"

def detect_flood(before, after):

    os.makedirs(OUT, exist_ok=True)

    b = cv2.imread(before,0)
    a = cv2.imread(after)

    gray_after = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)

    b = cv2.resize(b,(256,256))
    gray_after = cv2.resize(gray_after,(256,256))
    a = cv2.resize(a,(256,256))

    diff = cv2.absdiff(b, gray_after)

    _, mask = cv2.threshold(diff,30,255,cv2.THRESH_BINARY)

    mask_path = os.path.join(OUT,"flood_mask.png")
    overlay_path = os.path.join(OUT,"overlay.png")

    cv2.imwrite(mask_path, mask)

    flooded_pixels = int((mask>0).sum())

    overlay = a.copy()
    overlay[mask>0] = [0,0,255]

    cv2.imwrite(overlay_path, overlay)

    percent = (mask>0).mean()*100

    return round(percent,2), flooded_pixels
