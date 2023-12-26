import json
import boto3

# Initialize the Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime')

# S3 Bucket to store the output
output_bucket = "BUCKET FOR OUTPUT.TXT FILE"

def extract_food_beverage_labels(bucket, key, rekognition):
    try:
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            }
        )
        # Filter labels with the specified category
        food_and_beverage_labels = [label['Name'] for label in response['Labels'] if any(category['Name'] == 'Food and Beverage' for category in label.get('Categories', []))]
        return food_and_beverage_labels
    except rekognition.exceptions.ClientError as e:
        print(f"An error occurred in Rekognition: {str(e)}")
        return []

def upload_to_s3(text, output_key, s3):
    try:
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=text)
        print(f"Successfully uploaded to S3: {output_key}")
    except Exception as e:
        print(f"An error occurred while uploading to S3: {str(e)}")

def lambda_handler(event, context):
    # Initialize the Rekognition and S3 clients
    rekognition = boto3.client('rekognition')
    s3 = boto3.client('s3')

    # Assume the bucket and key where the image is stored do not change key value
    bucket = "BUCKET FOR IMAGE UPLOAD"
    key = "image.jpg"

    # Extract labels from the image using Rekognition
    image_labels = extract_food_beverage_labels(bucket, key, rekognition)

    # Use the first label as a variable in the prompt
    label_variable = image_labels[0] if image_labels else "unknown label"

    # Define the prompt with the required format
    prompt = (
        f"Human: Image labels: {', '.join(image_labels)}. Assume you are a dietitian. "
        f"Provide the nutritional facts of {label_variable} and suggest if this is healthy "
        f"according to the CDC and FDA.\n\nAssistant:"
    )

    # Build the request payload
    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.1,
        "top_p": 0.9
    })

    # Model ID and content types
    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'

    try:
        # Send the payload to Bedrock
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=modelId,
            accept=accept,
            contentType=contentType
        )

        # Parse the response
        response_body = json.loads(response['body'].read().decode('utf-8'))

        # Extracting text from 'completion' key
        if 'completion' in response_body:
            response_text = response_body['completion']
            print("Output from Bedrock:", response_text)

            # Store the response text in a file
            output_key = "output.txt"
            upload_to_s3(response_text, output_key, s3)
            print("Output saved to S3:", output_key)
        else:
            print("Response body does not contain 'completion' key:", response_body)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Full response body:", response_body)  # Print the full response for debugging

    return {
        'statusCode': 200,
        'body': json.dumps('Processed the request.')
    }


