#!/usr/local/bin/python3

import json
import pandas as pd
import os.path
import sys
import re
import imp
from textstat.textstat import textstat
from collections import Counter
from numpy import power

# imp.reload(sys)
# sys.setdefaultencoding('utf8')
# sys.stdout.flush()
pd.options.mode.chained_assignment = None
training_essays_df = pd.read_excel(open(sys.argv[1],"rb"), sheetname="data")

def get_character_count(essay):
    return len(essay)

def get_word_count(essay):
    return len(re.findall(r"\s", essay))+1

def get_nchar_word_count(essay, nchar):
	return len([word for word in essay.split() if len(word) == nchar])

first_row = int(sys.argv[3])
last_row = first_row + int(sys.argv[4])
# print "myrow start="+str(myrow)
#print "lastrow="+str(last_row) +",firstrow="+str(first_row)
for i in range(first_row, last_row):
    if i > (len(training_essays_df)-1):
        break
    training_essays_df.set_value(i, "character_count", get_character_count(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "word_count", get_word_count(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "5char_count", get_nchar_word_count(training_essays_df.iloc[i]['essay'], 5))
    training_essays_df.set_value(i, "6char_count", get_nchar_word_count(training_essays_df.iloc[i]['essay'], 6))
    training_essays_df.set_value(i, "7char_count", get_nchar_word_count(training_essays_df.iloc[i]['essay'], 7))
    training_essays_df.set_value(i, "8char_count", get_nchar_word_count(training_essays_df.iloc[i]['essay'], 8))
    training_essays_df.set_value(i, "unique_words_count", len(Counter(training_essays_df.iloc[i]['essay'].split())))
    training_essays_df.set_value(i, "fourth_root_word_count", int(round(power(len(training_essays_df.iloc[i]['essay'].split()), (1/4)))))
writer = pd.ExcelWriter(sys.argv[2])
training_essays_df.to_excel(writer, sheet_name="results",index=False)
writer.save()
