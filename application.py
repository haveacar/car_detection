from controls import configuration, CarDetector, redis_client

def run():
    """Main Function"""

    # test redis cloud client
    redis_client.test_redis_connection()

    # initialize detection
    CarDetector(
        configuration.get('yolo_name'),
        configuration.get('video_link'),
        configuration.get('conf'),
    )


if __name__ == '__main__':
    run()
