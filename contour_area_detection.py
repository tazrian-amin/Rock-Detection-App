import streamlit as st
import cv2
import numpy as np
from io import BytesIO

# Streamlit UI
st.title("Edge & Contour Detection and Calculating Area")
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
                                     help="Select how you want to display the original, edge-detected, and contours images.")

    # Sidebar for Gaussian Blur parameters
    st.sidebar.title("Gaussian Blur Parameters")
    kernel_size = st.sidebar.slider("Kernel Size", min_value=1, max_value=31, value=9, step=2)
    sigma = st.sidebar.slider("Sigma", min_value=0, max_value=100, value=0, step=1)

    # Apply Gaussian blur
    img_blur = cv2.GaussianBlur(img_gray, (kernel_size, kernel_size), sigma)

    # Sliders for Canny Edge Detection thresholds
    st.sidebar.title("Edge Detection Parameters")
    threshold1 = st.sidebar.slider("Lower Threshold", min_value=0, max_value=1000, value=80, step=1)
    threshold2 = st.sidebar.slider("Upper Threshold", min_value=0, max_value=1000, value=200, step=1)

    # Detect edges
    edges = cv2.Canny(img_blur, threshold1=threshold1, threshold2=threshold2)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calculate the total area of the contours (rocks) and other metrics
    total_area_contours = sum(cv2.contourArea(contour) for contour in contours)
    total_image_area = img.shape[0] * img.shape[1]
    empty_area = total_image_area - total_area_contours

    # Calculate percentages
    percentage_area_contours = (total_area_contours / total_image_area) * 100
    percentage_empty_area = (empty_area / total_image_area) * 100

    # Use columns to display the metrics side by side
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Image Area (pixels)", value=f"{total_image_area}")
    with col2:
        st.metric(label="Area of Rocks (pixels)", value=f"{total_area_contours:.2f}")
    with col3:
        st.metric(label="Empty Area (pixels)", value=f"{empty_area:.2f}")

    # Display percentages with progress bars
    st.progress(percentage_area_contours / 100)
    st.write(f"Rocks: {percentage_area_contours:.2f}% | Empty: {percentage_empty_area:.2f}%")

    # Draw contours on a copy of the original image
    img_with_contours = img.copy()
    cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 3)

    # Convert edges to colored image to display (optional, for consistency with contours visualization)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Display images based on the layout option
    if layout_option == 'Side by Side':
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(img, channels="BGR", caption="Original Image")
        with col2:
            st.image(edges_colored, channels="BGR", caption="Detected Edges")
        with col3:
            st.image(img_with_contours, channels="BGR", caption="Detected Contours")
    else:  # 'Up and Down'
        st.image(img, channels="BGR", caption="Original Image")
        st.image(edges_colored, channels="BGR", caption="Detected Edges")
        st.image(img_with_contours, channels="BGR", caption="Detected Contours")

    # Convert the edge-detected image to a byte stream for download
    _, buffer_edges = cv2.imencode('.png', edges_colored)
    byte_stream_edges = BytesIO(buffer_edges)
    st.download_button(label="Download Edge Detected Image",
                       data=byte_stream_edges,
                       file_name="edge_detected_image.png",
                       mime="image/png")

    # Convert the image with contours to a byte stream for download
    _, buffer_contours = cv2.imencode('.png', img_with_contours)
    byte_stream_contours = BytesIO(buffer_contours)
    st.download_button(label="Download Image with Contours",
                       data=byte_stream_contours,
                       file_name="image_with_contours.png",
                       mime="image/png")
