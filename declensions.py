#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
from collections import OrderedDict

import pymorphy2

import urllib.request
import urllib
import urllib.parse

from bs4 import BeautifulSoup

try:
    np = sys.argv[1]
except IndexError:
    np = "транспортная карта"

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
    forms = list(OrderedDict.fromkeys(forms))
    return forms

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
            if (p.tag.case == "nomn") and (non_nom_found == False):
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
            if (p.tag.case == "nomn") and (non_nom_found == False):
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
    forms2 = decline_morpher_ru(np)
    #forms2 = decline_pymorphy2(np)
    forms = []
    for i in forms2:
        forms.append(i.lower())
    forms_sg = list(OrderedDict.fromkeys(forms[0:6]))
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

    return forms, forms_sg, forms_familiya_io, forms_io_familiya, forms_imya_familiya, forms_familiya_imya, forms_imya_otch_familiya

a, sg, fam_io, io_fam, imya_fam, fam_imya, imya_otch_fam = decline(np)


kribrum_search_string = "(\"" + "\" | \"".join(a) + "\")"
kribrum_search_string_sg = "(\"" + "\" | \"".join(sg) + "\")"
kribrum_search_string_fam_io = "(\"" + "\" | \"".join(fam_io) + "\")"
kribrum_search_string_io_fam = "(\"" + "\" | \"".join(io_fam) + "\")"
kribrum_search_string_fam_imya = "(\"" + "\" | \"".join(fam_imya) + "\")"
kribrum_search_string_imya_fam = "(\"" + "\" | \"".join(imya_fam) + "\")"
kribrum_search_string_imya_otch_fam = "(\"" + "\" | \"".join(imya_otch_fam) + "\")"
kribrum_minus_string = "-\"" + "\" -\"".join(a) + "\""
with open("declension.txt", "a", encoding="utf-8") as out_file:
    out_file.write(kribrum_search_string_fam_io + '\n' + kribrum_search_string_io_fam + '\n' + kribrum_search_string_imya_otch_fam + '\n' + kribrum_search_string_fam_imya + '\n' + kribrum_search_string_imya_fam + '\n' + kribrum_search_string + '\n' + kribrum_search_string_sg + '\n\n' + kribrum_minus_string + '\n\n')