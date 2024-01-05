import pymongo, os, json, datetime
from bson import ObjectId

class database:
    def __init__(self):
        engine = pymongo.MongoClient(os.environ.get('DB_URL'))
        db = engine['test']

        self.clients = db['clients']
        self.products = db['products']

    # returns food data
    def getData(self,food_name):
        # add query here

        foods = list(self.products.find({"food_name":food_name})) # quering data

        return foods # returning data


    # inserts food data
    def putData(self,data):

        # Data segregation
        client_id = data['client_id'] # Getting client id
        prod = data['product'] # Getting food data

        # Adding creation data time 
        prod['created_time'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Inserting product
        prod_insert = self.products.insert_one(prod) # inserting food data

        # Converting to object id
        prod_id = ObjectId(prod_insert.inserted_id) 
        client_id = ObjectId(client_id)

        # Operation queries
        find_operation = {"_id":client_id} # finding clients for updation
        update_operation = {'$push': {"product_ids": prod_id}} # updating clients food ids

        # Updating the product array
        result = self.clients.update_one(find_operation, update_operation)
        print(result.acknowledged)
        return True

