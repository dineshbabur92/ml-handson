
# coding: utf-8

# In[86]:

from pymongo import MongoClient
import pandas as pd
import json
from bson import ObjectId


    
db = MongoClient("localhost", 27017);
    
def getReviews():
    products = db.test.products.find({}, { "_id": 1, "name":1, "reviews.content": 1} );
    productsDf = pd.DataFrame(list(products));


    productsDf = pd.concat(
                [
                    pd.Series(
                        str(row["_id"]) + "|" + row["name"],
                        [
                            review["content"] for review in row["reviews"]
                        ]
                    ) for i, row in productsDf.iterrows()
                ]
            ).reset_index();


#     print(productsDf);
    productsDf.columns = ["Review", "_id"];

    _id_split =pd.DataFrame(productsDf["_id"].str.split("|").tolist());
    _id_split.columns = ["ReviewId", "ProductName"];
    _id_split.set_index("ReviewId");

    del productsDf["_id"];

    productsDf = pd.concat([_id_split, productsDf], axis = 1);
    productsDf = productsDf.set_index("ReviewId");
#     print(productsDf)
    return productsDf;

def putPredictions(predictions):
    updateProducts = {};
#     [['58e9ed6afa9e66228c077024', 'HTC', 'good phone', 'positive']]
    for row in predictions:
        productId = row[0];
        productReview = row[2];
        productReviewSentiment = row[3];
        
        if not productId in updateProducts:
            updateProducts[productId] = {}
            targetProduct = updateProducts[productId];
            
        if not "reviews" in targetProduct:
            targetProduct["reviews"] = []
            targetProductReviews = targetProduct["reviews"]
            
        targetProductReviews.append({"content" : productReview, "sentiment": productReviewSentiment});
#     print(updateProducts)
    for productId in updateProducts:
        db.test.products.update_one({'_id':ObjectId(productId)}, {"$set": {"reviews" : updateProducts[productId]["reviews"]}}, upsert=False)
    return updateProducts;
    
    
getReviews()
putPredictions([['58e9ed6afa9e66228c077024', 'HTC', 'good phone', 'positive']]);
    


# In[ ]:



