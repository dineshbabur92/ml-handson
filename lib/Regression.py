
# coding: utf-8

# In[1]:

import numpy as np;
from scipy.optimize import fmin_bfgs;

class LogisticRegression:
    
    def __init__(self, X, y, lam):
        self.X = X;
#         print("in constructor, length of received arguement: ", y.shape)
        self.y = y;
        self.lam = lam;
        self.m = X.shape[0];
        self.n = X.shape[1];
        self.y = np.reshape(self.y, (self.m,1)); # need to check why this is happening
        self.X = LogisticRegression.addIntercept(self.X); # to be checked for documentation for how class name used in constructor
        self.theta = self.initializeTheta();
#         print("constructor",self.y.shape);
        
    def initializeTheta(self):
        return np.zeros((self.n + 1, 1));
    
    @staticmethod
    def addIntercept(X):
        m = X.shape[0];
        X = np.hstack((np.ones((m,1)), X));
        return X;
        
    @staticmethod
    def sigmoid(z):
        return 1 / (1 + np.exp(-1 * z));

    def buildModel(self):
        
        fminOutput = fmin_bfgs(
                            self.costFunction,
                            self.theta,
                            self.gradFunction,
                            disp=True,
                            maxiter=400,
                            full_output = True,
                            retall=True
                        );
        opTheta = fminOutput[0];
        opTheta = opTheta.reshape((self.n + 1, 1));
        return opTheta, fminOutput
        
    
        
    def costFunction(self, theta):
        
        theta = np.reshape(theta,(self.n + 1, 1));
        
        z = np.dot(self.X, theta);
        h = LogisticRegression.sigmoid(z);
#         print("cost function before",self.y.shape);
        J = np.add(
                np.multiply(
                    (1/self.m) 
                    , np.sum( 
                            np.subtract(
                                np.multiply(
                                    np.multiply(-1, self.y),
                                    np.log(h)
                                )
                                , np.multiply(
                                    np.subtract(1, self.y), 
                                    np.log(np.subtract(1, h))
                                )
                            )
                        )
                   )  
                , np.multiply(
                    (self.lam/self.m) 
                    , np.sum(
                        np.square(
                            np.vstack(
                                [0, theta[1:]]
                            )
                        )
                    ) 
                )
        );
#         print("cost function after",self.y.shape);
        return J;
    
    def gradFunction(self, theta):
        
#         print("grad function before",self.y.shape);
        theta = np.reshape(theta,(self.n + 1, 1));
        
#         print("grad function after reshaping",self.y.shape);
        z = np.dot(self.X, theta);
        h = LogisticRegression.sigmoid(z);
        
        grad = ( 
                    np.multiply(
                        (1/self.m) 
                        , (
                           np.dot(
                               np.transpose(self.X)
                                ,np.subtract(h, self.y)
                           )
                        )
                    )
                ) + \
                ( 
                    np.multiply(
                        (self.lam/self.m)
                        , np.vstack(
                            [0, theta[1:]]
                        )
                    )
                );
#         print("grad function after function formula",self.y.shape);
        grad = np.asarray(grad).reshape((self.n + 1,));
#         print("grad function after function formula and reshaping",self.y.shape);
        return grad;

