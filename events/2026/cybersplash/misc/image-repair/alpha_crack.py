from PIL import Image

img = Image.open("broken-image.png").convert("RGBA")
pixels = list(img.getdata())

# Show unique alpha values
alphas = [p[3] for p in pixels]
print("Unique alpha values:", set(alphas))
print("First 20 alpha values:", alphas[:20])

# Extract LSB from each alpha value
bits = [p[3] & 1 for p in pixels]

# Group into bytes
chars = []
for i in range(0, len(bits) - 7, 8):
    byte = 0
    for b in range(8):
        byte = (byte << 1) | bits[i + b]
    if byte == 0:
        break
    chars.append(chr(byte))

print(''.join(chars))
