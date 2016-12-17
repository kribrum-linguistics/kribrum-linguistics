#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
from collections import OrderedDict

import urllib.request
import urllib
import urllib.parse

from bs4 import BeautifulSoup

try:
    np = sys.argv[1]
except IndexError:
    np = "транспортная карта"

def decline(np):
    np = np.lower()
    parameters = {"s": np}
    parameters_encoded = urllib.parse.urlencode(parameters).encode("utf-8")
    req = urllib.request.Request(url="http://api.morpher.ru/WebService.asmx/GetXml", data=parameters_encoded)
    resp = urllib.request.urlopen(req).read()
    resp_text = resp.decode("utf-8")

    print(resp_text)

    soup = BeautifulSoup(resp, "xml")
    page_text = soup.findAll(text=True)
  #  page_text = []
   # page_text = (text for text in soup.find_all(text=True) if text.parent.name not in ["Ф", "И", "О"])
    #print(page_text)
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
    forms_sg = list(OrderedDict.fromkeys(forms[0:6]))
    forms = list(OrderedDict.fromkeys(forms))
    forms_lists = []
    for form in forms:
        forms_lists.append(form.split())
    #print(forms_lists)

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

    forms_familiya_imya = []
    for form in forms_lists:
        if len(form) >= 2:
            familiya_imya = form[0] + ' ' + form[1]
            forms_familiya_imya.append(familiya_imya)
    forms_familiya_imya = list(OrderedDict.fromkeys(forms_familiya_imya))

    return forms, forms_sg, forms_familiya_io, forms_io_familiya, forms_imya_familiya, forms_familiya_imya

a, sg, fam_io, io_fam, imya_fam, fam_imya = decline(np)


kribrum_search_string = "(\"" + "\" | \"".join(a) + "\")"
kribrum_search_string_sg = "(\"" + "\" | \"".join(sg) + "\")"
kribrum_search_string_fam_io = "(\"" + "\" | \"".join(fam_io) + "\")"
kribrum_search_string_io_fam = "(\"" + "\" | \"".join(io_fam) + "\")"
kribrum_search_string_fam_imya = "(\"" + "\" | \"".join(fam_imya) + "\")"
kribrum_search_string_imya_fam = "(\"" + "\" | \"".join(imya_fam) + "\")"
kribrum_minus_string = "-\"" + "\" -\"".join(a) + "\""
with open("declension.txt", "a", encoding="utf-8") as out_file:
    out_file.write(kribrum_search_string_fam_io + '\n' + kribrum_search_string_io_fam + '\n' + kribrum_search_string_fam_imya + '\n' + kribrum_search_string_imya_fam + '\n' + kribrum_search_string + '\n' + kribrum_search_string_sg + '\n\n' + kribrum_minus_string + '\n\n')