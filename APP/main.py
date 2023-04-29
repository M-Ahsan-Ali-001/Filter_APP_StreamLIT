import streamlit as st
import cv2
from PIL import Image
import numpy as np





st.title("FREE FILTER")

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Using "with" notation
with st.sidebar:
    st.markdown("<p style='color: red; font-size:25px;font-weight:bold'>Filto</p>", unsafe_allow_html=True)
    st.markdown("<div style ='  max-width=50px;  '> <h4 style=' border: 1px solid black; padding: 5px'> A filter Created with love</h4><br><br></div> "



                , unsafe_allow_html=True)

    add_radio = st.radio(
        "Convert your photo to:",
        (
        "Corner Detection",
        "Invert",
        "Blur",
        "Edge Detection",
        "Brightness"
        )
    )
    intensity = st.slider('Adjust intensity:', 1, 100, 50)

graay=False
def apply_filter(img, filter_name, intensity):
    if filter_name == "Corner Detection":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)

        corners = cv2.goodFeaturesToTrack(gray, intensity, 0.01, 10)
        corners = np.int0(corners)
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(img, (x, y), 3, 255, -1)




        return img


    elif filter_name == "Invert":
        img = intensity - img #255

        graay = False
    elif filter_name == "Blur":

        graay = False
        img = cv2.GaussianBlur(img, (15, 15), intensity/10)
    elif filter_name == "Edge Detection":
        img = cv2.Canny(img, intensity, intensity*3)

        graay = True
    elif filter_name == "Brightness":

        graay = False
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, intensity)
        img = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)

    return img




if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = np.array(image)

    filtered = apply_filter(img, add_radio, intensity)


    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, caption='Original Image', use_column_width=True)
    with col2:
        st.subheader("Filtered Image")
        filtered_image = Image.fromarray(filtered)
        st.image(filtered_image, caption=add_radio, use_column_width=True)
    if graay ==True:

         filerchange=filtered
    else:
        filerchange =  cv2.cvtColor(filtered,cv2.COLOR_BGR2RGB)

    save = st.button("Keep")
    if save:

        cv2.imwrite( 'output/filteredImage.jpg',    filerchange)
        st.warning('File Saved! ')


