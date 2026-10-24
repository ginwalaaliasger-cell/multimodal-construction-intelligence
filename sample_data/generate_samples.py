"""
Generates crisp, high-resolution sample construction test images
for immediate 1-click demonstration in Structura AI.
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("sample_data", exist_ok=True)

# 1. Generate Site Safety Sample Image
def create_site_safety_sample():
    width, height = 800, 500
    img = Image.new("RGB", (width, height), color=(210, 225, 235))
    draw = ImageDraw.Draw(img)

    # Sky gradient / ground
    draw.rectangle([(0, 300), (width, height)], fill=(120, 110, 100)) # ground dirt/gravel
    draw.rectangle([(0, 320), (width, 340)], fill=(70, 70, 70))      # concrete foundation curb

    # Concrete building frame
    draw.rectangle([(50, 80), (350, 320)], fill=(180, 185, 190), outline=(100, 105, 110), width=4)
    # Columns and beams
    draw.rectangle([(80, 80), (120, 320)], fill=(160, 165, 170))
    draw.rectangle([(280, 80), (320, 320)], fill=(160, 165, 170))
    draw.rectangle([(50, 190), (350, 215)], fill=(150, 155, 160))

    # Scaffolding pipes (yellow/steel)
    for x in [380, 440, 500, 560]:
        draw.line([(x, 100), (x, 320)], fill=(220, 180, 30), width=4)
    for y in [140, 190, 240, 290]:
        draw.line([(380, y), (560, y)], fill=(220, 180, 30), width=4)
        # diagonal braces
        draw.line([(380, y), (560, y+50)], fill=(200, 160, 20), width=2)

    # Worker 1 on ground (with Helmet + High-Vis Vest)
    draw.ellipse([(620, 220), (645, 245)], fill=(245, 190, 30)) # Yellow Hard Hat
    draw.ellipse([(625, 245), (640, 260)], fill=(230, 180, 140)) # Face
    draw.rectangle([(620, 260), (645, 300)], fill=(255, 100, 0)) # Orange High-Vis Vest
    draw.rectangle([(623, 300), (631, 335)], fill=(40, 50, 70))  # Pants leg 1
    draw.rectangle([(634, 300), (642, 335)], fill=(40, 50, 70))  # Pants leg 2
    draw.rectangle([(621, 335), (632, 342)], fill=(30, 20, 10))  # Steel-toe boot 1
    draw.rectangle([(633, 335), (644, 342)], fill=(30, 20, 10))  # Steel-toe boot 2

    # Worker 2 on elevated scaffold (Missing harness warning zone)
    draw.ellipse([(460, 110), (485, 135)], fill=(255, 255, 255)) # White helmet
    draw.ellipse([(465, 135), (480, 150)], fill=(220, 170, 130)) # Face
    draw.rectangle([(460, 150), (485, 190)], fill=(50, 180, 50))  # Green Shirt (NO high-vis vest!)
    draw.rectangle([(462, 190), (472, 225)], fill=(60, 60, 80))
    draw.rectangle([(474, 190), (484, 225)], fill=(60, 60, 80))

    # Safety Hazard Banners / Annotations
    draw.rectangle([(20, 20), (330, 60)], fill=(20, 30, 45))
    draw.text((35, 30), "ACTIVE CONSTRUCTION ZONE - SITE A4", fill=(255, 255, 255))

    img.save("sample_data/site_safety_sample.jpg", "JPEG", quality=95)
    print("Created sample_data/site_safety_sample.jpg")


# 2. Generate Concrete Crack Sample Image
def create_crack_sample():
    width, height = 700, 500
    img = Image.new("RGB", (width, height), color=(185, 185, 185))
    draw = ImageDraw.Draw(img)

    # Concrete mottled texture
    import random
    random.seed(42)
    for _ in range(8000):
        rx = random.randint(0, width-1)
        ry = random.randint(0, height-1)
        c = random.randint(150, 210)
        img.putpixel((rx, ry), (c, c, c))

    # Draw prominent diagonal shear crack with branches
    crack_points = [
        (120, 80), (160, 120), (210, 150), (270, 210), (330, 240),
        (390, 310), (450, 350), (510, 410), (570, 460)
    ]
    for i in range(len(crack_points)-1):
        p1 = crack_points[i]
        p2 = crack_points[i+1]
        draw.line([p1, p2], fill=(40, 35, 30), width=5)
        # crack shadow / spall border
        draw.line([(p1[0]+1, p1[1]+1), (p2[0]+1, p2[1]+1)], fill=(90, 85, 80), width=2)

    # Secondary micro-fissures / branches
    draw.line([(270, 210), (310, 180), (360, 170)], fill=(60, 55, 50), width=2)
    draw.line([(390, 310), (420, 360), (440, 420)], fill=(60, 55, 50), width=3)
    draw.line([(210, 150), (190, 190)], fill=(70, 65, 60), width=2)

    # Scale bar in the corner
    draw.rectangle([(50, 430), (200, 465)], fill=(245, 245, 245), outline=(30, 30, 30), width=2)
    draw.line([(65, 450), (185, 450)], fill=(0, 0, 0), width=3)
    draw.line([(65, 442), (65, 458)], fill=(0, 0, 0), width=3)
    draw.line([(185, 442), (185, 458)], fill=(0, 0, 0), width=3)
    draw.text((85, 432), "SCALE: 50 mm", fill=(0, 0, 0))

    img.save("sample_data/crack_sample.jpg", "JPEG", quality=95)
    print("Created sample_data/crack_sample.jpg")

if __name__ == "__main__":
    create_site_safety_sample()
    create_crack_sample()
