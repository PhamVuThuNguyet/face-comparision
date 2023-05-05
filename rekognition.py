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

    print("Generating results...")
    bbox = list(response["FaceMatches"][0]["Face"]["BoundingBox"].values())
    conf = response["FaceMatches"][0]["Face"]["Confidence"]

    print(bbox, conf)

    return (bbox, conf)


def capture_and_upload(file_name):
    print("Capturing....")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Capturing", frame)
        if cv2.waitKey(1) == ord('q'):
            print("Captured! Processing....")
            if not (os.path.exists("captured_images") and os.path.isdir("captured_images")):
                os.mkdir("captured_images")
            file_path = f'./captured_images/{file_name}_input.jpg'
            cv2.imwrite(file_path, frame)
            break

    bucket_name = 'fcomp'
    client = create_boto_client('s3')
    client.upload_file(file_path, bucket_name, f'{file_name}_input.jpg')
    print("Uploaded!")

    cap.release()
    cv2.destroyAllWindows()


def view_result(bbox, conf, image_path):
    global client_name
    image = cv2.imread(image_path)
    r, c, _ = image.shape

    w = int(bbox[0] * c)
    h = int(bbox[1] * r)
    x = int(bbox[2] * c)
    y = int(bbox[3] * r)

    image  = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # add a label (text) to the image
    label = f'{client_name}-{conf}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    color = (0, 0, 255)
    text_size, _ = cv2.getTextSize(label, font, font_scale, thickness)
    text_x = x
    text_y = y - text_size[1]
    image = cv2.putText(image, label, (text_x, text_y), font, font_scale, color, thickness)

    cv2.imshow("Captured", image)

    cv2.waitKey(0)


def main_program(file_name, bucket_name):
    capture_and_upload(file_name)

    source_image = {
        'S3Object': {
            'Bucket': f'{bucket_name}',
            'Name': f'{file_name}.jpg',
        }
    }

    target_image = {
        'S3Object': {
            'Bucket': f'{bucket_name}',
            'Name': f'{file_name}_input.jpg',
        }
    }

    (bbox, conf) = face_comparision(source_image, target_image)

    view_result(bbox, conf, f'./captured_images/{file_name}_input.jpg')


if __name__ == "__main__":
    with open("credentials.csv", "r") as input:
        reader = csv.reader(input)
        access_key_id = next(reader)[0]
        secret_access_key = next(reader)[0]

    # Change this to your source file name
    client_name = "nguyet"

    # Change this to your bucket name
    bucket_name = "fcomp"

    main_program(client_name, bucket_name)
