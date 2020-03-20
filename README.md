Machine Learning Accessibility Initiative (MLAI)



## :gear:	 Install
#### :whale:	Docker
  [Get started with Docker for Windows](https://docs.docker.com/docker-for-windows/)
  
  [Install Docker Desktop on Mac](https://docs.docker.com/docker-for-mac/install/)
  
#### :large_orange_diamond:	Node.js
  [Download Node.Js](https://nodejs.org/en/download/)
  
#### Python flask dependencies: 
  To Install all python dependencies run: 
  
      pip3 install -r requirements.txt

## :arrow_forward: Run

  ### :leaves:	MongoDB
  
  #### To install mongo and import all of current data into the database (make sure you are in the [docker folder](https://github.com/justinphan3110/MLAI-EECS393/tree/master/docker))
  
      docker-compose up -d
      
 This command will start a MongoDB Image on localhost:27017
  
  #### To stop mongo  (make sure you are in the [docker folder](https://github.com/justinphan3110/MLAI-EECS393/tree/master/docker))
  
      docker-compose down
  
  ### :inbox_tray:	Flask Python server
    
  Run the Flask Python REST API on localhost:5000
  
      python3 app.py
      
  ### :desktop_computer: React Website
  
  #### Make sure you are in the [frontend/website/mlai folder](https://github.com/justinphan3110/MLAI-EECS393/tree/master/frontend/website/mlai)
  
  ##### To install all the dependencies for the React App:
  
      npm install
  
  ##### Start the React App on localhost:3000:
  
      npm start
   
  Now check it on http://localhost:3000/
  
  ![image](https://user-images.githubusercontent.com/44376091/77139783-be8a9280-6a4d-11ea-8725-06ee3092521d.png)

  ### Some sample username and password is :
    
     username: testing 
    
     password: 123
     
  ### Main Dashboard after log in sucessfully
  
  ![image](https://user-images.githubusercontent.com/44376091/77140059-aebf7e00-6a4e-11ea-822c-76951a385a5d.png)

    
