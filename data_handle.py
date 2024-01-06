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

        # processing the object id and time for json
        for food in foods:
            food['_id'] = str(food['_id'])
            food['expire'] = str(food['expire'])
        
        return foods # returning data

    # Inserting food data
    def putData(self,data):

        # Data segregation
        client_id = data['client_id'] # Getting client id
        prod = data['product'] # Getting food data

        # Adding creation data time 
        # prod['expire'] = datetime.timedelta(hours=data['expire'])+datetime.datetime.now()

        # Inserting product
        prod_insert = self.products.insert_one(prod) # inserting food data

        # Converting to object id
        prod_id = ObjectId(prod_insert.inserted_id) 
        client_id = ObjectId(client_id)

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
    
    
