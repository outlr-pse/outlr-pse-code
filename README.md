<div style="text-align:center; height: 50%">
  <img src="./Logo.png" style="width:25%; height:25%;"  alt="Outlr-Logo"/>
</div>

# PSE Implementation
This is the GitLab repository of group 2, "Outlr", for the subspace outlier detection project at the IPD Böhm institute.
It contains the implementation of the project. 

# How to deploy
1. Start the docker daemon
2. Go to the latest release. Under Assests > Other download the `Docker-Compose files`
3. Extract the files and go to the extracted folder
5. Set a strong `JWT_SECRET_KEY` in the `.env` file
4. Run the following command to start the app:
````sh
docker-compose up -d
````
5. Go to http://localhost:1337/
6. To stop the app run:
````sh
docker-compose down
````
