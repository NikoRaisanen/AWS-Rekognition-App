import csv
import sys
import json
import boto3
import os

# Authenticating so that I can utilize AWS services
with open('niko11_user_credentials.csv', 'r') as credentials:
    next(credentials)
    reader = csv.reader(credentials)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]


def compare_faces(sourceFile, targetFile):
    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key,
                          region_name='us-west-1')
    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=80,
                                    SourceImage = {'Bytes': imageSource.read()},
                                    TargetImage = {'Bytes': imageTarget.read()})
    return json.dumps(response, indent=4)


def main():
    if len(sys.argv) != 3:
        print('Please execute the file in the following format: python {script} {sourceFile} {targetFile}')
        sys.exit(1)
    else:
        sourceFile = sys.argv[1]
        targetFile = sys.argv[2]

    # Can always call data_string to see full Rekognition output
    RekognitionResults = compare_faces(sourceFile, targetFile)
    for item in RekognitionResults['UnmatchedFaces']:
        print(item)
    # data_string = detect_labels(photo)
    # data_dict = json.loads(data_string)

    # for item in data_dict['Labels']:
    #     print(f"I am %{item['Confidence']:.2f} sure that this is a {item['Name']}")
    # print(os.listdir(os.getcwd() + directory))  # Prints all files in the user-inputted directory (must be from the program root folder)


if __name__ == "__main__":
    main()
