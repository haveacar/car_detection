from controls import upload_configuration, CarDetector

def run():
    """Main Function"""
    # Get config from settings file
    configuration = upload_configuration()

    CarDetector(
        configuration.get('yolo_name'),
        configuration.get('video_link'),
        configuration.get('conf'),
    )



if __name__ == '__main__':
    run()