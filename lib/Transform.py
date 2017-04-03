
# coding: utf-8

# In[4]:

import pandas as pd;

class GenTransform:
    
    def __init__(self):
        return;
    
    @staticmethod
    def generateBooleanColumns(df, columns):
        for column in columns:
                df[column] = -1 * df[column].isnull() + 1
        return df;
    
    @staticmethod
    def generateValueColumns(df, columns):
        for column in columns:
            df = pd.concat([df.drop(column, axis=1), df[column].str.get_dummies()], axis = 1);
        return df;
    
    @staticmethod
    def removeNonFeatures(df, columns):
        for column in columns:
            df = df.drop(column, axis = 1);
        return df;
    
    @staticmethod
    def fillNaWithMean(df):
        return df.fillna(df.mean());
    
    @staticmethod
    def dataTransform(df, listRowstoColumns, listRowsToBoolean, listNonFeatures):
        df1 = GenTransform.generateBooleanColumns(df, listRowsToBoolean);
        df2 = GenTransform.removeNonFeatures(df, listNonFeatures);
        df3 = GenTransform.generateValueColumns(df2, listRowstoColumns);
        df4 = GenTransform.fillNaWithMean(df3);
        return(df4);

