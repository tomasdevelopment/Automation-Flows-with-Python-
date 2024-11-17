Workflow Description
This project demonstrates a hybrid data processing pipeline where:

Alteryx Designer is used on an on-premises PC for data transformation and selection of the top 3 rows based on sorted criteria.
The results are saved locally on the desktop and uploaded to AWS S3.
An EC2 instance monitors the S3 bucket and triggers SNS notifications when new files are uploaded.
Step-by-Step Instructions
1. Process Data with Alteryx
Load Data:
Use the Input Tool in Alteryx to load your dataset (e.g., CSV or Excel file) from your PC.
Sort Data:


<img width="757" alt="SortActionAlteryx" src="https://github.com/user-attachments/assets/3875890b-39a6-4b9f-825e-4a637744e32a">



Use the Sort Tool to arrange the data by the desired column (e.g., CO2 emissions).
Choose ascending or descending order, depending on your analysis.


Select Top 10 Rows:
Use the Sample Tool.
Set it to "First N Rows" and input 3 to retrieve the top 3 rows from the sorted data.

![image](https://github.com/user-attachments/assets/0c36669c-79ea-40af-b671-7bc34c71cc4f)

Save the Output:
Use the Output Data Tool to save the transformed data:
Save locally: Select your Desktop or a specific folder (e.g., C:\Users\<YourName>\Desktop\co2analytics.csv).
![image](https://github.com/user-attachments/assets/f7ebd59a-7d03-4cb6-8574-153be5ed967f)

Use the Python Tool to upload the file to S3:

![image](https://github.com/user-attachments/assets/6385949d-63a3-4218-a034-d6ec0df434a1)



2. Monitor S3 Bucket with EC2
The EC2 instance runs a Python script to monitor the S3 bucket (alteryxetl) and trigger notifications via SNS when new files are uploaded.
check files for bash to understand ec2 set up. 


4. Notifications
When a new file is detected in the S3 bucket, the EC2 instance publishes an SNS notification to the topic alteryxreview.
<img width="410" alt="CreatingSNSTopic" src="https://github.com/user-attachments/assets/d9df5183-cb7c-465f-8a28-b135bd8f9f07">

Suscribe to that topic  and confirm suscription via email 

![Suscriptionemail](https://github.com/user-attachments/assets/83efcca6-50a2-4867-b40b-66315c8f69fa)

