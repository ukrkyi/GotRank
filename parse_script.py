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

    def retrieve_name(self,line):
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
                        #try to see if name is used with title
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

    def clear(self):
        episode_aliases = {}

proc = Processor()

script = open("ep1.txt", "r")
for line in script:
    if ':' in line:
        name = proc.retrieve_name(line)
        id = proc.process_name(name)
        if id != -1:
            print((name, id, nameset[id]["name"]))
        else:
            print((name, -1))
    elif line[0] == '[':
        episode_characters = re.findall('([A-Z][A-Z ]+[A-Z])', line)
        if len(episode_characters) > 1:
            #scene changed
            #proc.clear()
            print("New scene")
            for character in episode_characters:
                id = proc.process_name(character)
                if id != -1:
                    print((character, id, nameset[id]["name"]))
                else:
                    print((character, -1))
            print("Speaking starts")


print(proc.episode_aliases)
print(nameset)
print(people)
