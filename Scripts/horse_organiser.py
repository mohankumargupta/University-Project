import matplotlib.pyplot as plt

from collections import Counter
from horse_parser import HorseParser 
from race_parser import RaceParser 

class Race:
    def __init__(self, race_hash, race_track, race_date, race_time, race_name, race_prize, race_restrictions, no_of_runners, going, race_class, race_distance, horse_place, horse_age, weight_carried, jockey_name, jockeys_claim, trainer, horse_odds, horse_speed, winning_horse):
        self.race_hash = race_hash
        self.track = race_track
        self.date = race_date
        self.time = race_time
        self.name = race_name
        self.prize = race_prize
        self.restrictions = race_restrictions
        self.no_of_runners = no_of_runners
        self.going = going
        self.race_class = race_class
        self.distance = race_distance
        self.horse_place = horse_place
        self.horse_age = horse_age
        self.weight_carried = weight_carried
        self.horse_jockey = jockey_name
        self.jockeys_claim = jockeys_claim
        self.horse_trainer = trainer
        self.horse_odds = horse_odds
        self.horse_speed = horse_speed
        self.race_winner = winning_horse

class Horse:
    def __init__(self, horse_name, horse_hash):
        self.name = horse_name
        self.horse_hash = horse_hash
        self.races = {}

class HorseRecords:
    def __init__(self, full_races):
        self.horses = {}

        for r in full_races:
            for h in full_races[r].horses:
                race_hash = full_races[r].race_hash
                race_track = full_races[r].track
                race_date = full_races[r].date
                race_time = full_races[r].time
                race_name = full_races[r].name
                prize_money = full_races[r].prize
                race_restrictions = full_races[r].restrictions
                no_of_runners = full_races[r].no_of_runners
                going = full_races[r].going
                race_class = full_races[r].race_class
                race_distance = full_races[r].distance
                winning_horse = full_races[r].winner

                horse_name = h.name
                horse_hash = h.horse_hash
                horse_place = h.place
                horse_age = h.age
                weight_carried = h.weight_carried
                jockey_name = h.jockey
                jockeys_claim = h.jockeys_claim
                trainer = h.trainer
                odds = h.odds
                horse_speed = h.speed

                race = Race(race_hash, race_track, race_date, race_time, race_name, prize_money, race_restrictions, no_of_runners, going, race_class, race_distance, horse_place, horse_age, weight_carried, jockey_name, jockeys_claim, trainer, odds, horse_speed, winning_horse)
                horse = Horse(horse_name, horse_hash)

                try:       
                    self.horses[horse_hash].races[race_hash] = race
                except KeyError:
                    self.horses[horse_hash] = horse
                    self.horses[horse_hash].races[race_hash] = race

''' Returns the races which contain the records of all horses in the dataset '''
def get_full_races(races):
    full_races = {}
    
    for r in races:
        if len(races[r].horses) == races[r].no_of_runners:
            full_races[races[r].race_hash] = races[r]

    return full_races

''' Returns the count of horses given a number of races '''
def horses_with_k_races(races, horse_records):
    horses_race_count = Counter()
    seen_horses = set()

    for r in races:
        for h in races[r].horses:
            if h.horse_hash not in seen_horses:
                total_races = len(horse_records[h.horse_hash].races)
                horses_race_count[total_races] += 1
                seen_horses.add(h.horse_hash)
            else:
                continue

    return horses_race_count

def plot_graph(no_of_races, no_of_horses, title):
    xbins = [x for x in range(len(no_of_races))]
    
    plt.hist(no_of_horses, bins=xbins, color='blue')
    #plt.bar(no_of_races, no_of_horses, width, color='blue')
    plt.show()


def main():
    horses98 = HorseParser('./../Data/born98.csv').horses
    horses05 = HorseParser('./../Data/born05.csv').horses

    races98 = RaceParser('./../Data/born98.csv').races
    races05 = RaceParser('./../Data/born05.csv').races

    full_races_98 = get_full_races(races98)
    full_races_05 = get_full_races(races05)

    full_race_horse_data_98 = HorseRecords(full_races_98).horses
    full_race_horse_data_05 = HorseRecords(full_races_05).horses

    full_horses_race_count_98 = horses_with_k_races(full_races_98, full_race_horse_data_98)
    full_horses_race_count_05 = horses_with_k_races(full_races_05, full_race_horse_data_05)

    no_of_races_98 = [n for n in full_horses_race_count_98]
    no_of_races_05 = [n for n in full_horses_race_count_05]

    no_of_horses_98 = [full_horses_race_count_98[x] for x in full_horses_race_count_98]
    no_of_horses_05 = [full_horses_race_count_05[x] for x in full_horses_race_count_05]

    print 'Born98 Dataset Statistics:'
    print 'Race counts of horses for races with all runners: '
    print full_horses_race_count_98
    print 'No. of races:'
    print no_of_races_98
    print 'No. of horses:'
    print no_of_horses_98

    print ''

    print 'Born05 Dataset Statistics:'
    print 'Race counts of horses for races with all runners: '
    print full_horses_race_count_05
    print 'No. of races:'
    print no_of_races_05
    print 'No. of horses:'
    print no_of_horses_05

    plot_graph(no_of_races_98, no_of_horses_98, 'No. of Races per Horse (Born98 Dataset)')
    plot_graph(no_of_races_05, no_of_horses_05, 'No. of Races per Horse (Born05 Dataset)')


if __name__ == "__main__":
    main()