# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 20:33:49 2017

@author: kaok
"""
#set PYTHONPATH=%PYTHONPATH%; C:/Users/Jennifer/Documents/Berkeley/W241/Experiment/Data_Collection/MD/Male_original/Antonio
#%cd C:\Users\Jennifer\Documents\Berkeley\W241\Experiment\Data_Collection\MD\Male_original\Antonio
#%pwd
from html import *
from bs4 import BeautifulSoup
import os
import pandas as pd

def check_for_duplicates(directory):
    all_entries = {}
    like_list = []
    new_profile = []

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
            profile_image_counter = 0
            background_images = {}
            for a in name_list:
                div_list = a.find_all('div')
                for aa in div_list:
                    keys = aa.attrs
                    if "style" in keys:
                        if "background-image:" in aa["style"]:
                            profile_image_counter += 1
                            #split1 = aa["style"].rpartition("/")
                            #split2 = split1[2].rpartition('"')
                            split1 = aa["style"].partition('"')
                            split2 = split1[2].rpartition('"')
                            background_images[profile_image_counter] = split2[0]
                        
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
                        if profile_counter in background_images.keys():
                            new_profile.append(background_images[profile_counter])
                        else:
                            #print(file)
                            #print(profile_counter)
                            #print(background_images)
                            #print()
                            new_profile.append(float('nan'))
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
    columns = ['filename', 'file_position', 'profile_image','name', 'age']
    detail_number = 1
    while len(columns) <= num_columns:
        columns.append('detail_' + str(detail_number))
        detail_number += 1

    suitor_df = pd.DataFrame(suitor_list,columns=columns)

    #fill in missing values to enable counting of unique profiles
    suitor_df = suitor_df.fillna('NO DATA')

    #count the number of unique profiles
    groupby_list = columns[2:]
    unique_suitors = suitor_df.groupby(groupby_list)['filename'].count()

    #record of profiles that appeared more than once during the run
    duplicate_suitors = unique_suitors[unique_suitors>1]
    
    #return unique_suitors, duplicate_suitors, suitor_df, all_entries
    return unique_suitors, duplicate_suitors
	
male_city_names = []
unique_suitors, duplicate_suitors = check_for_duplicates("C:\\Users\\Jennifer\\Documents\\Berkeley\\W241\\Experiment\\Data_Collection\\MD\\Male_original\\Phoenix") 

duplicate_suitors = pd.DataFrame(duplicate_suitors)
total_duplicates = 0
for a in range(len(duplicate_suitors)):
    print(duplicate_suitors.iloc[a][0], ' instances of profile ', duplicate_suitors.iloc[a].name)
    total_duplicates += (duplicate_suitors.iloc[a][0] - 1)
    print()

print('Total duplicate suitor profiles: ', total_duplicates)
print()
print('Total unique suitors: ', len(unique_suitors))