GENERAL SCHEMA 


![Data Schema](https://raw.githubusercontent.com/tomasdevelopment/Automation-Flows-with-Python-/main/Power%20Bi%20%2B%20Python/Api%20Request%20with%20Bearer%20Token%20from%20Power%20Bi/data_schema_powerbidb.jpg)




One of the limitations when pulling APIs from Power BI is the lack of an Authorization header in the HTTP request parameters option when selecting data from the web.

<img width="545" alt="headerslimitations" src="https://github.com/user-attachments/assets/33aa4ea9-a277-474a-b4fe-a4c1f1d47142">




**Python Get Data with Bearer Token Instructions:**


1) Get Data, from other


<img width="667" alt="Python Screen 1" src="https://github.com/user-attachments/assets/43406601-2572-405e-adc8-e8f0cfd10368">

2) Look for Python on the search bar


<img width="504" alt="Python Screen 2" src="https://github.com/user-attachments/assets/6d261c45-cbf1-4b04-977a-7958d8e3db82">

3) Write your Python Script, make sure you have pip installed your libraries first and use only libraries available in power bi. 

<img width="528" alt="Python Screen 3" src="https://github.com/user-attachments/assets/7105e7b5-65be-49a4-8447-16cf638c47c6">

4) Expand your data frame and navigate to it, Pro tip: Uncheck "Use original column as prefix" so you don't have to make as much modification on the naming for your visuals later on. Unless you want to specifically reference the table

You will find your DF with the name you gave it on the scrypt


<img width="182" alt="Python Screen 4 dATA mANIPULATION" src="https://github.com/user-attachments/assets/9aea57d5-610e-43e1-9aca-28b2ef3ed4d4">

Click on the arrows on the value headers to expand it


<img width="831" alt="Python Screen 4 dATA NAVIGATION" src="https://github.com/user-attachments/assets/6a6f43a1-06de-470e-9fb2-53287853d5d7">

Close and load.



**Mcode Instructions**

Get data from a blank query


<img width="310" alt="Mcode Scrypt 1" src="https://github.com/user-attachments/assets/4918b373-681e-4db5-91b3-e6b0b4d25a0f">




Start the query steps using Json.Document(Web.Contents()) Mcode formula
<img width="524" alt="Mcode Scrypt 2" src="https://github.com/user-attachments/assets/97dd6de3-3652-478e-be7d-d6061867c0a0">



Click on the lists you've pulled from your JSON formula which represent your API nested values

<img width="346" alt="Mcode Scrypt 3 cLOCK ON LISTS" src="https://github.com/user-attachments/assets/542ceb2d-7b76-4f0a-a0c1-7be1bb35716b">


Convert the API response into a table format, ensuring that any data fields separated by delimiters are properly split into individual columns. This process involves normalizing the JSON structure and handling delimiters to create a clean, structured dataset.

<img width="613" alt="Mcode Scrypt 4 Convert to table" src="https://github.com/user-attachments/assets/403c861c-a4ae-44a5-9c15-963c6bbcd735">

<img width="518" alt="Mcode Scrypt 5 sELECT dELIMITERS" src="https://github.com/user-attachments/assets/f24285d2-5413-4a4a-949f-61cd2c249fb2">

<img width="613" alt="Mcode Scrypt 4 Convert to table" src="https://github.com/user-attachments/assets/8439d4d7-5efa-4ceb-b924-c763227cc0b8">


Pro tip: Uncheck "Use original column as prefix" so you don't have to make as much modification on the naming for your visuals later on. Unless you want to specifically reference the table

<img width="253" alt="Mcode Scrypt 6 Uncheck use original column as prefix unless you want to referentiate the original table name" src="https://github.com/user-attachments/assets/2eccde8f-0d3f-43d1-817d-8bb09423461f">



Close and apply


<img width="853" alt="Mcode Scrypt 6 close and apply" src="https://github.com/user-attachments/assets/c0e7164e-b83e-464c-8cc2-1f882dfdee66">



**Way 3, using API without required tokens:**



Alternatively, if your API does not require Headers, and your token API URL looks like this, you are going to be able to skip all these steps and simply load from the web. Only copy and paste the link is enough, but if you open your data source, you'll notice you will be using basic open file as JSON, then anonymous authentication.

URL Example:
https://yourserver.azureoraws.net/source/db/table?token=13token

<img width="523" alt="Screen 1 no bearer" src="https://github.com/user-attachments/assets/a64c62aa-ba04-420e-ad4c-a611c4c3b28d">



Add here the limitation of Python: 250 thousand rows, queries that take longer than 30 minutes will time out, and refine the article. Be very careful not to modify image links.





