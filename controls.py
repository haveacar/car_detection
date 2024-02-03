import json
import datetime
import cv2
import os
from ultralytics import YOLO
import redis
from keys import SecretsManager


def upload_configuration(config_file: str = 'settings1.json') -> dict:
    """
    Loads configuration settings from a specified JSON file.
    :param config_file: The name of the configuration file
    :return: A dictionary containing the configuration settings.
    """
    path = os.path.join(os.path.dirname(__file__), config_file)
    with open(path) as f:
        data = json.load(f)

    return data


class RedisClient:
    def __init__(self):
        """Initializes the RedisClient instance by setting up a connection pool to Redis."""
        # upload_config
        configuration = upload_configuration()

        # Initialize Redis connection pool
        self.pool = redis.ConnectionPool(
            host=configuration.get('redis_endpoint'),
            port=configuration.get('redis_port'),
            password=secret_manager_keys.get('REDIS_CLOUD_PASSWORD'),
            decode_responses=True
        )

    def test_redis_connection(self):
        """Tests the Redis connection by setting and then getting a value."""
        test_key = "test_connection_key"
        test_value = "hello_redis"
        try:
            # Use the connection pool to get a Redis connection
            with redis.Redis(connection_pool=self.pool) as r:
                # Set a value in Redis
                r.set(test_key, test_value)
                # Retrieve the value from Redis
                retrieved_value = r.get(test_key)

                # Check if the set and get operations were successful
                if retrieved_value == test_value:
                    print("Redis connection test successful: Value set and retrieved correctly.")
                else:
                    print("Redis connection test failed: Retrieved value does not match the set value.")
        except redis.RedisError as e:
            print(f"Redis connection test failed with an error: {e}")

    def cache_data(self, object_key: str) -> None:
        """
        Increments the count for a given object key in Redis
        :param object_key: The key under which the data is stored in Redis.
        :return: None
        """

        cache_key = f'detection_object:{object_key}'

        try:
            with redis.Redis(connection_pool=self.pool) as r:
                cached_data = r.get(cache_key)
                if cached_data:
                    # If data exists, parse it
                    cached_data = json.loads(cached_data)
                    # Increment the count
                    cached_data['count'] += 1
                else:
                    # If no data exists, initialize with count of 1
                    cached_data = {'count': 1}

                # Save updated data back to Redis
                r.set(cache_key, json.dumps(cached_data))

        except Exception as err:
            print(f'Error to get data from redis: {err}')


class CarDetector:
    def __init__(self, yolo_name, link, conf):
        """
        Initializes the CarDetector instance with a specified YOLO model, video source link, and
        confidence threshold for detections.

        :param yolo_name: The filename of the YOLO model to load
        :param link: The video source link. Can be a path to a video file or a camera stream.
        :param conf: The confidence threshold for object detection.
        """
        # Initialize an empty dictionary to track last write times
        self.last_write_time = {}
        # detection names
        self.names = ('car', 'motorbike', 'bus', 'truck', 'person', 'dog', 'bicycle', 'cat')
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

    def stream_detect(self) -> None:
        """
        Processes video frames from the specified source, performing object detection and tracking.
        :return: None
        """
        # Loop through the video frames
        while self.cap.isOpened():
            # Read a frame from the video
            success, frame = self.cap.read()

            if success:
                # Run YOLOv8 tracking on the frame, persisting tracks between frames
                results = self.model.track(frame, persist=True, conf=self.conf)

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

    def _detection_procesing(self, detected: list[dict], detection_time: int = 3) -> None:
        """
        Processes detected objects by filtering for specific object names. If an object is recognized
        :param detected: A list of dictionaries, each representing a detected object with
        details including the object's name.
        :param detection_time: A time for filter duplicates
        :return: None
        """

        current_time = datetime.datetime.now()
        if detected:
            unique_objects = set()  # Use a set to track unique object names detected in this frame
            for obj in detected:
                obj_name = obj.get('name')
                if obj_name in self.names:
                    unique_objects.add(obj_name)

            for obj_name in unique_objects:
                # Check if we've written this object type within the last two seconds
                if (obj_name not in self.last_write_time or
                        (current_time - self.last_write_time[obj_name]) > datetime.timedelta(seconds=detection_time)):

                    redis_client.cache_data(obj_name)
                    print('****Line***')
                    self.last_write_time[obj_name] = current_time

# upload configuration
configuration = upload_configuration()

# Usage
aws_secrets = SecretsManager(configuration.get('aws_access_key'), configuration.get('aws_secret_key'), configuration.get('aws_region_name'))
secret_manager_keys = aws_secrets.get_secret("logicgov")

# initialize redis client
redis_client = RedisClient()


