
# coding: utf-8

# In[4]:

from pymongo import MongoClient
import pandas as pd
import json

def getNewReviews():
    
    db = MongoClient("localhost", 27017);
    collection = "products";
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


    productsDf.columns = ["Review", "_id"];

    _id_split =pd.DataFrame(productsDf["_id"].str.split("|").tolist());
    _id_split.columns = ["ReviewId", "ProductName"];
    _id_split.set_index("ReviewId");

    del productsDf["_id"];

    productsDf = pd.concat([_id_split, productsDf], axis = 1);
    productsDf = productsDf.set_index("ReviewId");
    
    return productsDf;


# In[ ]:



