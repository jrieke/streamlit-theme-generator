import streamlit as st
import numpy as np
import requests
from pathlib import Path
from PIL import Image, ImageOps

# import SessionState


# This code is the same for each deployed app.
st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/271/woman-artist_1f469-200d-1f3a8.png",
    width=100,
)

"""
# Streamlit Theme Generator

Click below to generate a color palette and apply it to this app! 🎨 Powered by [colormind.io](http://colormind.io/bootstrap/)
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

# state = SessionState.get(
#     primaryColor="#f63366",
#     backgroundColor="#FFFFFF",
#     secondaryBackgroundColor="#f0f2f6",
#     textColor="#262730",
# )

state = st.get_state(
    primaryColor="#f63366",
    backgroundColor="#FFFFFF",
    secondaryBackgroundColor="#f0f2f6",
    textColor="#262730",
)


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
    res = requests.get("http://colormind.io/api/", json={"model": "ui"})

    rgb_colors = res.json()["result"]
    hex_colors = [rgb2hex(*rgb) for rgb in res.json()["result"]]
    # st.global_state = {"rgb_colors": rgb_colors, "hex_colors": hex_colors}

    state.primaryColor = hex_colors[3]
    state.backgroundColor = hex_colors[0]
    state.secondaryBackgroundColor = hex_colors[1]
    state.textColor = hex_colors[4]

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


if st.button("New colors! 🎈"):
    # print()
    # print(tab, " - button pressed :)")
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
st.write("Here are your current colors:")
columns = st.beta_columns(4)
labels = ["backgroundColor", "secondaryBackgroundColor", "primaryColor", "textColor"]
for column, label in zip(columns, labels):
    webhexcolor = "#4878A8"
    img = Image.new("RGB", (100, 50), state[label])
    img = ImageOps.expand(img, border=1, fill="black")
    # image = np.zeros((150, 300, 3), np.uint8)
    # image[3:-3, 3:-3] = color
    column.image(img, width=150)
    column.markdown(f"<sup>{label}</sup>", unsafe_allow_html=True)
    # ax.imshow(image)
    # ax.axis("off")

config = CONFIG_TEMPLATE.format(
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