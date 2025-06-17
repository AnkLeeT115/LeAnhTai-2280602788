def left_rotate(value, shift):
    value &= 0xFFFFFFFF
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def md5(message):
    # Khởi tạo các biến ban đầu
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    # Bảng hằng số (số lượng xoay và các hằng số sẵn có trong MD5)
    s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4
    K = [int(abs(__import__('math').sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]

    # Padding message
    original_length_bits = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'
    message += original_length_bits.to_bytes(8, byteorder='little')

    # Chia message thành các block 512-bit (64 bytes)
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        M = [int.from_bytes(block[j:j+4], 'little') for j in range(0, 64, 4)]

        A, B, C, D = a, b, c, d

        for j in range(64):
            if 0 <= j <= 15:
                F = (B & C) | ((~B) & D)
                g = j
            elif 16 <= j <= 31:
                F = (D & B) | ((~D) & C)
                g = (5*j + 1) % 16
            elif 32 <= j <= 47:
                F = B ^ C ^ D
                g = (3*j + 5) % 16
            else:
                F = C ^ (B | (~D))
                g = (7*j) % 16

            F &= 0xFFFFFFFF
            temp = D
            D = C
            C = B
            rotated = left_rotate((A + F + K[j] + M[g]) & 0xFFFFFFFF, s[j])
            B = (B + rotated) & 0xFFFFFFFF
            A = temp

        a = (a + A) & 0xFFFFFFFF
        b = (b + B) & 0xFFFFFFFF
        c = (c + C) & 0xFFFFFFFF
        d = (d + D) & 0xFFFFFFFF

    # Kết quả cuối cùng
    return '{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d)


input_string = input("Nhập chuỗi cần băm: ")
md5_hash = md5(input_string.encode('utf-8'))
print(f"Mã băm MD5 của chuỗi '{input_string}' là: {md5_hash}")
