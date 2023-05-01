import csv
import os

import boto3
import cv2


def create_boto_client(service_name):
    global access_key_id, secret_access_key
    return boto3.client(service_name, aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key,
                        region_name="ap-southeast-1")


def face_comparision(source_image, target_image):
    print("Comparing...")
    client = create_boto_client('rekognition')
    response = client.compare_faces(SourceImage=source_image, TargetImage=target_image,
                                    SimilarityThreshold=0.9)

    print(response["FaceMatches"])


def capture_and_upload(file_name):
    print("Capturing....")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    print("Captured! Processing....")
    if not (os.path.exists("captured_images") and os.path.isdir("captured_images")):
        os.mkdir("captured_images")
    file_path = f'./captured_images/{file_name}_input.jpg'
    cv2.imwrite(file_path, frame)

    bucket_name = 'fcomp'
    client = create_boto_client('s3')
    client.upload_file(file_path, bucket_name, f'{file_name}_input.jpg')
    print("Uploaded!")


def main_program(file_name, bucket_name):
    capture_and_upload(file_name)

    target_image = {
        'S3Object': {
            'Bucket': f'{bucket_name}',
            'Name': f'{file_name}.jpg',
        }
    }

    source_image = {
        'S3Object': {
            'Bucket': f'{bucket_name}',
            'Name': f'{file_name}_input.jpg',
        }
    }

    face_comparision(source_image, target_image)


if __name__ == "__main__":
    with open("credentials.csv", "r") as input:
        reader = csv.reader(input)
        access_key_id = next(reader)[0]
        secret_access_key = next(reader)[0]

    # Change this to your source file name
    client_name = "client"

    # Change this to your bucket name
    bucket_name = "fcomp"

    main_program(client_name, bucket_name)
