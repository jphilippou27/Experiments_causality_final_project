# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:37:49 2017

@author: kaok
"""

from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
import pandas as pd

all_entries = {}
file_list= []
like_list = []
new_profile = []
#my_dir = "C:\MIDS\W241\\final_project\Chicago\\"
my_dir = os.getcwd()
for file in os.listdir(my_dir):
    if file.endswith(".html"):
        new_file_indicator = True
        file_list.append(os.path.join(my_dir, file))
        profile = open(os.path.join(my_dir, file),'r',encoding='utf8',errors='ignore')
        source_code = profile.read()
        profile.close()
        soup = BeautifulSoup(source_code, 'html.parser')
        name_list = soup.find_all('span')
        for a in name_list:
            keys = a.attrs
            if "class" in keys:
                if new_file_indicator:
                    if new_profile:
                        like_list.append(new_profile)
                        new_profile = []
                    new_file_indicator = False
                    profile_counter = 0
                if "recCard__name" in a["class"]:
                    like_list.append(new_profile)
                    new_profile = [file]
                    profile_counter += 1
                    new_profile.append(profile_counter)
                    new_profile.append(a.string)
                elif "recCard__age" in a["class"]:
                    new_profile.append(int(a.string[2:]))
                elif "Fz($ms)" in a["class"] or " W(100%)" in a["class"] or "D(b)" in a["class"]:
                    new_profile.append(a.string)
if new_profile:
    like_list.append(new_profile)

profile_number = 'blah'
for b in like_list:
    if b:
        if b[0] != profile_number:
            profile_number = b[0]
            all_entries[profile_number] = []
        all_entries[profile_number].append(b[1:])

suitor_list = []
for c in all_entries:
    suitor = [c]
    suitor.extend(all_entries[c][-2])
    suitor_list.append(suitor)
#    print(suitor)

columns = ['filename', 'file_position', 'name', 'age', 'detail_1', 'detail_2']
#make number of columns data dependent
suitor_df = pd.DataFrame(suitor_list,columns=columns)
suitor_df.to_csv('all_suitors.csv', header=True, index=False)

suitor_df = suitor_df.fillna('NO DATA')

unique_suitors = suitor_df.groupby(['name','age','detail_1','detail_2'])['filename'].count()
unique_suitors.to_csv('unique_suitors.csv', header=True)

duplicate_suitors = unique_suitors[unique_suitors>1]
duplicate_suitors.to_csv('duplicate_suitors.csv', header=True)