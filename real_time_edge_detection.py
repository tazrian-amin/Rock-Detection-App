import cv2

s = 1  # Initially specify 1 for accessing the USB camera.
source = cv2.VideoCapture(s, cv2.CAP_DSHOW)

# Create a window to display the video stream.
win_name = 'Real-time Edge Detection Demo'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

PREVIEW = 0  # Preview Mode
CANNY = 1  # Canny Edge Detector
CONTOUR = 2  # Contour Mode
image_filter = PREVIEW
result = None

def switch_camera():
    global s, source
    s = 1 - s  # Toggle s between 0 and 1
    source.release()  # Release the current camera
    source = cv2.VideoCapture(s, cv2.CAP_DSHOW)  # Reinitialize the camera

while True:
    has_frame, frame = source.read()
    if not has_frame:
        break
    # Flip video frame for convenience.
    frame = cv2.flip(frame, 1)

    if image_filter == PREVIEW:
        result = frame
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 80, 150)
    elif image_filter == CONTOUR:
        edges = cv2.Canny(frame, 50, 250)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = cv2.drawContours(frame, contours, -1, (0, 230, 0), 2, cv2.LINE_AA)

    cv2.imshow(win_name, result)

    key = cv2.waitKey(1)
    if key == ord('Q') or key == ord('q') or key == 27:
        break
    elif key == ord('E') or key == ord('e'):
        image_filter = CANNY
    elif key == ord('C') or key == ord('c'):
        image_filter = CONTOUR
    elif key == ord('P') or key == ord('p'):
        image_filter = PREVIEW
    elif key == ord('T') or key == ord('t'):
        switch_camera()

source.release()
cv2.destroyAllWindows()
