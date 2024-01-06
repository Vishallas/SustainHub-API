#!/bin/bash

sudo yum update

sudo yum install git -y

git clone https://github.com/Vishallas/SustainHub-API.git

cd SustainHub-API/

python3 -m venv venv

export ATLAS_URL="mongodb+srv://vishal:Hello123@cluster0.j4ancvi.mongodb.net/?retryWrites=true&w=majority"

source venv/bin/activate

pip install pymongo flask python-dotenv

python app.py