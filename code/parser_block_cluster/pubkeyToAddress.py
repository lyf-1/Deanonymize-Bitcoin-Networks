import struct
import hashlib
import base58
import codecs
import binascii


def in_address(in_pubkey):
    in_pubkey_hash256 = hashlib.sha256(in_pubkey).hexdigest()
    in_pubkey_hash160 = hashlib.new('ripemd160', codecs.decode(in_pubkey_hash256, 'hex')).hexdigest()
    in_verandpubkey_hash160 = "00" + in_pubkey_hash160
    in_verandpubkey_hash160_hash256 = hashlib.sha256(codecs.decode(in_verandpubkey_hash160, 'hex')).hexdigest()
    in_verandpubkey_hash160_hash256_2 = hashlib.sha256(codecs.decode(in_verandpubkey_hash160_hash256, 'hex')).hexdigest()
    in_subaddress = "00" + in_pubkey_hash160 + in_verandpubkey_hash160_hash256_2[:8]
    return base58.b58encode(codecs.decode(in_subaddress, 'hex'))


def get_address(in_pubkey):
    in_pubkey_hash256 = hashlib.sha256(in_pubkey).hexdigest()
    in_pubkey_hash160 = hashlib.new('ripemd160', codecs.decode(in_pubkey_hash256, 'hex')).hexdigest()
    in_verandpubkey_hash160 = "00" + in_pubkey_hash160
    in_verandpubkey_hash160_hash256 = hashlib.sha256(codecs.decode(in_verandpubkey_hash160, 'hex')).hexdigest()
    in_verandpubkey_hash160_hash256_2 = hashlib.sha256(codecs.decode(in_verandpubkey_hash160_hash256, 'hex')).hexdigest()
    in_subaddress = "00" + in_pubkey_hash160 + in_verandpubkey_hash160_hash256_2[:8]
    return base58.b58encode(codecs.decode(in_subaddress, 'hex'))


def to_hex(bytestring):
    """
    convert given little-endian bytestring to hex
    """
    return binascii.hexlify(bytestring[::-1])


def double_hash(bytestring):
    """
    double SHA256 hash given bytestring
    """
    return hashlib.sha256(hashlib.sha256(bytestring).digest()).digest()


def hash160(bytestring):
    """
    SHA256 hash of given bytestring followed by RIPEMD-160 hash
    """
    return hashlib.new('ripemd160', hashlib.sha256(bytestring).digest()).digest()


def base58(bytestring):
    """
    base58 encode given bytestring
    """
    base58_characters = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    value = int(binascii.hexlify(bytestring), 16)

    result = ""
    while value >= len(base58_characters):
        value, mod = divmod(value, len(base58_characters))
        result += base58_characters[mod]
    result += base58_characters[value]

    # handle leading zeros
    for byte in bytestring:
        if byte == 0:
            result += base58_characters[0]
        else:
            break

    return result[::-1]


def ripemd160_to_address(key_hash):
    version = b"\00"
    checksum = double_hash(version + key_hash)[:4]
    return base58(version + key_hash + checksum)


def public_key_to_address(public_key):
    return ripemd160_to_address(hash160(public_key))


def get_script(script):
    script_length = len(script)
    tokens = []
    script_index = 0
    while script_index < script_length:
        op_code = script[script_index]
        script_index += 1
        print(op_code)
        if op_code <= 75:
            tokens.append(script[script_index:script_index + op_code])
            script_index += op_code
        elif op_code == 97:
            tokens.append("OP_NOP")
        elif op_code == 118:
            tokens.append("OP_DUP")
        elif op_code == 136:
            tokens.append("OP_EQUALVERIFY")
        elif op_code == 169:
            tokens.append("OP_HASH160")
        elif op_code == 172:
            tokens.append("OP_CHECKSIG")
        else:
            print("unknown opcode", op_code)

    return tokens


def to_address(script):
    if len(script) == 2 and script[1] == "OP_CHECKSIG":
        address = public_key_to_address(script[0])
    # P2PKH address
    elif len(script) == 5 and (
            script[0] == "OP_DUP" and
            script[1] == "OP_HASH160" and
            script[3] == "OP_EQUALVERIFY" and
            script[4] == "OP_CHECKSIG"
    ):
        address = ripemd160_to_address(script[2])
    else:
        address = "invalid"
    return address


a = b'v\xa9\x14\x12\xab\x8d\xc5\x88\xca\x9dW\x87\xdd\xe7\xeb)V\x9d\xa6<:#\x8c\x88\xac'
b = get_script(a)
c = to_address(b)

