from controls import configuration, CarDetector, redis_client


def run() -> None:
    """
    Main function to test Redis connection and initialize car detection.

    This function first tests the connection to the Redis cloud client to ensure
    it is operational.
    :return: None
    """

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
