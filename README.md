# ImageREconGenAI
Serverless application that uses Amazon Rekognition to detect image labels and Amazon Bedrock to generate  nutritional facts from the food label


This project is composed of three main operations: 
  1. store image to be analyzed
  2. extract image labels
  3. generate nutritional facts if labels are food related

In the repo file you will find the following files that puts together a front and back end
Files: 
  1. rekognition-bedrock.py <-Lambda function logic to extract labels, and generate bedrock response
  2. fetch-output-index.js <-Node.js script to pull the bedrock response from output.txt into the front end
  3. index.html <-front end HTML/Javascript web page

Solution Architecture:
![image](https://github.com/Mlyrics/nutrition-ai/assets/150750290/fd4e9b84-f123-4108-aa3a-362adc3ac925)

Deployment Steps: 
# Create S3 buckets
1. Create a S3 bucket to store the Amazon Bedrock output text- file. 
2. Create a S3 bucket to store the Image that will be analyzed

# Enable Amazon Bedrock Models
1. Go to the Amazon Bedrock service console
2. Click on Get Started
3. From the left menu click on Model Access, click on Manage model access, choose all models and click Save

# Setup Rekognition-Bedrock Lambda functions
1. Create a new Lambda function in Paython 3.12 and provide a any name
2. Copy & Paste the code in rekognition-bedrock.py
3. Update line #8 with your S3 bucket where the Amazon Bedrock response output text file will be stored
4. Update line #40 with the bucket name where you want to store the food related image to be analyzed
5. Save & Deploy
6. Add the appropriate permissions for Bedrock Access and S3 bucket
7. Change the Lambda application timeout to 45 sec under the Configuration tab
8. Configure a a S3 Trigger for the Lambda function:
   a. From the Lambda function main console, click on "Add Trigger"
   b. Source: S3
   c. Bucket: the S3 bucket where the image will be stored
   d. Event Types: PUT, POST
   e. suffix: .jpg
   f. Acknowlede recursive invokation and Add

# Setup Fetch output
1. Create a Node.js 14.x Lambda Function
2. Copy & Paste the code from the fetch-output-index.js file
3. Save & Deploy
4. Add the appropriate permissions for S3 bucket access

# Setup API Gateway
1. Create a REST API with a S3 integration with a PUT request to store the image into the bucket
2. Create  REST API with a Lambda integration with a ANY request to fetch the output of the Bedrock

# Front End web app
1. Edit the index.html file
2. Update line #126 with the PUT API endpoint URL
3. Update line #84 with the ANY API enpoint URL
4. Save and Close
5. At this stage you could either host the application in S3 or preferred hsoting provider or run locally from your Browser. 
