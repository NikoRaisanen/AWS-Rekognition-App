import csv
import sys
import json
import boto3
import os
import time

# Authenticating so that I can utilize AWS services
with open('niko11_user_credentials.csv', 'r') as credentials:
    next(credentials)
    reader = csv.reader(credentials)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]


def compare_faces(sourceFile, targetDir):
    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key,
                          region_name='us-west-1')
    # imageSource = open(sourceFile, 'rb')
    listImages = os.listdir(targetDir)

    for file in listImages:
        listImagesMatch = [] 

        imageSource = open(sourceFile, 'rb')
        imageTarget = open(os.getcwd() + '\\' + 'Images' + '\\' + file, 'rb')
        response = client.compare_faces(SimilarityThreshold=80,
                                        SourceImage = {'Bytes': imageSource.read()},
                                        TargetImage = {'Bytes': imageTarget.read()})
        counter = 0
        isPresent = False
        for item in response['FaceMatches']:
            counter += 1
        if counter > 0:
            isPresent = True
            listImagesMatch.append(file)
            print("Match found")
        else:
            print("Not a match")
        time.sleep(1)   # For debugging purposes, remove in final version
    
    return listImagesMatch


def main():
    if len(sys.argv) != 3:
        print('Please execute the file in the following format: python {script} {sourceFile} {targetDir}')
        sys.exit(1)
    else:
        sourceFile = sys.argv[1]
        targetDir = sys.argv[2]

    
    listMatches = compare_faces(sourceFile, targetDir)
    print(listMatches)

    # print(os.listdir(os.getcwd() + directory))  # Prints all files in the user-inputted directory (must be from the program root folder)


if __name__ == "__main__":
    main()
