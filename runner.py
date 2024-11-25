class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                # print(type(participant))
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers

"""r1=Runner('Vasya')
r1.run()
r1.walk()
print(r1.distance)
print(r1.name)
print(r1.__doc__)
"""

"""rn_0 = Runner('Усэйн', 10)
rn_1 = Runner('Андрей', 9)
rn_2 = Runner('Ник', 12)

tnmnt = Tournament(1000,rn_0, rn_1)
finishers = tnmnt.start()
for i in finishers:
    print(i.__str__())"""