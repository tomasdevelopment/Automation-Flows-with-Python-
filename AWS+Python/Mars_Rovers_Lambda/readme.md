

https://github.com/user-attachments/assets/beac190d-39ae-49ec-905d-a5c27ec6371a


Nasa Rovers AWS Event Bridge 


![FunctionOverview](https://github.com/user-attachments/assets/5bb6355f-4a34-4f6d-8f37-df7d0cbad1c5)


ttps://github.com/user-attachments/assets/d40bb25c-d6d2-4a83-920a-7e40d0a0bbae)

🚀 Contributing to Open Source with NASA Rover Data! 🚀

In a recent project, I leveraged the NASA Rovers open-source API to implement an ETL process. Here's a snapshot of the technical setup:

Data Retrieval & Transformation: Pulled data using the NASA API, transformed it with pandas, and stored it in an S3 bucket.
Scheduling & Access: Set up a daily data refresh with a cron job and enabled on-demand access via an API Gateway.
Security & Permissions: Configured IAM roles to grant Lambda functions S3 full control and used environment variables to manage the NASA API keys securely.
Monitoring: Utilized CloudWatch to monitor the ETL process, which had a timeout of 5 minutes. The CloudWatch report showed:
Request ID: 259c5cc6-375b-400d-9904-b19526daeb1d
Duration: 15,884.95 ms
Billed Duration: 15,885 ms
Memory Size: 128 MB
Max Memory Used: 124 MB
Init Duration: 2,221.76 ms
This project demonstrates how AWS serverless solutions simplify data aggregation and processing. I did it a 5-minute timeout (out of a 15-minute limit) but you could reduce it to try to control costs,
effective organization and monitoring allow for efficient data handling and transformation. 🌌💡

Check out the mission costs for the Mars rovers:
![Uploading LambdaFunctionIamroles.png…]()

Mars Science Lab (MLS): $2.9 billion
Mars Exploration Project (MEP): $1.2 billion
#DataEngineering #AWS #OpenSource #NASA #Serverless #ETL #DataTransformation #CloudComputing #Pandas #API #IAM #CloudWatch #Python #DataLake #S3
Values taken from: World Economic Forum Article : https://www.weforum.org/agenda/2021/02/mars-nasa-space-exploration-cost-perseverance-viking-curiosity/
Cron Expresion

![TriggeringWithCronexpression](https://github.com/user-attachments/assets/47ce1d12-b668-4d9e-ba24-bcedae944197)





Cloud Watch Image

![CloudWatch](https://github.com/user-attachments/assets/439b1830-8caf-48cb-ab00-73c8a487d528)


Test Event

![image](https://github.com/user-attachments/assets/fea74240-0839-42f9-9f16-ffb7166961a8)


Transformation Results 

![image](https://github.com/user-attachments/assets/d17f5f1d-7829-4ed8-8ed9-4fd60a4ca53d)


