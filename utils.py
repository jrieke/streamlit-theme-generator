def clamp(x):
    return max(0, min(x, 255))


def rgb2hex(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


def hex2rgb(h):
    return tuple(int(h.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))


CONFIG_TEMPLATE = """
[theme]
primaryColor = "{}"
backgroundColor = "{}"
secondaryBackgroundColor = "{}"
textColor = "{}"
font = "sans serif"
"""