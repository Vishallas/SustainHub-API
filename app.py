from flask import Flask,jsonify,request
import dotenv, data_handle
from bson.json_util import dumps

app = Flask(__name__)

dotenv.load_dotenv() # loading environment variables

# database connection
mongodb = data_handle.database() # creating a database obj
print("The database connected...")

@app.route('/get',methods=['POST',])
def find_something():
    
    food = request.json # converting the request json to dict

    data = mongodb.getData(food['food_name'])
    print(data)
    return dumps(data,indent = 2)

@app.route('/put', methods=['POST',])
def put_something():
    data = request.json
    status = mongodb.putData(data)
    return jsonify({'status':f'{status}'})


if(__name__ == '__main__'):
     
    # runs the app
    app.run(host='0.0.0.0',port=3000)
