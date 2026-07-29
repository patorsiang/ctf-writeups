import struct

with open('broken-image.png', 'rb') as f:
    sig = f.read(8)
    print('PNG signature:', sig.hex())
    while True:
        length_bytes = f.read(4)
        if not length_bytes or len(length_bytes) < 4:
            break
        length = struct.unpack('>I', length_bytes)[0]
        chunk_type = f.read(4).decode('latin-1')
        data = f.read(length)
        crc = f.read(4)
        print(f'Chunk: {chunk_type}, Length: {length}')
        if chunk_type == 'IEND':
            break
