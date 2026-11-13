from PIL import Image, ImageDraw, ImageFont
import os

correct_poem = []


WIDTH, HEIGHT = 900, 550

# 生成从上到下的渐变背景
def make_gradient(width, height, c1, c2):
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(c1[0] * (1 - y / height) + c2[0] * (y / height))
        g = int(c1[1] * (1 - y / height) + c2[1] * (y / height))
        b = int(c1[2] * (1 - y / height) + c2[2] * (y / height))
        draw.line((0, y, width, y), fill=(r, g, b))
    return img

# 柔和渐变：米黄 → 浅淡蓝紫
img = make_gradient(WIDTH, HEIGHT, (255, 250, 235), (225, 235, 255))
draw = ImageDraw.Draw(img)

# 字体
try:
    font = ImageFont.truetype("Helvetica.ttc", 28)
    big_font = ImageFont.truetype("Helvetica.ttc", 36)
except:
    font = ImageFont.load_default()
    big_font = ImageFont.load_default()

TITLE_COLOR = (60, 70, 90)
TEXT_COLOR = (30, 30, 30)
CODE_COLOR = (180, 20, 60)   # 高亮红色
LINE_COLOR = (180, 180, 180)

# 参考线（如果调试排版布局可以用来参考）
draw.line((WIDTH / 2, 0, WIDTH / 2, HEIGHT), fill=LINE_COLOR, width=1)
draw.line((0, HEIGHT / 2, WIDTH, HEIGHT / 2), fill=LINE_COLOR, width=1)

# 标题
title = ""
bbox_title = draw.textbbox((0, 0), title, font=big_font)
tw = bbox_title[2] - bbox_title[0]
draw.text(((WIDTH - tw) / 2, 25), title, font=big_font, fill=TITLE_COLOR)


# 关键：固定首字母列
margin_top = 140
line_gap = 55
# 固定：所有首字母都在这一列
FIXED_CODE_X = 220

print("===== 排版调试信息 =====")
y = margin_top

for idx, line in enumerate(correct_poem):
    first_char = line[0]
    rest_text = line[1:]

    # 首字母（固定 x）
    draw.text((FIXED_CODE_X, y), first_char, font=font, fill=CODE_COLOR)

    # 剩余文字紧跟在首字母后面
    bbox_code = draw.textbbox((0, 0), first_char, font=font)
    char_width = bbox_code[2] - bbox_code[0]
    rest_x = FIXED_CODE_X + char_width

    draw.text((rest_x, y), rest_text, font=font, fill=TEXT_COLOR)

    print(f"第 {idx+1} 行 | y={y:.0f} | 首字母 x = {FIXED_CODE_X}")
    y += line_gap

# 保存到桌面
desktop = os.path.expanduser("~/Desktop")
out_file = os.path.join(desktop, "poem_layout_result.png")
img.save(out_file)
img.show()

print(f"\n✅ 已保存到桌面：{out_file}")