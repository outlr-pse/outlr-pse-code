<div style="text-align:center;">
  <img src="./Logo.svg" style="width:66%; height:66%;"  alt="Outlr-Logo"/>
</div>

# PSE Implementation

This is the GitLab repository of group 2, "Outlr", for the subspace outlier detection project at the IPD Böhm institute.
It contains the implementation of the project.

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