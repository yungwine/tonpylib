import struct
import time

from bitarray import bitarray

from Cryptodome.Random import get_random_bytes
from hashlib import sha256

from crypto import enc_cipher, dec_cipher, dec_cipher2, enc_cipher2
# from tcp import s, enc_cipher, dec_cipher


def get_ping_request():
    data = b'\x00\x00\x00\x4c'[::-1]
    # data = 0x4c.to_bytes(byteorder='little', length=4)  # length

    nonce = get_random_bytes(32)

    data += nonce

    data += b'\x4d\x08\x2b\x9a'[::-1]  # TL id
    # data += 0x9a2b084d.to_bytes(byteorder='big', length=4)

    query_id = get_random_bytes(8)

    data += query_id[::-1]

    hash = sha256(data[4:]).digest()  # checksum
    data += hash

    # ping_result = enc_cipher.encrypt(data)
    ping_result = enc_cipher2.update(data)
    return ping_result, query_id


def parse_pong(data: bytes, query_id = None):
    assert data[32:36][::-1].hex() == 'dc69fb03'
    assert data[36:44][::-1] == query_id
    checksum = data[44:]
    hash = sha256(data[:44]).digest()
    assert checksum == hash
