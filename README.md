# Rock Detection App

## Introduction
This repository contains a set of Python scripts designed to demonstrate various computer vision techniques for rock detection using edge detection, contour detection, and real-time edge detection. The applications leverage the power of OpenCV for image processing and Streamlit for creating a user-friendly web interface.

## Installation

Before running the scripts, you need to install the required dependencies. It is recommended to use a virtual environment. To install the dependencies, run:

```bash
pip install opencv-python-headless streamlit numpy
```

## Usage

To run the Streamlit applications (`edge_detection.py` and `contour_area_detection.py`), execute the following command in your terminal:

```bash
streamlit run script_name.py
```

Replace `script_name.py` with the name of the script you want to run.

For the real-time edge detection script (`real_time_edge_detection.py`), simply run it with Python:

```bash
python real_time_edge_detection.py
```
## Scripts Description

### `edge_detection.py`

This script is a Streamlit app that allows users to upload an image and apply the Canny edge detector to identify edges within the image. It provides a user interface to adjust parameters such as Gaussian blur, and Canny edge detection thresholds. Users can view the original and edge-detected images side by side or one above the other, and download the edge-detected image.

### `contour_area_detection.py`

Another Streamlit app, this script extends the functionality of edge_detection.py by finding contours on the detected edges and calculating the area covered by these contours (e.g., rocks). It provides metrics such as the total image area, area covered by rocks, and empty area. Users can adjust image processing parameters, view the original, edge-detected, and contour-detected images, and download images as needed.

### `real_time_edge_detection.py`

This script demonstrates real-time edge detection using a video stream from a camera. It allows toggling between preview, Canny edge detection, and contour detection modes by pressing specific keys. The script includes functionality to switch between the primary and secondary camera if available.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.
