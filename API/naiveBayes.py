from sklearn.naive_bayes import GaussianNB
import numpy as np

#months = features, rates = labels
def trainModel(months, rates):
    model = GaussianNB()
    model.fit(np.array(months).reshape(-1,1), np.array(rates))
    return model
    
#Predict what the rate will be based on current date
def makePrediction(model, month):
    predictedRate = model.predict([[month]])
    return predictedRate
