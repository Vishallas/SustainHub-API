import pymongo, os, datetime
from bson import ObjectId

class database:
    def __init__(self):
        engine = pymongo.MongoClient(os.environ.get('ATLAS_URL'),)
        db = engine['sus-hub']

        self.clients = db['clients']
        self.products = db['products']

    # Searching food data
    def getData(self,food_name):

        # query for time 
        query = {
            "$and": [
                {"name": food_name},
                {"expire": {"$gt": datetime.datetime.now()}}
            ]
        }

        # query for search without time
        temp_query = {
            "$or":[
                {
                    "name": food_name
                },
                {
                    "name":{
                        "$regex":f"^{food_name}"
                    }
                }
            ]
        }
        
        # quering data
        res = self.products.find(temp_query)
        foods = list(res)
        client = self.clients.find({'_id':ObjectId()})
        # processing the object id and time for json
        for food in foods:
            food['_id'] = str(food['_id'])
            food['expire'] = str(food['expire'])
            food['user'] = self.clients.find_one({'_id':ObjectId(food['client_id'])})
        
        return foods # returning data

    # Inserting food data
    def putData(self,data):

        # Data segregation
        prod = data # Getting food data
        
        client_id = ObjectId(data['client_id'])

        # Inserting product
        prod_insert = self.products.insert_one(prod) # inserting food data

        # Converting to object id
        prod_id = ObjectId(prod_insert.inserted_id) 
        
        # Operation queries
        find_operation = {"_id":client_id} # findxing clients for updation
        update_operation = {"$push": {"product_ids": prod_id}} # updating clients food ids

        # Updating the product array
        result = self.clients.update_one(find_operation, update_operation)

        return prod_insert.inserted_id
    
    # Deleting food data
    def delData(self, prod_id,client_id):
        prod_id = ObjectId(prod_id)
        client_id = ObjectId(client_id)
        try:
            self.products.delete_one({"_id":prod_id})
            self.clients.update_one({"_id":client_id},{"$pull":{"product_ids":prod_id}})
            return True
        except:
            return False
        
    def getLatest(self):
        res = self.products.find().sort([('expire', -1)])

        foods = list(res)

        # processing the object id and time for json
        for food in foods:
            food['_id'] = str(food['_id'])
            food['expire'] = str(food['expire'])
        
        return foods # returning data
