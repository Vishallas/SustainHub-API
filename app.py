from flask import Flask,jsonify,request
import dotenv, data_handle
from bson.json_util import dumps

app = Flask(__name__)

dotenv.load_dotenv() # loading environment variables

# database connection
mongodb = data_handle.database() # creating a database obj
print("The database connected...")


@app.route('/get',methods=['GET',])
def find_something():
    food_name = request.args['food_name']
    data = mongodb.getData(food_name) 
    return dumps(data,indent = 2)

@app.route('/feed',methods=['GET',])
def get_latest():
    return jsonify(mongodb.getLatest())


@app.route('/put', methods=['POST',])
def put_something():
    data = request.json
    status = mongodb.putData(data)
    return jsonify({'prod_id':f'{status}'})


@app.route('/delete',methods=['DELETE',])
def delete_something():
    client_id = request.args['client_id']
    prod_id = request.args['product_id']
    status = mongodb.delData(prod_id, client_id)
    return jsonify({'status':f'{status}'}) 

if(__name__ == '__main__'):
     
    # runs the app
    app.run(host='0.0.0.0',port=3000)
