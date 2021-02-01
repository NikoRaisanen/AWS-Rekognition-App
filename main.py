import csv
import sys
import json
import boto3

# Authenticating so that I can utilize AWS services
with open('niko11_user_credentials.csv', 'r') as credentials:
    next(credentials)
    reader = csv.reader(credentials)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]


def detect_labels(photo):
    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key,
                          region_name='us-west-1')
    with open(photo, 'rb') as image:
        response = client.detect_labels(
            Image={'Bytes': image.read()})
        return json.dumps(response, indent=4)


def main():
    if len(sys.argv) != 2:
        print('Please execute the file in the following format: python {script} {image.jpg}')
        sys.exit(1)
    else:
        photo = sys.argv[1]

    # Can always call data_string to see full Rekognition output
    data_string = detect_labels(photo)
    data_dict = json.loads(data_string)

    for item in data_dict['Labels']:
        print(f"I am %{item['Confidence']:.2f} sure that this is a {item['Name']}")


if __name__ == "__main__":
    main()
