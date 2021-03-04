import csv
import sys
import json
import boto3
import os
import time
import shutil

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

    listImagesMatch = [] 
    for file in listImages:

        imageSource = open(sourceFile, 'rb')
        imageTarget = open(os.getcwd() + '\\' + targetDir + '\\' + file, 'rb')
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
            print(f"Match found: {file}")
        else:
            print(f"Not a match: {file}")
        time.sleep(1)   # For debugging purposes, remove in final version
    
    return listImagesMatch


def copy_files(listMatches):
    for item in listMatches:
        source = os.getcwd() + '\\' + targetDir + '\\' + item
        destination = os.getcwd() + '\\' + 'Matches' + '\\' + item
        shutil.copyfile(source, destination)
        print(f"Copying {item} to {destination}...")
        time.sleep(1)   # Debugging purposes, remove in final version


def main():
    global targetDir
    if len(sys.argv) != 3:
        print('Please execute the file in the following format: python {script} {sourceFile} {targetDir}')
        sys.exit(1)
    else:
        sourceFile = sys.argv[1]
        targetDir = sys.argv[2]

    
    listMatches = compare_faces(sourceFile, targetDir)
    print(f"Here are the files that returned as matches: {listMatches}")
    copy_files(listMatches)


if __name__ == "__main__":
    main()
