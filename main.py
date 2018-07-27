import os, sys, talib
from Datafile import *
from sklearn.ensemble import RandomForestClassifier
path = r'C:\Users\ricwi\Documents\Projects\Project 5 - Best Sector\Data\\'

_timestamp = 0
_open = 1
_high = 2
_low = 3
_close = 4
_volume = 5

NO_DAYS_PER_SAMPLE = 10 #the days of historical data that goes into each sample
NO_PREDICTION_DAYS = 30 #the days ahead we're trying to predict the price of
NO_SAMPLES = 100 #the number of samples to train with

def createFeatures(i, data, NO_DAYS_PER_SAMPLE):
    x = []
    for symbol, sector in data:
        for row in range(i-NO_DAYS_PER_SAMPLE+1, i+1):
            if row > i:
                raise Exception("Lookahead")
            x.append(sector[row][_close])
    return x

def percentChange(start, end):
    start = float(start)
    end = float(end)
    return (end-start)/start

def signal(today, data):

    #Check for lookahead and make sure all arrays are the same length
    for symbol, sector in data:
        if len(sector) != len(data[0][1]):
            raise Exception("Unequal length")
        for row in sector:
            if row[0] > today:
                raise Exception("Lookahead")
    dataPoints = len(data[0][1])
    requiredDataPoints = NO_SAMPLES
    if dataPoints < requiredDataPoints:
        return 'need more data'
    
    #construct features matrix
    X = []
    Y = []
    for i in range(NO_DAYS_PER_SAMPLE, len(data[0][1])-NO_PREDICTION_DAYS):
        #independent variable, input
        x = createFeatures(i, data, NO_DAYS_PER_SAMPLE)

        #dependent variable, best performing sector
        futureMax = percentChange(data[0][1][i][_close], data[0][1][i+NO_PREDICTION_DAYS][_close])
        y = data[0][0]
        for symbol, sector in data:
            if percentChange(sector[i][_close], sector[i+NO_PREDICTION_DAYS][_close]) > futureMax:
                y = symbol

        X.append(x)
        Y.append(y)
    clf = RandomForestClassifier(n_estimators = 100)
    clf.fit(X, Y)

    xPrediction = createFeatures(dataPoints - 1, data, NO_DAYS_PER_SAMPLE)
    xPrediction = np.reshape(xPrediction, (1, len(xPrediction)))
    yPrediction = clf.predict(xPrediction)
    return yPrediction
            
        
#signal is called after the markets close on date = today

files = [Datafile(str(path) + x) for x in os.listdir(path)]

#find min date
minDate = files[0].array[0][_timestamp]
maxDate = minDate
for sector in files:
    if sector.array[0][0] > minDate:
        minDate = sector.array[0][_timestamp]
    if sector.array[-1][0] > maxDate:
        maxDate = sector.array[-1][_timestamp]

today = minDate
predictions = []
binaryAccuracy = []
while True:
    
    print("Today: " + str(today))
    
    #Make sure all sectors trade
    doesNotTrade = False
    for sector in files:
        if sector.getToday(today) == 'does not trade':
            doesNotTrade = True
    if doesNotTrade:
        print("One sector does not trade")
        print()
        today += datetime.timedelta(days = 1)
        continue

    

    #Prepare data to pass to signal()
    data = []
    for sector in files:
        data.append((sector.name, sector.array[0:sector.getToday(today) + 1]))
    minLength = min([len(sector) for name, sector in data])
    data = [(name, sector[-minLength:]) for name, sector in data]

    #Check existing predictions
    for i in range(len(predictions)):
        predictions[i][1] += 1 #add a day to the number of trading days since the prediction
        if predictions[i][1] == NO_PREDICTION_DAYS:
            #check the prediction
            bestSector = data[0][0]
            bestSectorPerformance = percentChange(data[0][1][-NO_PREDICTION_DAYS][_close], data[0][1][-1][_close])
            for symbol, sector in data:
                sectorPerformance = percentChange(sector[-NO_PREDICTION_DAYS][_close], sector[-1][_close])
                if sectorPerformance > bestSectorPerformance:
                    bestSector = symbol
                    bestSectorPerformance = sectorPerformance

            if bestSector == predictions[i][0]:
                binaryAccuracy.append(1)
            else:
                binaryAccuracy.append(0)
            accuracy = float(sum(binaryAccuracy))/float(len(binaryAccuracy))
            print("Prediction: " + str(predictions[i][0]) + "   Actual: " + bestSector)
            print("Accuracy: " + str(accuracy))
                    
    prediction = signal(today, data)
    if prediction != 'need more data':
        predictions.append([prediction, 0])




    
    today += datetime.timedelta(days = 1)
    print()

