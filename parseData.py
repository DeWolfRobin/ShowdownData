class Battle:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()

class Player:
    def __init__(self):
        self.team = dict()
        self.name = "unknown"
        self.turnaction

class Pokemon:
    def __init__(self, species):
        self.species = species
        self.nickname = False
        self.moves = list()

def parseBattle(filename):
    b = Battle()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            detectPokemonAndPlayers(line.split("|"),b)
        for line in lines:
            detectMoves(line.split("|"),b)
            # parseLine(line, b)
    for i,p in b.p2.team.items():
        print(p.moves)

def parseLine(line, b):
    #sort these in the order of the file for faster parsing
    l = line.split("|")

def detectPokemonAndPlayers(l, b):
    if (len(l) == 2 or
        l[1] == 'j'):
        pass
    elif (len(l) == 6 and
        l[1].strip() == "player"):
        if l[2] == "p1":
            b.p1.name = l[3]
        if l[2] == "p2":
            b.p2.name = l[3]
    elif (len(l) == 5 and
        l[1].strip() == "poke"):
        if l[2] == "p1":
            b.p1.team[l[3].split(",")[0]] = Pokemon(l[3])
        if l[2] == "p2":
            b.p2.team[l[3].split(",")[0]] = Pokemon(l[3])
    elif (l[1].strip() == "switch"):
        s = l[2].split(":")
        p = l[3].split(",")
        if "Urshifu-" in p[0]:
            p[0] = "Urshifu-*"
        if "p1" in s[0]:
            b.p1.team[p[0]].nickname = s[1]
        if "p2" in s[0]:
            b.p2.team[p[0]].nickname = s[1]

def detectMoves(l, b):
    if (l[1].strip() == "move"):
        s = l[2].split(":")
        pk = s[1].strip()
        if "p1" in s[0]:
            for i,p in b.p1.team.items():
                if p.nickname.strip() == pk:
                    if l[3] not in p.moves:
                        p.moves.append(l[3])
        if "p2" in s[0]:
            for i,p in b.p2.team.items():
                if p.nickname.strip() == pk:
                    if l[3] not in p.moves:
                        p.moves.append(l[3])

parseBattle("data/china-gen8ou-4182974.log")
