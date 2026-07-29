import struct, zlib

with open('broken-image.png', 'rb') as f:
    data = f.read()

idat_start = data.index(b'IDAT')
length = struct.unpack('>I', data[idat_start-4:idat_start])[0]
idat_data = data[idat_start+4:idat_start+4+length]
raw = zlib.decompress(idat_data)

print(f'Decompressed IDAT size: {len(raw)} bytes')
print(f'Declared dimensions: 600x250, expected: {250 * (600*4 + 1)} bytes')
print(f'Actual height if width=600: {len(raw) / (600*4+1)} rows')
