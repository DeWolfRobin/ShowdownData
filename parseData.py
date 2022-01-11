from os import walk
from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

class Battle:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()

    def getPlayers(self):
        return [self.p1, self.p2]

class Player:
    def __init__(self):
        self.team = dict()
        self.name = "unknown"
        self.turnactions = list()
        self.won = False

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
    turnParser("".join(lines), b)
    return b

def detectPokemonAndPlayers(l, b):
    if (len(l) == 2 or
        (len(l) > 1 and l[1] == 'j')):
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
    elif (len(l) > 1 and l[1].strip() == "switch"):
        s = l[2].split(":")
        p = l[3].split(",")
        if "Urshifu-" in p[0]:
            p[0] = "Urshifu-*"
        if "Silvally-" in p[0]:
            p[0] = "Silvally-*"
        if "-Mega" in p[0]:
            p[0] = p[0].split("-")[0]
        if "Gourgeist" in p[0]:
            p[0] = "Gourgeist-*"
        if "Mimikyu" in p[0]:
            p[0] = "Mimikyu"
        if "p1" in s[0]:
            b.p1.team[p[0]].nickname = s[1]
        if "p2" in s[0]:
            b.p2.team[p[0]].nickname = s[1]

def detectMoves(l, b):
    if (len(l) > 1 and l[1].strip() == "move"):
        s = l[2].split(":")
        pk = s[1].strip()
        if "p1" in s[0]:
            for i,p in b.p1.team.items():
                if p.nickname:
                    if p.nickname.strip() == pk:
                        if l[3] not in p.moves:
                            p.moves.append(l[3])
                else:
                    if p.species.strip() == pk:
                        if l[3] not in p.moves:
                            p.moves.append(l[3])
        elif "p2" in s[0]:
            for i,p in b.p2.team.items():
                if p.nickname:
                    if p.nickname.strip() == pk:
                        if l[3] not in p.moves:
                            p.moves.append(l[3])
                else:
                    if p.species.strip() == pk:
                        if l[3] not in p.moves:
                            p.moves.append(l[3])

def turnParser(l, b):
    turns = l.split("|turn|")
    for turn in turns:
        lines = turn.split("\n")
        try:
            turn = int(lines[0])
            for line in lines:
                l = line.split("|")
                if len(b.p1.turnactions) <= turn:
                    b.p1.turnactions.append(list())
                    b.p2.turnactions.append(list())
                if len(l) > 1:
                    if (len(l) >= 3 and l[1].strip() == "switch"):
                        s = l[2].split(":")
                        p = l[3].split(",")
                        if "Urshifu-" in p[0]:
                            p[0] = "Urshifu-*"
                        if "Silvally-" in p[0]:
                            p[0] = "Silvally-*"
                        if "-Mega" in p[0]:
                            p[0] = p[0].split("-")[0]
                        if "Gourgeist" in p[0]:
                            p[0] = "Gourgeist-*"
                        if "Mimikyu" in p[0]:
                            p[0] = "Mimikyu"
                        if "p1" in s[0]:
                            b.p1.turnactions[turn].append(line)
                        elif "p2" in s[0]:
                            b.p2.turnactions[turn].append(line)
                    elif (len(l) >= 3 and l[1].strip() == "move"):
                        s = l[2].split(":")
                        p = l[3].split(",")
                        if "Urshifu-" in p[0]:
                            p[0] = "Urshifu-*"
                        if "Silvally-" in p[0]:
                            p[0] = "Silvally-*"
                        if "-Mega" in p[0]:
                            p[0] = p[0].split("-")[0]
                        if "Gourgeist" in p[0]:
                            p[0] = "Gourgeist-*"
                        if "Mimikyu" in p[0]:
                            p[0] = "Mimikyu"
                        if "p1" in s[0]:
                            b.p1.turnactions[turn].append(line)
                        elif "p2" in s[0]:
                            b.p2.turnactions[turn].append(line)
                    elif (len(l) > 2 and '-' in l[1].strip()):
                        s = l[2].split(":")
                        if "p1" in s[0]:
                            b.p1.turnactions[turn].append(line)
                        elif "p2" in s[0]:
                            b.p2.turnactions[turn].append(line)
                    elif l[1].strip() == "win":
                        if l[2] == b.p1.name:
                            b.p1.won = True
                        else:
                            b.p2.won = True
        except ValueError as e:
            #Turn 0
            for line in lines:
                l = line.split("|")
                if (len(l) > 1 and l[1].strip() == "switch"):
                    s = l[2].split(":")
                    p = l[3].split(",")
                    if "Urshifu-" in p[0]:
                        p[0] = "Urshifu-*"
                    if "Silvally-" in p[0]:
                        p[0] = "Silvally-*"
                    if "-Mega" in p[0]:
                        p[0] = p[0].split("-")[0]
                    if "Gourgeist" in p[0]:
                        p[0] = "Gourgeist-*"
                    if "Mimikyu" in p[0]:
                        p[0] = "Mimikyu"
                    if "p1" in s[0]:
                        b.p1.turnactions.append(line)
                    elif "p2" in s[0]:
                        b.p2.turnactions.append(line)

def searchWonWithPokemon(l, pokemonName=False):
    out = list()
    for b in l:
        for player in b.getPlayers():
            if player.won:
                if pokemonName:
                    for p in player.team:
                        if p == pokemonName:
                            out.append(b)
                else:
                    out.append(b)
    return out

def getAllPokemonNames(l):
    out = list()
    for b in l:
        for player in b.getPlayers():
            for p in player.team:
                if p not in out:
                    out.append(p)
    return out

def getMostWonPokemon(parsed):
    pokemon = getAllPokemonNames(parsed)
    mapped = dict()

    for p in pokemon:
        mapped[p] = len(searchWonWithPokemon(parsed, p))

    return {k: v for k, v in sorted(mapped.items(), key=lambda item: item[1], reverse=True)}

def getMostWonMovesets(parsed, p):
    allmoves = dict()

    for b in searchWonWithPokemon(parsed, p):
        for player in b.getPlayers():
            if player.won:
                for move in player.team[p].moves:
                    if move in allmoves:
                        allmoves[move] = allmoves[move] +1
                    else:
                        allmoves[move] = 1
    return {k: v for k, v in sorted(allmoves.items(), key=lambda item: item[1], reverse=True)}


filenames = next(walk("data/"), (None, None, []))[2]
parsed = list()
for battle in filenames:
    parsed.append(parseBattle("data/"+battle))

champs = take(6, getMostWonPokemon(parsed).keys())

team = dict()

for champ in champs:
    team[champ] = take(4, getMostWonMovesets(parsed, champ).keys())

print(team)
