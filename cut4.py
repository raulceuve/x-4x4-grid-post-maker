#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
4-part image splitter for X/Twitter memes
- GUI file selection
- Perfect even split (center crops if needed)
- Saves parts next to original image
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def make_perfect_four_split(image_path):
    if not os.path.isfile(image_path):
        return False, f"File not found: {image_path}"

    folder = os.path.dirname(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    try:
        img = Image.open(image_path).convert("RGB")
    except Exception as e:
        return False, f"Cannot open image: {e}"

    w, h = img.size

    # Make dimensions even → center crop max 1 px per side
    new_w = w - (w % 2)
    new_h = h - (h % 2)

    left = (w - new_w) // 2
    top  = (h - new_h) // 2

    if left or top:
        img = img.crop((left, top, left + new_w, top + new_h))

    half_w = new_w // 2
    half_h = new_h // 2

    pieces = [
        (0,       0,        half_w, half_h),      # 1 top-left
        (half_w,  0,        new_w,   half_h),     # 2 top-right
        (0,       half_h,   half_w,  new_h),      # 3 bottom-left
        (half_w,  half_h,   new_w,   new_h),      # 4 bottom-right
    ]

    saved = []

    for i, box in enumerate(pieces, 1):
        piece = img.crop(box)
        out_path = os.path.join(folder, f"{base_name}_part{i}.jpg")
        piece.save(out_path, "JPEG", quality=92, optimize=True)
        saved.append(out_path)

    msg = f"Done! Created 4 files next to your image:\n\n"
    for p in saved:
        msg += f"• {os.path.basename(p)}\n"
    msg += "\nUpload order on X: 1 → 2 → 3 → 4"

    return True, msg


def main():
    root = tk.Tk()
    root.withdraw()  # hide empty window

    # Ask user to select one or more images
    files = filedialog.askopenfilenames(
        title="Select image(s) to split into 4 parts",
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.webp *.bmp"),
            ("All files", "*.*")
        ]
    )

    if not files:
        return  # user cancelled

    results = []
    for path in files:
        success, message = make_perfect_four_split(path)
        results.append(f"→ {os.path.basename(path)}\n   {message}")

    # Show final result
    final_msg = "Image splitting finished!\n\n" + "\n\n".join(results)
    messagebox.showinfo("All done", final_msg)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        tk.messagebox.showerror("Error", f"Something went wrong:\n\n{str(e)}")
