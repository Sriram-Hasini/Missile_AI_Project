import struct


def float_to_binary(value):
    packed = struct.pack('!f', float(value))
    return ''.join(f'{byte:08b}' for byte in packed)


def float_to_hex(value):
    packed = struct.pack('!f', float(value))
    return packed.hex()


def detect_numeric_value(value):

    value = str(value).strip()

    # Hexadecimal

    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)

    # Binary

    elif all(c in "01" for c in value) and len(value) > 1:
        return int(value, 2)

    # Float

    elif "." in value:
        return float(value)

    # Integer

    else:
        return int(value)


def convert_value(value, target_type):

    try:

        numeric_value = detect_numeric_value(value)

        if target_type == "Integer":

            return int(numeric_value)

        elif target_type == "Float":

            return float(numeric_value)

        elif target_type == "Hex":

            return hex(int(numeric_value))

        elif target_type == "Binary":

            return bin(int(numeric_value))[2:]

        else:

            return "Unsupported Conversion"

    except Exception as e:

        return f"Conversion Failed"