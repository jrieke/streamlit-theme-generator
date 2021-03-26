import requests
from pathlib import Path
import streamlit as st
import numpy as np
from PIL import Image, ImageOps

import utils

# Show header.
st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/woman-artist_1f469-200d-1f3a8.png",
    width=100,
)

"""
# Streamlit Theme Generator

Click below to generate a color palette and apply it to this app! 🎨 Powered by [colormind.io](http://colormind.io/bootstrap/)
"""

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

# Show current theme colors.
locked = []
columns = st.beta_columns(4)
labels = ["backgroundColor", "secondaryBackgroundColor", "primaryColor", "textColor"]
for column, label in zip(columns, labels):
    img = Image.new("RGB", (100, 50), state[label])
    img = ImageOps.expand(img, border=1, fill="black")
    # image = np.zeros((150, 300, 3), np.uint8)
    # image[3:-3, 3:-3] = color
    column.image(img, width=150)
    column.markdown(f"<sup>{label}<br>{state[label]}</sup>", unsafe_allow_html=True)
    # TODO: Do this with st.checkbox, but doesn't return the proper value with current wheel.
    lock_value = column.radio("", ["Locked", "Unlocked"], index=1, key="lock-" + label)
    locked.append(lock_value == "Locked")
    column.color_picker(
        label.rstrip("Color").replace("B", " b").capitalize(),
        state[label],
        key="color_picker" + label,
    )
    # ax.imshow(image)
    # ax.axis("off")
# st.write(locked)

# tab = st.text_input("Which tab is this?")
# st.write(tab)
# print(tab, state.primaryColor)


def apply_theme_from_session_state():
    # print(tab, " - config primary:", st.config.get_option("theme.primaryColor"))
    # print(tab, " - state primary: ", state.primaryColor)
    if st.config.get_option("theme.primaryColor") != state.primaryColor:
        # print(tab, " - DIFFERENCE, APPLYING THEME NOW")
        st.config.set_option("theme.primaryColor", state.primaryColor)
        st.config.set_option("theme.backgroundColor", state.backgroundColor)
        st.config.set_option(
            "theme.secondaryBackgroundColor", state.secondaryBackgroundColor
        )
        st.config.set_option("theme.textColor", state.textColor)
        st.experimental_rerun()
    else:
        # print(tab, " - no difference, did not apply theme")
        pass


def apply_random_theme():
    if any(locked):
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
        print(input_list)
        res = requests.get(
            "http://colormind.io/api/", json={"input": input_list, "model": "ui"}
        )
        # "input":
    else:
        res = requests.get("http://colormind.io/api/", json={"model": "ui"})

    rgb_colors = res.json()["result"]
    hex_colors = [utils.rgb2hex(*rgb) for rgb in res.json()["result"]]
    # st.global_state = {"rgb_colors": rgb_colors, "hex_colors": hex_colors}

    state.rgb_palette = rgb_colors
    if theme_type == "Light":
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

    apply_theme_from_session_state()
    # st.experimental_rerun()

    # config = CONFIG_TEMPLATE.format(
    #     hex_colors[3], hex_colors[0], hex_colors[1], hex_colors[4]
    # )
    # print(config)

    # config_dir = Path(".streamlit")
    # config_dir.mkdir(parents=True, exist_ok=True)
    # with (config_dir / "config.toml").open("w") as f:
    #     f.write(config)

    # TODO: Store these colors in session state or globally, so they don't get removed
    #   as soon as streamlit re-runs due to the changing config.
    # fig, axes = plt.subplots(1, 5)
    # columns = st.beta_columns(5)
    # for column, color in zip(columns, rgb_colors):
    #     image = np.zeros((300, 300, 3), np.uint8)
    #     image[:] = color
    #     column.image(image)
    #     # ax.imshow(image)
    #     # ax.axis("off")


theme_type = st.radio("Which kind?", ["Light", "Dark"])

if st.button("🔄 New colors! 🎈"):
    # print()
    # print(tab, " - button pressed :)")
    if state.first_time:
        st.balloons()
        state.first_time = False
    apply_random_theme()
    st.info("Applying colors... (hit *Rerun* if asked)")
else:
    # print()
    apply_theme_from_session_state()


# st.markdown(
#     "<sub>Note: May not work properly if a lot of people use this app at the same time!</sub>",
#     unsafe_allow_html=True,
# )


st.write("---")


config = utils.CONFIG_TEMPLATE.format(
    state.primaryColor,
    state.backgroundColor,
    state.secondaryBackgroundColor,
    state.textColor,
)
st.write("")
st.write("To use them in your app, just add this code to `.streamlit/config.toml`:")
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