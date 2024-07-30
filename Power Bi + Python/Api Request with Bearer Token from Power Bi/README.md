One of the limitation when pulling api's from power bi is the lack of an Authorization header in the Http request parameters option from select from web,

<img width="545" alt="headerslimitations" src="https://github.com/user-attachments/assets/33aa4ea9-a277-474a-b4fe-a4c1f1d47142">



Python Get Data with Bearer Token Instructions:

Get Data, from other 
<img width="667" alt="Python Screen 1" src="https://github.com/user-attachments/assets/43406601-2572-405e-adc8-e8f0cfd10368">
Look for Python on the search bar
<img width="504" alt="Python Screen 2" src="https://github.com/user-attachments/assets/6d261c45-cbf1-4b04-977a-7958d8e3db82">
Write your Python Scrypt, make sure you have pip installed your  libraries first

<img width="528" alt="Python Screen 3" src="https://github.com/user-attachments/assets/7105e7b5-65be-49a4-8447-16cf638c47c6">

Mcode Instructions

1) Get data from a blank query
   
<img width="310" alt="Mcode Scrypt 1" src="https://github.com/user-attachments/assets/4918b373-681e-4db5-91b3-e6b0b4d25a0f">

2) Start the query steps using = Json.Document(Web.Contents()) Mcode formula
   
<img width="524" alt="Mcode Scrypt 2" src="https://github.com/user-attachments/assets/97dd6de3-3652-478e-be7d-d6061867c0a0">

3) Click on the lists you've pulled from your json formula which represent your api nested values
<img width="346" alt="Mcode Scrypt 3 cLOCK ON LISTS" src="https://github.com/user-attachments/assets/542ceb2d-7b76-4f0a-a0c1-7be1bb35716b">


4)Convert the API response into a table format, ensuring that any data fields separated by delimiters are properly split into individual columns. This process involves normalizing the JSON structure and handling delimiters to create a clean, structured dataset.


<img width="613" alt="Mcode Scrypt 4 Convert to table" src="https://github.com/user-attachments/assets/403c861c-a4ae-44a5-9c15-963c6bbcd735">


<img width="518" alt="Mcode Scrypt 5 sELECT dELIMITERS" src="https://github.com/user-attachments/assets/f24285d2-5413-4a4a-949f-61cd2c249fb2">

<img width="613" alt="Mcode Scrypt 4 Convert to table" src="https://github.com/user-attachments/assets/8439d4d7-5efa-4ceb-b924-c763227cc0b8">

Pro tip: Uncheck "Use original column as prefix" so you don't have to make as much modification on the namings for your visuals later on. Unless you want to specifically reference the table

<img width="253" alt="Mcode Scrypt 6 Uncheck use original column as prefix unless you want to referentiate the original table name" src="https://github.com/user-attachments/assets/2eccde8f-0d3f-43d1-817d-8bb09423461f">

5) Close and apply

<img width="853" alt="Mcode Scrypt 6 close and apply" src="https://github.com/user-attachments/assets/c0e7164e-b83e-464c-8cc2-1f882dfdee66">



Way 3, using api without required tokens:

Alternatively if your api does not require Headers, and your token api url looks like this, you are going to be able to skip all this steps and simply load from web,
only copy and paste the link is enough, but if you open your data source you'll notice you will be using basic open file as Json, then anonymous authentication.
URL Example:
https://yourserver.azureoraws.net/source/db/table?token=13token

<img width="523" alt="Screen 1 no bearer" src="https://github.com/user-attachments/assets/a64c62aa-ba04-420e-ad4c-a611c4c3b28d">


