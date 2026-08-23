from pathlib import Path

from PIL import Image, ImageDraw


OUTPUT = Path(__file__).with_name("synthetic-portrait.png")

canvas = Image.new("RGB", (900, 1200), "#dce7ef")
draw = ImageDraw.Draw(canvas)
draw.rectangle((0, 840, 900, 1200), fill="#36536a")
draw.ellipse((205, 155, 695, 815), fill="#d89973")
draw.pieslice((160, 90, 740, 650), 180, 360, fill="#273746")
draw.ellipse((325, 420, 385, 470), fill="#263746")
draw.ellipse((515, 420, 575, 470), fill="#263746")
draw.arc((355, 500, 545, 680), 20, 160, fill="#7a3d3d", width=14)
draw.rounded_rectangle((270, 760, 630, 1070), radius=90, fill="#f4c95d")
draw.text((36, 1128), "Synthetic portrait test fixture", fill="#ffffff")
canvas.save(OUTPUT, format="PNG", optimize=True)
print(OUTPUT)
