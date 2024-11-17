#!/bin/bash

# Exit immediately if any command fails
set -e

# --- Restrict Access to PEM File ---
icacls "C:\Users\tomsuare\Downloads\pgpcc-key1.pem" /inheritance:r
icacls "C:\Users\tomsuare\Downloads\pgpcc-key1.pem" /grant:r "%username%:F"

# --- SSH Into EC2 Instance ---
ssh -i "C:\Users\tomsuare\Downloads\pgpcc-key1.pem" ec2-user@54.89.116.229 <<EOF

    # --- Install Python ---
    sudo yum install python3 -y

    # --- Create and Edit a systemd Service File ---
    sudo tee /etc/systemd/system/manual_instance.service <<EOL
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
EOL

    # --- Enable and Start the Service ---
    sudo systemctl daemon-reload
    sudo systemctl enable manual_instance.service
    sudo systemctl start manual_instance.service

    # --- Check Service Status ---
    sudo systemctl status manual_instance.service

    # --- Install Python Dependencies ---
    pip3 install -r /home/ec2-user/requirements.txt

    # --- Test Application Locally ---
    curl http://localhost:8080 && echo "Local application running on port 8080."
EOF

# --- Transfer Files from Local Machine to EC2 ---
scp -i "C:\Users\tomsuare\Downloads\pgpcc-key1.pem" "C:\Users\tomsuare\Desktop\instance_script.py" ec2-user@54.89.116.229:~
scp -i "C:\Users\tomsuare\Downloads\pgpcc-key1.pem" "C:\Users\tomsuare\Desktop\requirements.txt" ec2-user@54.89.116.229:~

# --- Test Application Externally ---
curl http://52.201.246.151:8080 && echo "External application running on public IP port 8080."

# --- Publish SNS Notifications ---
aws sns publish --topic-arn arn:aws:sns:us-east-1:789873626066:alteryxreview --message "Test Message" --region us-east-1
