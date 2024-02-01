
import cv2
import os
from ultralytics import YOLO


class CarDetector:
    def __init__(self, yolo_name, link):
        # path
        path = os.path.join(os.path.dirname(__file__), yolo_name)
        # load yolo model
        self.model = YOLO(path)
        # load video stream
        self.cap = cv2.VideoCapture(link)
        # initialize detecting
        self.stream_detect()

    def stream_detect(self):
        # Loop through the video frames
        while self.cap.isOpened():
            # Read a frame from the video
            success, frame = self.cap.read()

            if success:
                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                results = self.model.track(frame, persist=True)

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Display the annotated frame
                cv2.imshow("YOLOv8 Tracking", annotated_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and close the display window
        self.cap.release()
        cv2.destroyAllWindows()


LINK = "http://185.146.206.159:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER"
# load_stream_video(LINK)

detector = CarDetector("yolov8s.pt", LINK)
