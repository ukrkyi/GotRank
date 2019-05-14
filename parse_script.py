#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re

nameset = json.load(open("example.json", 'r'))

i = 0

people = {}

for person in nameset:
    person["id"] = i
    people[person["name"].upper()] = i
    for alias in person["aliases"]:
        people[alias.upper()] = i
    i += 1


class Processor:
    def __init__(self):
        self.names_used = []
        self.episode_aliases = {}

    def retrieve_name(self, line):
        index = line.index(":")
        name = line[:index]
        try:
            parenthesis = line.index("(")
            name = name[:parenthesis - 1]
        except:
            pass
        return name

    def process_name(self, name):
        if name in self.episode_aliases:
            name = self.episode_aliases[name]
        else:
            if name not in people:
                # try to see if it is part of already used name
                for fullname in self.names_used:
                    if " " in fullname and name in fullname.split(" "):
                        self.episode_aliases[name] = fullname
                        name = fullname
                        break
                else:
                    if " " in name:
                        # try to see if name is used with title
                        for partname in name.split(" "):
                            if partname in people:
                                self.episode_aliases[name] = partname
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
        for i in self.episode_aliases:
            if replic.count(i):
                names += [i for k in range(replic.count(i))]
        for j in people:
            if replic.count(j):
                names += [j for k in range(replic.count(j))]
        for i in range(len(names)):
            names[i] = self.process_name(names[i])
        return names

    def clear(self):
        self.episode_aliases = {}


proc = Processor()

script = open("ep1.txt", "r")
is_replic = False
replic = ''
replics_by_id = {}
prev_id = None
for line in script:
    if ':' in line:
        if prev_id in replics_by_id:
            replics_by_id[prev_id].append(replic)
        else:
            replics_by_id[prev_id] = [replic]
        print(replic)
        is_replic = True
        name = proc.retrieve_name(line)
        id = proc.process_name(name)
        delim = line.find(':')
        replic = line[delim + 1:]
        if id != -1:
            print((name, id, nameset[id]["name"]))
        else:
            print((name, -1))
        prev_id = id
    elif line[0] == '[':
        is_replic = False
        episode_characters = re.findall('([A-Z][A-Z ]+[A-Z])', line)
        if len(episode_characters) > 1:
            # scene changed
            # proc.clear()
            print("\n[New scene]\n")
            for character in episode_characters:
                id = proc.process_name(character)
                if id != -1:
                    print((character, id, nameset[id]["name"]))
                else:
                    print((character, -1))
            print("\n[Speaking starts]\n")
    elif is_replic:
        replic += line

for i in replics_by_id:
    for j in range(len(replics_by_id[i])):
        replics_by_id[i][j] = proc.replic_to_list_of_ids(replics_by_id[i][j].strip().upper())
    j = 0
    while j < len(replics_by_id[i]) - 1:
        replics_by_id[i][j] += replics_by_id[i][j + 1]
        del replics_by_id[i][j + 1]
    replics_by_id[i] = replics_by_id[i][0]

del replics_by_id[None]
del replics_by_id[-1]

for i in replics_by_id:
    mentions = {}
    for j in replics_by_id[i]:
        mentions[j] = replics_by_id[i].count(j)
    mentions = [(v, k) for v, k in mentions.items()]
    mentions = set(mentions)
    mentions = list(mentions)
    replics_by_id[i] = mentions


matrix_for_test = [[0 for j in range(len(nameset))] for i in range(len(nameset))]

for i in replics_by_id:
    for j in replics_by_id[i]:
        matrix_for_test[i][j[0]] = j[1]

f = open("matrix.txt", "w")

for row in matrix_for_test:
    for el in row:
        f.write("%3d" % (el, ))
    f.write("\n")

print(replics_by_id)
print (str(matrix_for_test[831][479]) + str(nameset[831]) + str(nameset[479]))

print(matrix_for_test[919][1860])
for i in nameset:
    if i['id'] in [1648, 308]:
        print(i)
print(proc.episode_aliases)
print(nameset)
print(people)
