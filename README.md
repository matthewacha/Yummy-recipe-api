# Yummy-recipe-api
[![Build Status](https://travis-ci.org/matthewacha/Yummy-recipe-api.svg?branch=developer)](https://travis-ci.org/matthewacha/Yummy-recipe-api)
API for your recipes
Introduction
============

1.Environment setup
===================
We shall assume that you have downloaded and installed python

-Clone the repository from https://github.com/matthewacha/Yummy-recipe-api.git

-set up and activate virtual environment in the repo root folder

$virtualenv renv

-download and install pip from pypip

-install the dependencies

$pip install -r requirements.txt

2.Run tests
===========
-Using coverage

$coverage run tests.py -v

-Using py.test

$py.test tests.py -v

2.running app
=============
To run app

-python run.py 
  
3.Test api using postman
========================
After launching app from command line;

Launch postman from a browser or desktop

use the following endpoints and methods

To add new user- 
  
  endpoint = http://127.0.0.1:5000/api/user
  
  method= POST
  
  Body = {"first_name":"<your_name>",
          "last_name":"<your_name>",
          "email":"<your_email>",
          "password":"<password>"}
  
To get users
  
  endpoint = http://127.0.0.1:5000/api/user
  
  method= GET
  
To get a single user
  
  endpoint = http://127.0.0.1:5000/api/user/"<email>"
  
  method= GET
  
To login user
  
  endpoint = http://127.0.0.1:5000/login
  
  method= POST
  
  Body={"email":"<your_email>", 
        "password":"your_password"}
  
To add recipe
  
  endpoint = http://127.0.0.1:5000/api/recipe
  
  method= POST
  
  Body={"name":"<recipe_name>",
        "description":"<recipe_description>"}
  
To view recipes
  
  endpoint = http://127.0.0.1:5000/api/recipe
  
  method= GET
  
To view single recipe
  
  endpoint = http://127.0.0.1:5000/api/recipe/"<name>"
  
  method= POST
  
  Body={"name":"Recipe_name"}
  
To edit single recipe
  
  endpoint = http://127.0.0.1:5000/api/recipe/"<name>"
  
  method= PUT
  
  Body={"name":"recipe_name",
        "new_name":"<edited_name>",
        "new_description":"<edited_description>"}
  
To delete recipe
  
  endpoint = http://127.0.0.1:5000/api/recipe/"<name>"
  
  method= DELETE


