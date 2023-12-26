const AWS = require('aws-sdk');

const s3 = new AWS.S3();

exports.handler = async (event) => {
    const params = {
        Bucket: 'mulloap-bedrock-output-1', // Replace with your S3 bucket name
        Key: 'output.txt'
    };
    
    try {
        const data = await s3.getObject(params).promise();
        return {
            statusCode: 200,
            body: data.Body.toString('utf-8'),
            headers: {
                'Content-Type': 'text/plain'
            }
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: 'Error fetching content: ' + error.message
        };
    }
};
