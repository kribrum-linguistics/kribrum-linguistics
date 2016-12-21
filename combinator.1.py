#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Input: input_1, input_2.
Output: comdined_free.txt.
Combinations are being written with quotes and brackets.
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

def disjunction_str(inp):
    kribrum_search_string = "(\"" + "\" | \"".join(inp) + "\")"
    return kribrum_search_string

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

input_1_lists = list(chunks(input_1, 15))
input_2_lists = list(chunks(input_2, 10))

input_1_chunked_strings = []
input_2_chunked_strings = []

for list in input_1_lists:
    input_1_chunked_strings.append(disjunction_str(list))
for list in input_2_lists:
    input_2_chunked_strings.append(disjunction_str(list))

list_str = []
for entry_1 in input_1_chunked_strings:
    for entry_2 in input_2_chunked_strings:
        list_str.append(entry_1 + " " + entry_2)

with open("combined_free.txt", "a") as combined_file:
    for i in list_str:
        combined_file.write(i + "\n")