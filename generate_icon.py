#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成应用图标
"""

import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw

    icon_dir = Path(__file__).parent / "gui" / "resources"
    icon_dir.mkdir(parents=True, exist_ok=True)

    icon_path = icon_dir / "icon.ico"

    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []

    for size in sizes:
        img = Image.new("RGBA", size, (102, 126, 234, 255))
        draw = ImageDraw.Draw(img)

        margin = size[0] // 8
        draw.rounded_rectangle(
            [margin, margin, size[0] - margin, size[1] - margin],
            radius=size[0] // 6,
            fill=(255, 255, 255, 255),
        )

        text_size = size[0] // 3
        draw.text(
            (size[0] // 2 - text_size // 3, size[1] // 2 - text_size // 3),
            "SAU",
            fill=(102, 126, 234, 255),
        )

        images.append(img)

    icon_path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(icon_path, format="ICO", sizes=[(s[0], s[1]) for s in sizes])

    print(f"图标已生成: {icon_path}")

except ImportError:
    print("Pillow未安装，跳过图标生成")
    print("请运行: pip install pillow")
