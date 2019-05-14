#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
import functools

nameset = json.load(open("example.json", 'r'))

i = 0

f = open("names.txt", "w")

people = {}

for person in nameset:
    person["id"] = i
    people[person["name"].upper()] = i
    for alias in person["aliases"]:
        people[alias.upper()] = i
    f.write(person["name"] +"\n")
    i += 1

f.close()

class Processor:
    def __init__(self):
        self.names_used = []
        self.episode_aliases = {
            "TYRION" : "TYRION LANNISTER",
            "BRAN" : "BRAN STARK",
            "BENJEN" : "BENJEN STARK",
            "JOFFREY" : "JOFFREY BARATHEON",
            "CERSEI" : "CERSEI LANNISTER",
            "JAIME" : "JAIME LANNISTER",
            "VISERYS" : "VISERYS TARGARYEN",
            "JORY" : "JORY CASSEL",
            "RHAEGAR" : "RHAEGAR TARGARYEN"
        }
        self.name_pool = list(people.keys()) + list(self.episode_aliases.keys())

    def retrieve_name(self, line):
        index = line.index(":")
        name = line[:index]
        try:
            parenthesis = line.index("(")
            name = name[:parenthesis - 1]
        except:
            pass
        return name.upper()

    def process_name(self, name):
        if name in self.episode_aliases:
            name = self.episode_aliases[name]
        else:
            if name not in people:
                # try to see if it is part of already used name
                for fullname in self.names_used:
                    if " " in fullname and name in fullname.split(" "):
                        self.episode_aliases[name] = fullname
                        self.name_pool.append(name)
                        name = fullname
                        break
                else:
                    if " " in name:
                        # try to see if name is used with title
                        for partname in name.split(" "):
                            if partname in people:
                                self.episode_aliases[name] = partname
                                self.name_pool.append(name)
                                name = partname
                                break
            if name not in self.names_used:
                self.names_used.append(name)
        if name in people:
            return people[name]
        else:
            return -1

    def replic_to_list_of_ids(self, replic):
        names = []
        self.name_pool.sort(key=functools.cmp_to_key(lambda x, y: len(y) - len(x)))
        for name in self.name_pool:
            matches = re.subn("([^A-Z]" + name + "[^A-Z])", "", replic)
            if matches[1]:
                names.append((name, matches[1]))
                replic = matches[0]
        for i in range(len(names)):
            names[i] = (self.process_name(names[i][0]), names[i][1])
        return names

    def clear(self):
        self.episode_aliases = {}

proc = Processor()

replics_by_id = {}

def parse_line(line):
    if ':' in line:
        #print(replic)
        name = proc.retrieve_name(line)
        id = proc.process_name(name)
        delim = line.find(':')
        replic = line[delim + 1:]

        if id in replics_by_id:
            replics_by_id[id].append(replic)
        else:
            replics_by_id[id] = [replic]
        #if id != -1:
        #    print((name, id, nameset[id]["name"]))
        #else:
        #    print((name, -1))
        prev_id = id
    elif re.search('[a-zA-Z]', line) is not None:
        print("Not replic: ", line, end='')
        episode_characters = re.findall('([A-Z][A-Z ]+[A-Z])', line)
        if len(episode_characters) > 1:
            # scene changed
            # proc.clear()
            #print("\n[New scene]\n")
            for character in episode_characters:
                id = proc.process_name(character)
                #if id != -1:
                #    print((character, id, nameset[id]["name"]))
                #else:
                #    print((character, -1))
            #print("\n[Speaking starts]\n")

script = open("scripts/episode1.txt", "r")
for line in script:
    parse_line(line)

script = open("scripts/episode2.txt", "r")
for line in script:
    parse_line(line)

script = open("scripts/episode3.txt", "r")
for line in script:
    parse_line(line)

script = open("scripts/episode4.txt", "r")
for line in script:
    parse_line(line)


script = open("scripts/episode5.txt", "r")
for line in script:
    parse_line(line)


script = open("scripts/episode6.txt", "r")
for line in script:
    parse_line(line)

script = open("scripts/episode7.txt", "r")
for line in script:
    parse_line(line)

script = open("scripts/episode8.txt", "r")
for line in script:
    parse_line(line)

script = open("scripts/episode9.txt", "r")
for line in script:
    parse_line(line)

script = open("scripts/episode10.txt", "r")
for line in script:
    parse_line(line)

for i in replics_by_id:
    replics_by_id[i] = proc.replic_to_list_of_ids('\n'.join(replics_by_id[i]).upper())

if None in replics_by_id:
    del replics_by_id[None]

del replics_by_id[-1]

matrix_for_test = [[0 for j in range(len(nameset))] for i in range(len(nameset))]

for i in replics_by_id:
    for j in replics_by_id[i]:
        if j[0] >= 0:
            matrix_for_test[i][j[0]] = j[1]

#clear loops
for i in replics_by_id:
    matrix_for_test[i][i] = 0

f = open("matrix.txt", "w")

f.write(str(len(nameset)) + "\n")

for row in matrix_for_test:
    for el in row:
        f.write("%3d" % (el, ))
    f.write("\n")

f.close()

print(replics_by_id)

print(people["VISERYS TARGARYEN".upper()])
ment = (829, 929)
print ("Mentions: " + str(matrix_for_test[ment[0]][ment[1]]) + " from " + str(nameset[ment[0]]["name"]) +" to "+str(nameset[ment[1]]["name"]))

for name in proc.names_used:
    id = proc.process_name(name)
    print(name.ljust(20), id, "" if id == -1 else nameset[id]["name"])
print(proc.episode_aliases)
print(nameset)
print(people)
