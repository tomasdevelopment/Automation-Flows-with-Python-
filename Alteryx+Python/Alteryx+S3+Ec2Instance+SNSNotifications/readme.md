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
check files for  to understand ec2 set up. 


4. Notifications
When a new file is detected in the S3 bucket, the EC2 instance publishes an SNS notification to the topic alteryxreview.
<img width="410" alt="CreatingSNSTopic" src="https://github.com/user-attachments/assets/d9df5183-cb7c-465f-8a28-b135bd8f9f07">

Suscribe to that topic  and confirm suscription via email 

![Suscriptionemail](https://github.com/user-attachments/assets/83efcca6-50a2-4867-b40b-66315c8f69fa)



Summary of  Commands for EC2 Setup and Workflow
This section summarizes the key  commands used to:

Transfer files from your PC to EC2.
Install Python dependencies.
Modify and configure the systemd service.
Test the application on port 80.
1. Transfer Files to EC2
You transferred the instance_script.py and requirements.txt files from your PC to the EC2 instance:



# Transfer Python script and requirements file to EC2
scp -i <your-key.pem> instance_script.py ec2-user@<EC2-public-IP>:/home/ec2-user/
scp -i <your-key.pem> requirements.txt ec2-user@<EC2-public-IP>:/home/ec2-user/
2. Install Python Dependencies
Once the files were on the EC2 instance, you installed the required Python packages:



# Activate the Python virtual environment if already created
source /home/ec2-user/.venv/bin/activate

# Install dependencies from requirements.txt
pip install -r /home/ec2-user/requirements.txt
If the virtual environment wasn’t created earlier, you initialized it:



# Create a Python virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
3. Configure the Systemd Service
You set up a systemd service to ensure the Python script runs continuously and listens on port 80.

Create/Modify the Service File:



sudo nano /etc/systemd/system/manual_instance.service
Service File Contents:

ini

[Unit]
Description=Run Manual Instance Python Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/ec2-user/instance_script.py
Restart=always
User=ec2-user
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
Reload systemd and Restart the Service:



# Reload the systemd daemon to register the updated service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable manual_instance.service

# Start the service
sudo systemctl start manual_instance.service
Check Service Status:



# Verify the service is running
sudo systemctl status manual_instance.service
4. Configure Python Script to Run on Port 80
To allow the Python script to bind to port 80 (a privileged port), you used authbind:

Install authbind:



sudo yum install authbind -y
Configure authbind for the Python executable:



sudo touch /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
sudo chown ec2-user /etc/authbind/byport/80
Modify the service file to use authbind:



ExecStart=/usr/bin/authbind --deep /usr/bin/python3 /home/ec2-user/instance_script.py
5. Test Application on Port 80
Verify the application is running on port 80:



curl http://127.0.0.1:80
Test external access:



curl http://<EC2-public-IP>
6. Key Commands for Debugging
View Logs for the Service:



sudo journalctl -u manual_instance.service
Restart the Service:



sudo systemctl restart manual_instance.service
Verify Active Processes:



ps aux | grep python
