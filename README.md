Machine Learning Accessibility Initiative (MLAI)

Instructions for running MLAI on a personal device 

## :gear:	 Install
#### :whale:	Docker
  [Get started with Docker for Windows](https://docs.docker.com/docker-for-windows/)

  [Install Docker Desktop on Mac](https://docs.docker.com/docker-for-mac/install/)

#### :large_orange_diamond:	Node.js
  [Download Node.Js](https://nodejs.org/en/download/)

#### Python flask dependencies:
  To Install all python dependencies navigate to the main project folder and run:

      pip3 install -r requirements.txt

Please note that the server and website need to be run on two seperate terminals (labeled inside this readme): 

## :arrow_forward: Run

  ### :leaves:	MongoDB 

  #### To install mongo and import all of current data into the database (make sure you are in the [docker folder](https://github.com/justinphan3110/MLAI-EECS393/tree/master/docker))    
      
      docker-compose up -d

 This command will start a MongoDB Image on localhost:27017

  #### To stop mongo  (make sure you are in the [docker folder](https://github.com/justinphan3110/MLAI-EECS393/tree/master/docker))
  ### Only run this after you want to stop the program.
      docker-compose down

  ### :inbox_tray:	Flask Python server (needs own terminal)

  Run the Flask Python REST API on localhost:5000. 

      python3 app.py

  ### :desktop_computer: React Website (needs own terminal)

  #### Make sure you are in the [templates/mlai folder](https://github.com/justinphan3110/MLAI-EECS393/tree/master/templates/mlai)

  ##### To install all the dependencies for the React App:

      npm install

  ##### Start the React App on localhost:3000:

      npm start

  Now check it on http://localhost:3000/

  ![image](https://user-images.githubusercontent.com/44376091/77139783-be8a9280-6a4d-11ea-8725-06ee3092521d.png)
  

  ### A sample username and password is:

     username: sadsad

     password: 123 

  ### Main Dashboard after log in sucessfully (Updated 3/20/2020)

  ![image](https://user-images.githubusercontent.com/44376091/77140059-aebf7e00-6a4e-11ea-822c-76951a385a5d.png)
  
  Once you are done running the program, press Ctrl + C in both the server terminal (where you ran python3 app.py) and the website terminal (where you ran npm start). Don't forget to go back to the start and go to the docker folder and do: 
  
        docker-compose down
        
As is stated in the docker part of this readme.
