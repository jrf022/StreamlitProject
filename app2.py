import pandas as pd  # pip install pandas
from PIL import Image  # pip install pillow
import streamlit as st  # pip install streamlit
# pip install streamlit-drawable-canvas
from streamlit_drawable_canvas import st_canvas

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("point",  # "freedraw",
                      "line",  "curve", "text",
                      "rect", "polygon",  # "circle", "polygon",
                      "transform")
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == 'point':
    point_display_radius = st.sidebar.slider(
        "Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])

realtime_update = st.sidebar.checkbox("Update in realtime", True)

# Add a text input field for the label when the drawing mode is "text"
label = st.sidebar.text_input("Label: ") if drawing_mode == "text" else None

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=realtime_update,
    height=400,
    drawing_mode=drawing_mode,
    # text=label,  # Use the entered label as the text to be drawn
    point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)

# Do something interesting with the image data and paths
if canvas_result.image_data is not None:
    st.image(canvas_result.image_data)
if canvas_result.json_data is not None:
    # need to convert obj to str because PyArrow
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
    st.dataframe(objects)


# -----------------------------------------------------------------------------------
# Initialize and run the component template frontend in webpack:
# cd ./streamlit_drawable_canvas/frontend
# npm install # install dependencies # done once
# npm start  #the frontend in the development mode

# From a separate terminal, run the template's Streamlit app (python file):
# conda activate streamlit-drawable-canvas
# cd _mycomp6_sdcanvas_dev  # this is were the app.py is
# pip install -e . # install template as editable package (dont forget the "period") (assuming the venv't is activated already) # done once
#  streamlit run ./app2.py
