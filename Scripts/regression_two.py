import numpy as np
import pylab as pl
import random
from race_parser_no_handicaps import RaceParserNoHandicaps
from horse_parser_no_handicaps import HorseParserNoHandicaps
from utilities import split_dataset
from sklearn import linear_model

''' Regression Experiment 2: Basic prediction with lifetime features using the random race (between race 4 and second-last race) as next race '''

def compute_vector(horse):
    vector = []
    sorted_races = sorted(horse.races, key=lambda x:x.date, reverse=False)

    # Determine the next race of the horse between 4 and the second last race
    next_race_number = random.randint(3, len(sorted_races)-2)
    speed_in_next_race = sorted_races[next_race_number].horse_speed

    # Compute and append lifetime features
    average_speed = 0.0
    average_rating = 0.0
    average_odds = 0.0
    average_prize_money = 0.0
    average_distance = 0.0
    
    for r in sorted_races[:next_race_number]:
        average_speed += r.horse_speed
        average_rating += r.horse_rating
        average_odds += r.horse_odds
        average_distance += r.distance
        average_prize_money += r.prize

    vector.append(average_speed)
    vector.append(average_rating)
    vector.append(average_odds)
    vector.append(average_prize_money)
    vector.append(average_distance)
    
    no_of_races = len(sorted_races[:next_race_number])
    vector = [a/no_of_races for a in vector]
    return vector, speed_in_next_race

def main():
    horses98 = HorseParserNoHandicaps('./../Data/born98.csv').horses
    horses05 = HorseParserNoHandicaps('./../Data/born05.csv').horses

    races98 = RaceParserNoHandicaps('./../Data/born98.csv').races
    races05 = RaceParserNoHandicaps('./../Data/born05.csv').races

    ''' HorsesBorn98 Dataset '''
    horses_train_98, horses_test_98 = split_dataset(horses98)

    horses_98_X_train = []
    horses_98_y_train = []
    for h in horses_train_98:
        v,s = compute_vector(h)
        horses_98_X_train.append(v)
        horses_98_y_train .append(s)

    print 'No. of instances in training set:'
    print len(horses_98_X_train)
    print len(horses_98_y_train)
    print ''

    horses_98_X_test = []
    horses_98_y_test = []
    for h in horses_test_98:
        v,s = compute_vector(h)
        horses_98_X_test.append(v)
        horses_98_y_test.append(s)

    print 'No. of instances in testing set:'
    print len(horses_98_X_test)
    print len(horses_98_y_test)
    print ''
    
    # Create linear regression object
    regr98 = linear_model.LinearRegression()

    # Train the model using the training sets
    regr98.fit(horses_98_X_train, horses_98_y_train)

    # Coefficients
    print 'Coefficients:'
    print regr98.coef_
    print ''

    # Mean square error
    print 'Residual sum of squares:' 
    print np.mean((regr98.predict(horses_98_X_test) - horses_98_y_test) ** 2)
    print ''

    # Explained variance score: 1 is perfect prediction
    print 'Variance score:'
    print regr98.score(horses_98_X_test, horses_98_y_test)
    print ''

    print 'Mean absolute error:'
    print mean_absolute_error((regr98.predict(horses_98_X_test)), horses_98_y_test)
    print ''   


    ''' HorsesBorn05 Dataset '''
    horses_train_05, horses_test_05 = split_dataset(horses05)

    horses_05_X_train = []
    horses_05_y_train = []
    for h in horses_train_05:
        v,s = compute_vector(h)
        horses_05_X_train.append(v)
        horses_05_y_train .append(s)

    print 'No. of instances in training set:'
    print len(horses_05_X_train)
    print len(horses_05_y_train)
    print ''

    horses_05_X_test = []
    horses_05_y_test = []
    for h in horses_test_05:
        v,s = compute_vector(h)
        horses_05_X_test.append(v)
        horses_05_y_test.append(s)

    print 'No. of instances in testing set:'
    print len(horses_05_X_test)
    print len(horses_05_y_test)
    print ''
    
    # Create linear regression object
    regr05 = linear_model.LinearRegression()

    # Train the model using the training sets
    regr05.fit(horses_05_X_train, horses_05_y_train)

    # Coefficients
    print 'Coefficients:'
    print regr05.coef_
    print ''

    # Mean square error
    print 'Residual sum of squares:' 
    print np.mean((regr05.predict(horses_05_X_test) - horses_05_y_test) ** 2)
    print ''

    # Explained variance score: 1 is perfect prediction
    print 'Variance score:'
    print regr05.score(horses_05_X_test, horses_05_y_test)
    print ''

    print 'Mean absolute error:'
    print mean_absolute_error((regr05.predict(horses_05_X_test)), horses_05_y_test)
    print ''    
        




if __name__ == "__main__":
    main()