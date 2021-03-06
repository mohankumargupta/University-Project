import re
from collections import Counter, defaultdict
from horse_parser_no_handicaps import HorseParserNoHandicaps
from race_parser_no_handicaps import RaceParserNoHandicaps

''' Computes the number of races in the dataset for which the dataset contains the records of all participating horses '''
def no_of_races_with_all_horses(races):
    total_races = 0
    
    for r in races:
        if len(races[r].horses) == races[r].no_of_runners:
            total_races += 1
    
    return total_races

''' Computes the number of races in the dataset for which the dataset contains the record of the winning horse '''
def no_of_races_with_winner(races, horses):
    total_races = 0
    
    for r in races:
        if races[r].winner and horses[races[r].winner]:
            total_races += 1

    return total_races

''' Computes the average number of races per horse within the dataset '''
def average_no_of_races_per_horse(horses):
    total_races = 0

    for h in horses:
        total_races += len(horses[h].races)

    average_races = float(total_races)/len(horses)
    return average_races


''' Returns the races which contain the records of all horses in the dataset '''
def get_full_races(races):
    full_races = {}
    
    for r in races:
        if len(races[r].horses) == races[r].no_of_runners:
            full_races[races[r].race_key] = races[r]

    return full_races


''' Computes the ages of horses in races where all horse records are present in the dataset '''
def get_ages(full_races):
    ages = set()

    for r in full_races:
        for h in full_races[r].horses:
            ages.add(h.age)

    return ages

''' Computes the number of races for horses at each age. Only takes into account those races which have all runners '''
def races_at_each_age(full_races, ages_set):
    no_of_races_per_age = Counter()
    
    for a in ages_set:
        total_races = 0
        for r in full_races:
            ages = [h.age for h in full_races[r].horses]
            if max(ages) == a:
                total_races += 1
        no_of_races_per_age[a] = total_races

    return no_of_races_per_age

''' Computes the number of races with k missing horses in the dataset  '''
def races_with_k_missing_runners(races):
    races_with_missing_horses = Counter()

    for r in races:
        missing_runners = races[r].no_of_runners - len(races[r].horses)
        races_with_missing_horses[missing_runners] += 1

    return races_with_missing_horses

''' Computes the frequency of races with k horses participating '''
def races_with_k_runners(races):
    races_with_k_horses = Counter()

    for r in races:
        races_with_k_horses[races[r].no_of_runners] += 1
    
    return races_with_k_horses

''' Computes the number of races which contain the information for the winning horse '''
def races_with_winning_horse(races):
    races_with_winner = 0

    for r in races:
        for h in races[r].horses:
            if races[r].winner == h.horse_key:
                races_with_winner += 1

    return races_with_winner

''' Computes the number of distinct trainers in the dataset '''
def no_of_trainers(horses):
    trainers = set()

    for h in horses:
        for r in horses[h].races:
            trainers.add(r.horse_trainer)

    return len(trainers)

''' Computes the number of distinct jockeys in the dataset '''
def no_of_jockeys(horses):
    jockeys = set()

    for h in horses:
        for r in horses[h].races:
            jockeys.add(r.horse_jockey)

    return len(jockeys)

''' Computes the average horse speed on each going type '''
def going_average_speeds(races):
    going = defaultdict(list)
    averages = defaultdict()

    for r in races:
        for h in races[r].horses:
            going[races[r].going].append(h.speed)

    for g in going:
        total_speed = sum([x for x in going[g]])
        number = len(going[g])
        averages[g] = float(total_speed)/number
        total_speed = 0.0
        number = 0

    print averages

''' Computes the average horse speed in each race class '''
def class_average_speeds(races):
    race_class = defaultdict(list)
    averages = defaultdict()

    for r in races:
        for h in races[r].horses:
            race_class[races[r].race_class].append(h.speed)

    for rc in race_class:
        total_speed = sum([x for x in race_class[rc]])
        number = len(race_class[rc])
        averages[rc] = float(total_speed)/number
        total_speed = 0.0
        number = 0

    print averages

''' Computes the average race distance in each race class '''
def class_average_distances(races):
    race_class = defaultdict(list)
    averages = defaultdict()

    for r in races:
        race_class[races[r].race_class].append(races[r].distance)

    for rc in race_class:
        total_distance = sum([x for x in race_class[rc]])
        number = len(race_class[rc])
        averages[rc] = float(total_distance)/number
        total_distance = 0.0
        number = 0

    print averages

''' Computes the average prize money in each race class '''
def class_average_prizes(races):
    race_class = defaultdict(list)
    averages = defaultdict()

    for r in races:
        race_class[races[r].race_class].append(races[r].prize)

    for rc in race_class:
        total_prize = sum([x for x in race_class[rc]])
        number = len(race_class[rc])
        averages[rc] = float(total_prize)/number
        total_prize = 0.0
        number = 0

    print averages

def main():
    horse_parser_98 = HorseParserNoHandicaps('./../Data/born98.csv')
    horse_parser_05 = HorseParserNoHandicaps('./../Data/born05.csv')

    race_parser_98 = RaceParserNoHandicaps('./../Data/born98.csv')
    race_parser_05 = RaceParserNoHandicaps('./../Data/born05.csv')

    horses98 = horse_parser_98.horses
    horses05 = horse_parser_05.horses

    races98 = race_parser_98.races
    races05 = race_parser_05.races

    full_races_98 = get_full_races(races98)
    full_races_05 = get_full_races(races05)

    total_races_with_all_horses_98 = no_of_races_with_all_horses(races98)
    total_races_with_winners_98 = races_with_winning_horse(races98)

    total_races_with_all_horses_05 = no_of_races_with_all_horses(races05)
    total_races_with_winners_05 = races_with_winning_horse(races05)

    average_races_per_horse_98 = average_no_of_races_per_horse(horses98)
    average_races_per_horse_05 = average_no_of_races_per_horse(horses05)

    ages98 = get_ages(full_races_98)
    ages05 = get_ages(full_races_05)

    no_of_races_per_age_98 = races_at_each_age(full_races_98, ages98)
    no_of_races_per_age_05 = races_at_each_age(full_races_05, ages05)

    races_with_k_missing_horses_98 = races_with_k_missing_runners(races98)
    races_with_k_missing_horses_05 = races_with_k_missing_runners(races05)

    print 'born98.csv file statistics - without handicap races:'
    print 'No. of horses: ' + str(len(horses98))
    print 'No. of races: ' + str(len(races98))
    print 'No. of races for which we have all the horses: ' + str(total_races_with_all_horses_98)
    print 'No. of races for which we have the winner: ' + str(total_races_with_winners_98)
    print 'Fraction of races for which we have all the horses: ' + str(float(total_races_with_all_horses_98)/len(races98))
    print 'Fraction of races for which we have the winner: ' + str(float(total_races_with_winners_98)/len(races98))
    print 'Average no. of races per horse: ' + str(average_races_per_horse_98)
    print 'No. of races for horses at each age: ' + str(no_of_races_per_age_98)
    print 'No. of races with k-missing horse records: ' + str(races_with_k_missing_horses_98)
    print 'No. of different trainers: ' + str(no_of_trainers(horses98))
    print 'No. of different jockeys: ' + str(no_of_jockeys(horses98))
    print 'Going and Speed: '
    going_average_speeds(races98)
    print 'Race Class and Speed:'
    class_average_speeds(races98)
    print 'Race Class and Distance:'
    class_average_distances(races98)
    print 'Race Class and Prize:'
    class_average_prizes(races98)


    print ''

    print 'born05.csv file statistics - without handicap races:'
    print 'No. of horses: ' + str(len(horses05))
    print 'No. of races: ' + str(len(races05))
    print 'No. of races for which we have all the horses: ' + str(total_races_with_all_horses_05)
    print 'No. of races for which we have the winner: ' + str(total_races_with_winners_05)
    print 'Fraction of races for which we have all the horses: ' + str(float(total_races_with_all_horses_05)/len(races05))
    print 'Fraction of races for which we have the winner: ' + str(float(total_races_with_winners_05)/len(races05))
    print 'Average no. of races per horse: ' + str(average_races_per_horse_05)
    print 'No. of races for horses at each age: ' + str(no_of_races_per_age_05)
    print 'No. of races with k-missing horse records: ' + str(races_with_k_missing_horses_05)
    print 'No. of different trainers: ' + str(no_of_trainers(horses05))
    print 'No. of different jockeys: ' + str(no_of_jockeys(horses05))
    print 'Going and Speed: '
    going_average_speeds(races05)
    print 'Race Class and Speed:'
    class_average_speeds(races05)
    print 'Race Class and Distance:'
    class_average_distances(races05)
    print 'Race Class and Prize:'
    class_average_prizes(races05)


if __name__ == "__main__":
    main()