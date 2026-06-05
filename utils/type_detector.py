def detect_type(value):

    value = str(value).strip()

    try:
        int(value)
        return "Integer"
    except:
        pass

    try:
        float(value)
        if "." in value:
            return "Float"
    except:
        pass

    if value.startswith("0x") or value.startswith("0X"):
        return "Hexadecimal"

    if all(c in "01" for c in value):
        return "Binary"

    return "Unknown"