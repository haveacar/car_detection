import json

import cv2
import os
from ultralytics import YOLO

def upload_configuration() -> dict:
    """
    Function to upload basic settings from a JSON file.
    """
    path = os.path.join(os.path.dirname(__file__), 'settings.json')
    with open(path) as f:
        data = json.load(f)

    return data


class CarDetector:
    def __init__(self, yolo_name, link, conf):
        # detection names
        self.names = ('car', 'motorbike', 'bus', 'truck', 'person', 'dog', 'bicycle')
        # detection
        self.conf = conf
        # path
        path = os.path.join(os.path.dirname(__file__), yolo_name)
        # load yolo model
        self.model = YOLO(path)
        # load video stream
        self.cap = cv2.VideoCapture(link)
        # initialize detecting
        self.stream_detect()

    def stream_detect(self)->None:
        # Loop through the video frames
        while self.cap.isOpened():
            # Read a frame from the video
            success, frame = self.cap.read()

            if success:
                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                results = self.model.track(frame, persist=True, conf=0.2)

                # detected data processing

                detected_name = results[0].tojson()

                if detected_name:
                    self._detection_procesing(json.loads(detected_name))

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

    def _detection_procesing(self, detected:list[dict])->None:

       if detected:
           for object in detected:
               if object.get('name') in self.names:
                   print('********', object)




