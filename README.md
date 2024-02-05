
# Car Detection Application

## Overview

This application uses a YOLO (You Only Look Once) model for detecting cars, motorbikes, buses, trucks, persons, dogs, bicycles, and cats in video streams. It leverages OpenCV for video processing and Redis for data caching. The core functionality is encapsulated in two Python files: `application.py` and `controls.py`.

## Features

- Real-time detection of various objects including vehicles and pedestrians.
- Integration with Redis for caching detection results.
- Utilizes the ultralytics YOLO model for object detection.
- Configuration through JSON file for easy setup.

## Installation

### Prerequisites

- Python 3.11
- Redis server
- AWS account for Secrets Manager (optional for storing Redis credentials)

### Setup

1. Clone the repository:

```
git clone [link-to-repository]
```

Replace `[link-to-repository]` with the actual link to the GitHub repository where the code is hosted.

2. Install dependencies:

Navigate to the cloned directory and run:

```
pip install -r requirements.txt
```

3. Configure `settings1.json` with your Redis server and video stream settings.

4. (Optional) Configure AWS Secrets Manager for Redis credentials by setting up `keys.py` with your AWS credentials.

## Usage

To start the application, run:

```
python application.py
```

Ensure your Redis server is running and accessible as per your `settings1.json` configuration.

## Docker

A `Dockerfile` is provided for containerization of the application. Build and run the Docker container using:

```
docker build -t car-detection-app .
docker run -d -p 80:80 -p 18975:18975 car-detection-app
```

## Contributing

Contributions to the project are welcome. Please fork the repository, make your changes, and submit a pull request.
