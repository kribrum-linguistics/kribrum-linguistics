#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import urllib
import urllib.parse
import urllib.request
import re
from collections import OrderedDict

from bs4 import BeautifulSoup

import pymorphy2

try:
    np = sys.argv[1]
except IndexError:
    np = "транспортная карта"

with open("case_forms.txt", "w", encoding="utf-8") as out_file:
    out_file.write("")

def kribrum_normal_form(string):
    string = string.lower()
    string = re.sub("\W", " ", string)
    string = re.sub("\s+", " ", string)
    string = re.sub("(ё|ё)", "е", string)
    string = string.strip()
    return string

def decline_morpher_ru(np):
    parameters = {"s": np}
    parameters_encoded = urllib.parse.urlencode(parameters).encode("utf-8")
    req = urllib.request.Request(url="http://api.morpher.ru/WebService.asmx/GetXml", data=parameters_encoded)
    resp = urllib.request.urlopen(req).read()
    resp_text = resp.decode("utf-8")

    print(resp_text)

    soup = BeautifulSoup(resp, "xml")
    page_text = soup.findAll(text=True)
    forms = []
    forms.append(np)
    #space count is needed to exclude parsed personal names of people
    space_count = 0
    fio = False
    for i in page_text:
        if i.count(" ") > space_count:
            space_count = i.count(" ")
    for i in page_text:
        if len(i.strip()) > 0:
            if i.count(" ") == space_count:
                forms.append(i)
            else:
                fio = True
    forms_unique = list(OrderedDict.fromkeys(forms))
    return forms, forms_unique

def decline_pymorphy2(np):
    forms = []
    forms.append(np)
    morph = pymorphy2.MorphAnalyzer()
    np_list = np.split()
    #p = morph.parse(np)
    #print(p.normal_form)
    nom_found = False
    gender = ""
    number_of_nom = 0
    for word in enumerate(np_list):
        if word[0] == 0:
            for anal in enumerate(morph.parse(word[1])):
                if anal[1].tag.case == "nomn":
                    print(anal[0])
                    number_of_nom = anal[0]
        p = morph.parse(word[1])[0]
        if (p.tag.case == "nomn") and (nom_found == False):
            gender = p.tag.gender
            nom_found = True
    cases = ['gent', 'datv', 'accs', 'ablt', 'loct']
    normal = False
    for case in cases:
        non_nom_found = False
        a = []
        first_word = normal
        for word in np_list:
            if first_word == True:
                p = morph.parse(word)[number_of_nom]
            else:
                p = morph.parse(word)[0]
            first_word = False
            if (p.tag.case == "nomn") and (not non_nom_found):
                a.append(p.inflect({'sing', case, gender}).word)
            else:
                a.append(word)
                non_nom_found = True
        forms.append(" ".join(a))
    for case in cases:
        non_nom_found = False
        a = []
        first_word = normal
        for word in np_list:
            if first_word == True:
                p = morph.parse(word)[number_of_nom]
            else:
                p = morph.parse(word)[0]
            first_word = False
            if (p.tag.case == "nomn") and (not non_nom_found):
                try:
                    a.append(p.inflect({'plur', case, gender}).word)
                except AttributeError:
                    a.append(p.inflect({'plur', case}).word)
            else:
                a.append(word)
        forms.append(" ".join(a))
    print(forms)
    return forms


def decline(np):
    with open("forms_dict.json") as forms_dict_file:
        forms_dict = json.loads(forms_dict_file.read())
    if np not in forms_dict:
        forms_all, forms2 = decline_morpher_ru(np)
        forms_dict[np] = {}
        forms_dict[np]["all_forms"] = forms_all
        forms_dict[np]["forms"] = forms2
    else:
        forms_all = forms_dict[np]["all_forms"]
        forms2 = forms_dict[np]["forms"]
    with open("forms_dict.json", "w", encoding="utf-8") as forms_dict_file:
        forms_dict_file.write(json.dumps(forms_dict,ensure_ascii=False))
    #forms2 = decline_pymorphy2(np)
    forms = []
    for i in forms2:
        forms.append(i)
    forms_sg = list(OrderedDict.fromkeys(forms[0:5]))
    forms = list(OrderedDict.fromkeys(forms))
    forms_lists = []
    for form in forms:
        forms_lists.append(form.split())

    forms_familiya_io = []
    for form in forms_lists:
        if len(form) >= 3:
            familiya_i_o = form[0] + ' ' + form[1][0] + ' ' + form[2][0]
            forms_familiya_io.append(familiya_i_o)
    forms_familiya_io = list(OrderedDict.fromkeys(forms_familiya_io))

    forms_io_familiya = []
    for form in forms_lists:
        if len(form) >= 3:
            io_familiya = form[1][0] + ' ' + form[2][0] + ' ' + form[0]
            forms_io_familiya.append(io_familiya)
    forms_io_familiya = list(OrderedDict.fromkeys(forms_io_familiya))

    forms_imya_familiya = []
    for form in forms_lists:
        if len(form) >= 2:
            imya_familiya = form[1] + ' ' + form[0]
            forms_imya_familiya.append(imya_familiya)
    forms_imya_familiya = list(OrderedDict.fromkeys(forms_imya_familiya))

    forms_imya_otch_familiya = []
    for form in forms_lists:
        if len(form) >= 3:
            imya_otch_familiya = form[1] + ' ' + form[2] + ' ' + form[0]
            forms_imya_otch_familiya.append(imya_otch_familiya)
    forms_imya_otch_familiya = list(OrderedDict.fromkeys(forms_imya_otch_familiya))

    forms_familiya_imya = []
    for form in forms_lists:
        if len(form) >= 2:
            familiya_imya = form[0] + ' ' + form[1]
            forms_familiya_imya.append(familiya_imya)
    forms_familiya_imya = list(OrderedDict.fromkeys(forms_familiya_imya))

    return forms, forms_sg, forms_familiya_io, forms_io_familiya, forms_imya_familiya, forms_familiya_imya, forms_imya_otch_familiya, forms_all

def write_all(np):
    a, sg, fam_io, io_fam, imya_fam, fam_imya, imya_otch_fam, forms_all = decline(np)
    a_k = []
    for i in a:
        a_k.append(kribrum_normal_form(i))
    sg_k = []
    for i in sg:
        sg_k.append(kribrum_normal_form(i))
    fam_io_k = []
    for i in fam_io:
        fam_io_k.append(kribrum_normal_form(i))
    io_fam_k = []
    for i in io_fam:
        io_fam_k.append(kribrum_normal_form(i))
    imya_fam_k = []
    for i in imya_fam:
        imya_fam_k.append(kribrum_normal_form(i))
    fam_imya_k = []
    for i in fam_imya:
        fam_imya_k.append(kribrum_normal_form(i))
    imya_otch_fam_k = []
    for i in imya_otch_fam:
        imya_otch_fam_k.append(kribrum_normal_form(i))
    a_k = []
    for i in a:
        a_k.append(kribrum_normal_form(i))
    kribrum_search_string = "(\"" + "\"|\"".join(a_k) + "\")"
    kribrum_search_string_sg = "(\"" + "\"|\"".join(sg_k) + "\")"
    kribrum_search_string_fam_io = "(\"" + "\"|\"".join(fam_io_k) + "\")"
    kribrum_search_string_io_fam = "(\"" + "\"|\"".join(io_fam_k) + "\")"
    kribrum_search_string_fam_imya = "(\"" + "\"|\"".join(fam_imya_k) + "\")"
    kribrum_search_string_imya_fam = "(\"" + "\"|\"".join(imya_fam_k) + "\")"
    kribrum_search_string_imya_otch_fam = "(\"" + "\"|\"".join(imya_otch_fam_k) + "\")"
    kribrum_minus_string = "-\"" + "\" -\"".join(a_k) + "\""
    with open("case_forms.txt", "a", encoding="utf-8") as out_file:
        out_file.write(kribrum_search_string_fam_io + '\n' + kribrum_search_string_io_fam + '\n' + kribrum_search_string_imya_otch_fam + '\n' + kribrum_search_string_fam_imya + '\n' + kribrum_search_string_imya_fam + '\n' + kribrum_search_string + '\n' + kribrum_search_string_sg + '\n\n' + kribrum_minus_string + '\n\n')
    return forms_all

all_forms = []
with open("input_1") as data_file:
    other = False
    for line in data_file:
        line = line.strip()
        line = line.replace("\u0301", "")
        if len(line) > 0:
            if line[0] == "=":
                other = True
            if other == False:
                all_forms.append(write_all(line))
print(all_forms)

case = {
    0: "NOM",
    1: "GEN",
    2: "DAT",
    3: "ACC",
    4: "INSTR",
    5: "LOC",
    6: "NOM.PL",
    7: "GEN.PL",
    8: "DAT.PL",
    9: "ACC.PL",
    10: "INSTR.PL",
    11: "LOC.PL",
}

def decl_by_case(all_forms):
    by_case_string = ""
    for j in range(12):
        by_case_string += case[j] + "\n"
        for i in all_forms:
            try:
                by_case_string += kribrum_normal_form(i[j]) + "\n"
            except IndexError:
                pass
        by_case_string += "\n"
    by_case_string += "\nSG and PL\n\n"
    for j in range(6):
        by_case_string += case[j] + "\n"
        for i in all_forms:
            try:
                by_case_string += kribrum_normal_form(i[j]) + "\n"
            except IndexError:
                pass
            try:
                by_case_string += kribrum_normal_form(i[j + 6]) + "\n"
            except IndexError:
                pass
        by_case_string += "\n"
    return by_case_string

def decl_by_case_success(all_forms):
    by_case_string = "\nALL CASES\n"
    uniques = []
    for j in range(12):
        for i in all_forms:
            try:
                if i[j] not in uniques:
                    by_case_string += kribrum_normal_form(i[j]) + "\n"
                uniques.append(i[j])
            except IndexError:
                pass
    return by_case_string

def decl_by_case_sg_success(all_forms):
    by_case_string = "\nALL CASES, SG\n"
    uniques = []
    for j in range(6):
        for i in all_forms:
            try:
                if i[j] not in uniques:
                    by_case_string += kribrum_normal_form(i[j]) + "\n"
                uniques.append(i[j])
            except IndexError:
                pass
    return by_case_string

def decl_by_term_success(all_forms):
    by_term_string = "\nALL TERMS\n"
    uniques = []
    for i in all_forms:
        for j in i:
            if j not in uniques:
                by_term_string += kribrum_normal_form(j) + "\n"
            uniques.append(j)
    return by_term_string


with open("case_forms.txt", "a") as case_forms_file:
    case_forms_file.write("\n\n")
    case_forms_file.write(decl_by_case(all_forms))
    case_forms_file.write(decl_by_case_success(all_forms))
    case_forms_file.write(decl_by_case_sg_success(all_forms))
    case_forms_file.write(decl_by_term_success(all_forms))
