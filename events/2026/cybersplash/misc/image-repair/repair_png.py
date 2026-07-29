import struct, zlib

with open('broken-image.png', 'rb') as f:
    data = bytearray(f.read())

height_offset = 20
print('Current height:', struct.unpack('>I', data[height_offset:height_offset+4])[0])

data[height_offset:height_offset+4] = struct.pack('>I', 400)

ihdr_chunk = data[12:29]
new_crc = zlib.crc32(ihdr_chunk) & 0xffffffff
data[29:33] = struct.pack('>I', new_crc)

with open('repaired.png', 'wb') as f:
    f.write(data)
print('Saved repaired.png with height=400')
