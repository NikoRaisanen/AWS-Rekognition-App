# What is this?
This application allows you to automatically organize your photos by the people that appear in them. First you upload a headshot of the person that you would like to find in other pictures. Then you upload a directory, the program will traverse this directory and prepare the valid files for analysis.
The program then compares the subject in the headshot to each of the valid images in the uploaded directory. If the subject is found to be in the target image, then the file will be copied into a directory called "Matches".

## Accuracy
Analysis is done by calling the AWS Rekognition us-west1 endpoint. Below you can get a taste for the accuracy of results:

![](https://github.com/NikoRaisanen/AWS-Rekognition-App/blob/main/READMEContent/RekognitionExampleEdit.png)

**I chose to use these images as an example because:**

1. Drastically different lighting
2. Completely different angle of my face



Despite these differences, Rekognition was able to identify with strong certainty that I was present in the target image. You can visit https://us-west-1.console.aws.amazon.com/rekognition/home?region=us-west-1#/face-comparison to check the accuracy and see if it fits your use case

## Use case
With this program you can automtically sort through and organize photos based on the people in them. This means that you could have folders named "PhotosWithJim", "PhotosWithSally", "PhotosWithGrandma", etc.
This provides a more organized way to archive and look back on memories with specific people

## Getting credentials
- Go to the users section of your IAM console https://console.aws.amazon.com/iam/home#/users
- Add/create a user and check the box for programmatic access

![](https://github.com/NikoRaisanen/AWS-Rekognition-App/blob/main/READMEContent/CredentialsWalkthroughEdit.png)

- Give this user the "AmazonRekognitionFullAccess" permission policy
- Download the .csv file which contains your credentials

![](https://github.com/NikoRaisanen/AWS-Rekognition-App/blob/main/READMEContent/CredentialsWalkthrough2Edit.png)


## How to use
1. Obtain AWS credentials in .csv format (see below)
2. Clone this repository `git clone https://github.com/NikoRaisanen/AWS-Rekognition-App.git`
3. Copy the credentials .csv into the same directory that you cloned the repo to
4. Install python dependencies [Show dependencies here... I think it is just PyQt5(?)]
