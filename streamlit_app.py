import requests
from pathlib import Path
import random
import streamlit as st
import numpy as np
from PIL import Image, ImageOps

import utils


st.set_page_config(
    "Streamlit Theme Generator",
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/woman-artist_1f469-200d-1f3a8.png",
)

utils.local_css("local_styles.css")

# Init state. This is only run whenever a new session starts (i.e. each time a new
# browser tab is opened).
state = st.get_state(
    primaryColor="#f63366",
    backgroundColor="#FFFFFF",
    secondaryBackgroundColor="#f0f2f6",
    textColor="#262730",
    is_dark_theme=False,
    first_time=True,
)


# Show header.
st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/woman-artist_1f469-200d-1f3a8.png",
    width=100,
)

"""
# Streamlit Theme Generator

Generate beautiful color themes for Streamlit, powered by [colormind.io](http://colormind.io/bootstrap/). 
Scroll down to see the theme in action 🎈
"""

""

col1, col2 = st.beta_columns([0.3, 0.7])
new_theme_clicked = col1.button("🔄 Generate new theme")
theme_type = col2.radio("", ["Light theme", "Dark theme"])
# spinner = st.empty()
# if not state.first_time:
#     ""
#     "Done! Scroll down to see your new theme 🎈 "
# TODO: Use a checkbox here instead. Doesn't work with current wheel file.
# dark_checked = st.checkbox("Use dark themes")  # "Black is beautiful" or "Make it dark"

"---"


# Show current theme colors.
locked = []
columns = st.beta_columns(4)
labels = ["backgroundColor", "secondaryBackgroundColor", "primaryColor", "textColor"]
for column, label in zip(columns, labels):
    # c = column.color_picker(
    #     label.rstrip("Color").replace("B", " b").capitalize(),
    #     state[label],
    #     key="color_picker" + label,
    # )
    # st.write(c)
    # st.text_input("c", state[label], key="test" + label)
    img = Image.new("RGB", (100, 50), state[label])
    img = ImageOps.expand(img, border=1, fill="black")
    column.image(img, width=150)
    column.markdown(
        f"<small>{label.rstrip('Color').replace('B', ' b').capitalize()}</small>",
        unsafe_allow_html=True,
    )
    # TODO: Do this with st.checkbox, but doesn't return the proper value with current wheel.
    lock_value = column.radio("", ["Locked", "Unlocked"], index=1, key="lock-" + label)
    locked.append(lock_value == "Locked")
    # TODO: Show colorpicker above instead of images.


def apply_theme_from_session_state():
    """Retrieve theme from session state and apply it to streamlit config."""
    # Only apply if theme in state differs from the current config. This is important
    # to not trigger rerun repeatedly.
    if st.config.get_option("theme.primaryColor") != state.primaryColor:
        st.config.set_option("theme.primaryColor", state.primaryColor)
        st.config.set_option("theme.backgroundColor", state.backgroundColor)
        st.config.set_option(
            "theme.secondaryBackgroundColor", state.secondaryBackgroundColor
        )
        st.config.set_option("theme.textColor", state.textColor)

        # Trigger manual rerun (required to actually apply the theme to the app).
        st.experimental_rerun()


def generate_new_theme():
    """Retrieve new theme from colormind, store in state, and apply to app."""
    if any(locked):
        # Generate only new colors for the colors that are not locked. These need to be
        # represented as "N" in the list below. Locked colors need to be represented by
        # their RGB values, e.g. [123, 123, 123].
        input_list = ["N", "N", "N", "N", "N"]
        # TODO: Refactor this.
        if locked[0]:
            if state.is_dark_theme:
                input_list[4] = utils.hex2rgb(state.backgroundColor)
            else:
                input_list[0] = utils.hex2rgb(state.backgroundColor)
        if locked[1]:
            if state.is_dark_theme:
                input_list[3] = utils.hex2rgb(state.secondaryBackgroundColor)
            else:
                input_list[1] = utils.hex2rgb(state.secondaryBackgroundColor)
        if locked[2]:
            input_list[2] = utils.hex2rgb(state.primaryColor)
        if locked[3]:
            if state.is_dark_theme:
                input_list[0] = utils.hex2rgb(state.textColor)
            else:
                input_list[4] = utils.hex2rgb(state.textColor)
        res = requests.get(
            "http://colormind.io/api/", json={"input": input_list, "model": "ui"}
        )
    else:
        # Generate new colors for all colors.
        res = requests.get("http://colormind.io/api/", json={"model": "ui"})

    # Retrieve results from colormind.io and convert to hex.
    rgb_colors = res.json()["result"]
    hex_colors = [utils.rgb2hex(*rgb) for rgb in res.json()["result"]]

    # TODO: Refactor this with the stuff above.
    # Store colors in session state. This is required so that separate tabs/users can
    # have different themes. If we would apply the theme directly to `st.config`,
    # every user would see the same theme!
    if theme_type == "Light theme":
        state.primaryColor = hex_colors[2]
        state.backgroundColor = hex_colors[0]
        state.secondaryBackgroundColor = hex_colors[1]
        state.textColor = hex_colors[4]
        state.is_dark_theme = False
    else:
        state.primaryColor = hex_colors[2]
        state.backgroundColor = hex_colors[4]
        state.secondaryBackgroundColor = hex_colors[3]
        state.textColor = hex_colors[0]
        state.is_dark_theme = True


""


if new_theme_clicked:
    if state.first_time:
        # Show some 🎈 🎈 the first time the user creates a new theme ;)
        st.balloons()
        state.first_time = False
    wait_texts = [
        "🎨 Mixing colors...",
        "🌈 Collecting rainbows...",
        "🖌️ Painting...",
        "🐿️ Making happy little accidents...",
        "🌲 Decision time...",
        "☀️ Lighting up...",
    ]
    # spinner.info(random.choice(wait_texts))
    generate_new_theme()

# TODO: Try to do everything after this call, because this triggers a re-run.
apply_theme_from_session_state()


# st.write("---")
""

"""
To use this theme in your app, just create a file *.streamlit/config.toml* in your app's 
root directory and add the following code:
"""

config = utils.CONFIG_TEMPLATE.format(
    state.primaryColor,
    state.backgroundColor,
    state.secondaryBackgroundColor,
    state.textColor,
)
st.code(config)
st.write("---")


# Draw some dummy content in main page and sidebar.
def draw_all(
    key,
    plot=False,
):
    st.write(
        """
        ## Example Widgets
        
        These widgets don't do anything. But look at all the new colors they got 👀 
    
        ```python
        # First some code.
        streamlit = "cool"
        theming = "fantastic"
        both = "💥"
        ```
        """
    )

    st.checkbox("Is this cool or what?", key=key + "check")
    st.radio(
        "How many balloons?",
        ["1 balloon 🎈", "2 balloons 🎈🎈", "3 balloons 🎈🎈🎈"],
        key=key + "radio",
    )
    st.button("🤡 Click me", key=key + "button")

    # if plot:
    #     st.write("Oh look, a plot:")
    #     x1 = np.random.randn(200) - 2
    #     x2 = np.random.randn(200)
    #     x3 = np.random.randn(200) + 2

    #     hist_data = [x1, x2, x3]
    #     group_labels = ["Group 1", "Group 2", "Group 3"]

    #     fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])

    #     st.plotly_chart(fig, use_container_width=True)

    # st.file_uploader("You can now upload with style", key=key + "file_uploader")
    st.slider(
        "From 10 to 11, how cool are themes?",
        min_value=10,
        max_value=11,
        key=key + "slider",
    )
    # st.select_slider("Pick a number", [1, 2, 3], key=key)
    st.number_input("So many numbers", key=key + "number")
    # st.text_area("A little writing space for you :)", key=key + "text")
    st.selectbox(
        "My favorite thing in the world is...",
        ["Streamlit", "Theming", "Baloooons 🎈 "],
        key=key + "select",
    )
    # st.multiselect("Pick a number", [1, 2, 3], key=key)
    # st.color_picker("Colors, colors, colors", key=key)
    with st.beta_expander("Expand me!"):
        st.write("Hey there! Nothing to see here 👀 ")
    st.write("")
    # st.write("That's our progress on theming:")
    # st.progress(0.99)
    if plot:
        st.write("And here's some data and plots")
        st.json({"data": [1, 2, 3, 4]})
        st.dataframe({"data": [1, 2, 3, 4]})
        st.table({"data": [1, 2, 3, 4]})
        st.line_chart({"data": [1, 2, 3, 4]})
        # st.help(st.write)
    st.write("This is the end. Have fun building themes!")


draw_all("main", plot=True)

with st.sidebar:
    draw_all("sidebar")