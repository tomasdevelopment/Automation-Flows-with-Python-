Step 0: Set Up Your Data Storage
Set Up Your Database:

Ensure you have a database to handle your requests. In this case, we use Amazon Redshift.
Create a Table:

Use Python to integrate with Redshift and create a table. 

Use SQL Sentences to filter only what you need from your table



![image](https://github.com/user-attachments/assets/30e9eef8-a7ca-4322-a595-598765758e88)

Step 1: Set Up and Configure AWS Lambda



Image Schema 

![image](https://github.com/user-attachments/assets/b0edcce3-1b3b-4c2b-bc64-f2212a3efaf4)


1. Log in to AWS Management Console
Navigate to the AWS Management Console.
Sign in with your AWS credentials.


3. Create a New Lambda Function
Navigate to the AWS Lambda Console:

![image](https://github.com/user-attachments/assets/24321dcc-3b24-4554-bd5e-9b94406b8dc2)


Go to the AWS Lambda Console.
Create a New Lambda Function:

Click on “Create function”.
Choose “Author from scratch”.
Function Name: Enter a descriptive name, e.g., UFCDataProcessor.
Runtime: Choose Python (select the version appropriate for your code).
Execution Role:
Select “Create a new role with basic Lambda permissions” if you don’t have an existing role.
For existing roles, choose “Use an existing role” and select the role with AWSLambdaBasicExecutionRole permissions. This role allows the Lambda function to write logs to CloudWatch.
Add a Layer for Pandas:

AWS Lambda does not include Pandas by default, so you need to add it as a layer.

Create a Pandas Layer:
Click on layers on your function overview or scroll down in your function view until you see it, you'll have to either select a layer or upload a zip package of your customized requirements to install.

![image](https://github.com/user-attachments/assets/2351a4a4-06ae-4056-b9aa-cb21c48d9f86)


Specify Layer, QWS Layer, Pandas-Python312
![image](https://github.com/user-attachments/assets/9e4e3a90-c134-47f4-85c3-3f2a8c02e764)

3. Configure Lambda Function 

You can upload your Lambda function code directly in the AWS Management Console or use the AWS CLI for deployment.

![image](https://github.com/user-attachments/assets/faee0259-c0b6-4e47-98af-69654db35990)


Make sure you write a test event either customize it or select from the templates, in this scenario we customized it 

![image](https://github.com/user-attachments/assets/538f0153-3f9c-4fd0-b4d2-fcc4118d83ef)

Set Timeout and Memory:
![image](https://github.com/user-attachments/assets/384caabd-dea2-49f4-b3ee-b1e3d7137436)

Timeout: Go to the configuration tab of your Lambda function under general configuration and set the timeout between 0 and 15 minutes based on your data processing needs. A typical setting might be 5 minutes.
Memory: Adjust the memory allocated to the function (e.g., 128 MB or more if necessary) to optimize performance.
Configure Environment Variables (if needed):

Set up environment variables to store configuration details, such as API keys.

4. Configure Api Gateway:
Make sure to configure your api gateway in a way that matches your request, here's where you'll add roles and APi keys if needed. 
 ![image](https://github.com/user-attachments/assets/00648043-75b6-4060-bf93-e9c5e1c19cb0)


6. Make the http request from your jupyter notebook or ide, make sure to allign your method and payload to what you configured on your api. gateway
