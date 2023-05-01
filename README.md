# Face Comparision with Amazon Rekognition

A solution to assist with identity verification using Amazon Rekognition.

## Prerequisites

- Install python 3.7 or later
- Clone this repository
- Install all dependencies
- Create an AWS account and set up authentication credentials for your account. (
  Read <a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console">this</a>)
- Once the user has been created, create and retrieve the keys used to authenticate the user. (
  Read <a href = "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey">
  this</a>)
- Create an S3 bucket
- Upload your source image (named {client}.jpg) to that bucket
- Create a file named "credentials.csv" under the root folder. Pass your access_key_id and secret_access_key on two
  separating lines
- Change the bucket name and source file name in the "rekognition.py" file to match yours
- Run the "rekognition.py" file and enjoy ( •̀ ω •́ )✧