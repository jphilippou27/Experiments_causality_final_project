# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:37:49 2017

@author: kaok
"""

from html.parser import HTMLParser
from bs4 import BeautifulSoup
import os
import pandas as pd
import csv

def get_suitor_info(directory):
    all_entries = {}
    #file_list= []
    like_list = []
    new_profile = []
    #my_dir = os.getcwd()

    #retrieve every record of a suitor from every profile#.html file
    #like_list is a list in which each element is a list of the details of a suitor
    for file in os.listdir(directory):
        if file.endswith(".html"):
            new_file_indicator = True
            #file_list.append(os.path.join(directory, file))
            profile = open(os.path.join(directory, file),'r',encoding='utf8',errors='ignore')
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
                        if bool(a.string):
                            new_profile.append(int(a.string[2:]))
                        else:
                            new_profile.append(a.string)
                    elif "Fz($ms)" in a["class"] or " W(100%)" in a["class"] or "D(b)" in a["class"]:
                        new_profile.append(a.string)
    if new_profile:
        like_list.append(new_profile)

    #organize all the records in like_list by filename
    #all_entries is a dictionary that has the filename as its key and a list of entries from like_list as its value
    profile_number = 'blah'
    for b in like_list:
        if b:
            if b[0] != profile_number:
                profile_number = b[0]
                all_entries[profile_number] = []
            all_entries[profile_number].append(b[1:])

    #get the 2nd suitor record of each file
    #suitor_list is the actual list of liked suitors
    num_columns = 0
    suitor_list = []
    for c in all_entries:
        suitor = [c]
        suitor.extend(all_entries[c][1])
        suitor_list.append(suitor)
        if len(all_entries[c][1]) > num_columns:
            num_columns = len(all_entries[c][1])

    #make number of columns data dependent
    columns = ['filename', 'file_position', 'name', 'age']
    detail_number = 1
    while len(columns) <= num_columns:
        columns.append('detail_' + str(detail_number))
        detail_number += 1

    #write the record of every swipe
    suitor_df = pd.DataFrame(suitor_list,columns=columns)
    #suitor_df.to_csv('all_suitors.csv', header=True, index=False)

    #fill in missing values to enable counting of unique profiles
    suitor_df = suitor_df.fillna('NO DATA')

    #count the number of unique profiles
    #write the record of unique profiles in the run, including the number of times that profile appears
    #groupby_list = columns[1:]
    groupby_list = columns[2:]
    unique_suitors = suitor_df.groupby(groupby_list)['filename'].count()
    #unique_suitors.to_csv('unique_suitors.csv', header=True)

    #write the record of profiles that appeared more than once during the run
    duplicate_suitors = unique_suitors[unique_suitors>1]
    #duplicate_suitors.to_csv('duplicate_suitors.csv', header=True)

    #write all records of all suitors in every profile#.html file
    #not sure how to handle strange characters-- ignoring for now
    #with open('original_suitor_records.csv', 'w', newline='',errors='ignore') as original_suitor_records:
        #wr = csv.writer(original_suitor_records)
        #wr.writerow(columns)
        #for d in like_list:
            #if d:
                #wr.writerow(d)
    
    return unique_suitors, duplicate_suitors, suitor_df, all_entries

complete_records = {}
directories = os.walk(os.getcwd())
for folder in directories:
    #print(folder)
    current_dir = folder[0]
    subfolders = folder[1]
    contents = folder[2]
    if contents:
        if any('.html' in file for file in contents):
            complete_records[current_dir] = get_suitor_info(current_dir)