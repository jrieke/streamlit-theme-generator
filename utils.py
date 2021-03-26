import streamlit as st


CONFIG_TEMPLATE = """
[theme]
primaryColor = "{}"
backgroundColor = "{}"
secondaryBackgroundColor = "{}"
textColor = "{}"
font = "sans serif"
"""


def clamp(x):
    return max(0, min(x, 255))


def rgb2hex(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


def hex2rgb(h):
    return tuple(int(h.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))


def local_css(file_name: str) -> None:
    """Loads a local .css file into streamlit."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
