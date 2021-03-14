# What is this application?
With this program you can automtically organize photos based on the people that appear in them. This means that you could have folders named "PhotosWithJim", "PhotosWithSally", "PhotosWithGrandma", etc. The goal of this program is to provide an organized way to archive and look back on memories with specific people. This is a GUI-based application but information is also printed in the terminal so that the user can understand what is going on behind the scenes.

This application allows you to automatically organize your photos by the people that appear in them. First you upload a headshot of the person that you would like to find in other pictures. Then you upload a directory, the program will traverse this directory and prepare the valid files for analysis.
The program then compares the subject in the headshot to each of the valid images in the uploaded directory. If the subject is found to be in the target image, then the file will be copied into a directory called "Matches"

![](https://github.com/NikoRaisanen/AWS-Rekognition-App/blob/main/READMEContent/ImageSorterExample.gif)

In addition to the GUI I included terminal output in the case that the GUI stops responding. The above example shows me selecting my LinkedIn photo as the reference picture, and selecting a folder called Images as the target directory. Matches of this analysis were copied into the Matches folder, as shown by terminal output.


## Accuracy
Analysis is done by calling the AWS Rekognition us-west-1 endpoint. Below you can get a taste for the accuracy of results:

![](https://github.com/NikoRaisanen/AWS-Rekognition-App/blob/main/READMEContent/RekognitionExampleEdit.png)

**I chose to use these images as an example because:**

1. Drastically different lighting
2. Completely different angle of my face
3. Different expression



Despite these differences, Rekognition was able to identify with a 99.4% certainty that I was present in the target image. You can visit https://us-west-1.console.aws.amazon.com/rekognition/home?region=us-west-1#/face-comparison to check the accuracy and see if it fits your use case


## How to use
1. Clone this repository `git clone https://github.com/NikoRaisanen/AWS-Rekognition-App.git`
2. Obtain AWS credentials in .csv format (see "Getting credentials" below)
3. Copy the credentials .csv into the same directory that you cloned the repo to
4. Install the dependencies for the program by running `pip install -r requirements.txt` in the AWS-Rekognition-App directory

## Getting credentials
Use of the Amazon Rekognition service is not free, so each user of the application must use their own credentials. The first 5,000 images per month are free, after which the price becomes $1 per 1,000 images. The program will look for a file that contains the word "credentials" and has an extension of .csv in the same folder as ImageSorter.py - and use that for authentication. Make sure to log in or create an AWS account before following the steps below

- Go to the users section of your IAM console https://console.aws.amazon.com/iam/home#/users
- Add/create a user and check the box for programmatic access

![](https://github.com/NikoRaisanen/AWS-Rekognition-App/blob/main/READMEContent/CredentialsWalkthroughEdit.png)

- Give this user the "AmazonRekognitionFullAccess" permission policy
- Download the .csv file which contains your credentials

![](https://github.com/NikoRaisanen/AWS-Rekognition-App/blob/main/READMEContent/CredentialsWalkthrough2Edit.png)
- To use these credentials in the program - copy this credentials csv file into the same directory as ImageSorter.py

## Future plans
This is an ongoing project and improvements can be expected. It currently satisfies the use case for organizing photos by the people present in them, but it is still too slow for my preference. I see this as an opportunity to learn about threading in python, a challenge that I welcome.
