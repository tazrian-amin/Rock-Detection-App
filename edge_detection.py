import streamlit as st
import cv2
import numpy as np
from io import BytesIO

# Streamlit UI
st.title("Edge Detection with Canny Edge Detector")
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Convert the file to an OpenCV image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Sidebar for layout options
    st.sidebar.title("Display Options")
    layout_option = st.sidebar.radio("Choose the layout for displaying images:",
                                     ('Side by Side', 'Up and Down'),
                                     help="Select how you want to display the original and edge-detected images.")

    # Sidebar for Gaussian Blur parameters
    st.sidebar.title("Gaussian Blur Parameters")
    kernel_size = st.sidebar.slider("Kernel Size", min_value=1, max_value=31, value=9, step=2, help="Size of the Gaussian kernel. Must be odd.")
    sigma = st.sidebar.slider("Sigma", min_value=0, max_value=100, value=0, step=1, help="Standard deviation in X and Y directions. If 0, it is calculated from the kernel size.")

    # Apply Gaussian blur
    img_blur = cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), sigma)

    # Sliders for Canny Edge Detection thresholds
    st.sidebar.title("Edge Detection Parameters")
    threshold1 = st.sidebar.slider("Lower Threshold", min_value=0, max_value=1000, value=180, step=1, help="Lower threshold for edge detection")
    threshold2 = st.sidebar.slider("Upper Threshold", min_value=0, max_value=1000, value=200, step=1, help="Upper threshold for edge detection")

    # Detect edges with user-defined thresholds
    edges = cv2.Canny(img_blur, threshold1=threshold1, threshold2=threshold2)

    # Convert edges to colored image to display (optional)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Display images based on the layout option
    if layout_option == 'Side by Side':
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, channels="BGR", caption="Original Image")
        with col2:
            st.image(edges_colored, channels="BGR", caption="Edge Detected Image")
    else:  # 'Up and Down'
        st.image(img, channels="BGR", caption="Original Image")
        st.image(edges_colored, channels="BGR", caption="Edge Detected Image")

    # Convert the edge-detected image to a byte stream for download
    _, buffer = cv2.imencode('.png', edges_colored)
    byte_stream = BytesIO(buffer)

    # Create a download button and provide the byte stream as the file to download
    st.download_button(label="Download Edge Detected Image",
                       data=byte_stream,
                       file_name="edge_detected_image.png",
                       mime="image/png")
