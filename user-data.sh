#!/bin/bash

sudo yum update

sudo yum install git -y

git clone https://github.com/Vishallas/SustainHub-API.git

cd SustainHub-API/

python3 -m venv venv

source venv/bin/activate

pip install pymongo flask python-dotenv

python app.py