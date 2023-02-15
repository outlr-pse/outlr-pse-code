<div style="text-align:center; height: 50%">
  <img src="./Logo.png" style="width:25%; height:25%;"  alt="Outlr-Logo"/>
</div>

# PSE Implementation

This is the GitLab repository of group 2, "Outlr", for the subspace outlier detection project at the IPD Böhm institute.
It contains the implementation of the project. 

Unfortunately, deployment is not finished. To try the web application, please install PostgreSQL and Python 3.10 and Vue (npm with nodejs). Install python packages in backend/requirements.txt and run npm install in the frontend folder. 
After setting up PostgreSQL create config.ini file and replace the url, with your PostgreSQL settings:
```
[jwt]
secret_key = secret

[database]
url = postgresql://postgres:123@localhost:5432/outlr
```
Afterwards start the PostgresSQL server, and create a database outlr, and run init.py in the backend.
Finally, you can run npm run dev in the pse-implementation/frontend directory.

# How to deploy
The project is deployed using Docker. To deploy the project, you need to have Docker installed on your machine.
To deploy the project, run the following command in the root directory of the project:
````commandline
    docker-compose up --build
````
This will create three containers:
- The database container
- The backend container
- The frontend container

You can access the frontend at http://localhost:1337 and the backend at http://localhost:1337/api/.

To stop the containers and delete all tables, run the following command in the root directory of the project:
````commandline
    docker-compose down -v
````
