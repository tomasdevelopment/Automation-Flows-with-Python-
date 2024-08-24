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

Mars Science Lab (MLS): $2.9 billion
Mars Exploration Project (MEP): $1.2 billion
#DataEngineering #AWS #OpenSource #NASA #Serverless #ETL #DataTransformation #CloudComputing #Pandas #API #IAM #CloudWatch #Python #DataLake #S3

