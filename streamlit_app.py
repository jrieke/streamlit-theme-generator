import streamlit as st
import numpy as np
import requests
from pathlib import Path


# This code is the same for each deployed app.
st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/woman-artist_1f469-200d-1f3a8.png",
    width=100,
)

"""
# Streamlit Theme Generator


Click below to generate a new color theme, based on color palettes from 
[colormind.io](http://colormind.io/). Note: This may not work properly if multiple 
people use the app at the same time.
"""

def clamp(x):
    return max(0, min(x, 255))


def rgb2hex(r, g, b):
    return "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))


CONFIG_TEMPLATE = """
[theme]
primaryColor = "{}"
backgroundColor = "{}"
secondaryBackgroundColor = "{}"
textColor = "{}"
font = "sans serif"
"""


def apply_random_theme():
    res = requests.get("http://colormind.io/api/", json={"model": "ui"})

    rgb_colors = res.json()["result"]
    hex_colors = [rgb2hex(*rgb) for rgb in res.json()["result"]]
    st.global_state = {"rgb_colors": rgb_colors, "hex_colors": hex_colors}

    config = CONFIG_TEMPLATE.format(
        hex_colors[3], hex_colors[0], hex_colors[1], hex_colors[4]
    )
    print(config)

    config_dir = Path(".streamlit")
    config_dir.mkdir(parents=True, exist_ok=True)
    with (config_dir / "config.toml").open("w") as f:
        f.write(config)

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


if st.button("New colors! 🎈"):
    apply_random_theme()
    st.info("Applying colors... (hit *Rerun* if asked)")


if hasattr(st, "global_state"):
    rgb_colors = st.global_state["rgb_colors"]
    hex_colors = st.global_state["hex_colors"]

    st.write("---")
    st.write("Here are your new colors:")
    columns = st.beta_columns(4)
    labels = ["Background", "2nd Background", "Primary", "Text"]
    for column, color, label in zip(
        columns, np.array(rgb_colors)[[0, 1, 3, 4]], labels
    ):
        image = np.zeros((150, 300, 3), np.uint8)
        image[3:-3, 3:-3] = color
        column.image(image, width=150)
        column.write(label)
        # ax.imshow(image)
        # ax.axis("off")

    config = CONFIG_TEMPLATE.format(
        hex_colors[3], hex_colors[0], hex_colors[1], hex_colors[4]
    )
    st.write("")
    st.write("And this is the config for them (put in `.streamlit/config.toml`):")
    st.code(config)


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

    st.checkbox("Is this cool or what?", key=key)
    st.radio(
        "How many balloons?",
        ["1 balloon 🎈", "2 balloons 🎈🎈", "3 balloons 🎈🎈🎈"],
        key=key,
    )
    st.button("🤡 Click me", key=key)

    # if plot:
    #     st.write("Oh look, a plot:")
    #     x1 = np.random.randn(200) - 2
    #     x2 = np.random.randn(200)
    #     x3 = np.random.randn(200) + 2

    #     hist_data = [x1, x2, x3]
    #     group_labels = ["Group 1", "Group 2", "Group 3"]

    #     fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])

    #     st.plotly_chart(fig, use_container_width=True)

    st.file_uploader("You can now upload with style", key=key)
    st.slider(
        "From 10 to 11, how cool are themes?", min_value=10, max_value=11, key=key
    )
    # st.select_slider("Pick a number", [1, 2, 3], key=key)
    st.number_input("So many numbers", key=key)
    st.text_area("A little writing space for you :)", key=key)
    st.selectbox(
        "My favorite thing in the world is...",
        ["Streamlit", "Theming", "Baloooons 🎈 "],
        key=key,
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