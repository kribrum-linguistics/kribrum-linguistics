#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Input: input_1, input_2.
Output: comdined.txt.
Each combination is being written in a new line.
'''

input_1 = []
input_2 = []

with open("input_1") as input_1_file:
    for line in input_1_file:
        line = line.strip()
        if len(line) > 0:
            input_1.append(line)

with open("input_2") as input_2_file:
    for line in input_2_file:
        line = line.strip()
        if len(line) > 0:
            input_2.append(line)

lists = []

for entry_1 in input_1:
    lists.append([])
    for entry_2 in input_2:
        lists[-1].append(entry_1 + " " + entry_2)

with open("combined.txt", "a") as combined_file:
    for i in lists:
        for j in i:
            combined_file.write(j + "\n")
    combined_file.write("\n\n\n")
print(lists)