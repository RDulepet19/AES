#!/usr/local/bin/python3

import json
import pandas as pd
import os.path
import sys
import re
import imp
from textstat.textstat import textstat

# imp.reload(sys)
# sys.setdefaultencoding('utf8')
# sys.stdout.flush()
pd.options.mode.chained_assignment = None
training_essays_df = pd.read_excel(open(sys.argv[1],"rb"), sheetname="results")

first_row = int(sys.argv[3])
last_row = first_row + int(sys.argv[4])
# print "myrow start="+str(myrow)
#print "lastrow="+str(last_row) +",firstrow="+str(first_row)
for i in range(first_row, last_row):
    if i > (len(training_essays_df)-1):
        break
    training_essays_df.set_value(i, "syllable_count", textstat.syllable_count(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "lexicon_count", textstat.lexicon_count(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "sentence_count", textstat.sentence_count(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "flesch_reading_ease", textstat.flesch_reading_ease(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "smog_index", textstat.smog_index(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "flesch_kincaid_grade", textstat.flesch_kincaid_grade(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "coleman_liau_index", textstat.coleman_liau_index(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "automated_readability_index", textstat.automated_readability_index(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "dale_chall_readability_score", textstat.dale_chall_readability_score(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "difficult_words", textstat.difficult_words(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "linsear_write_formula", textstat.linsear_write_formula(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "gunning_fog", textstat.gunning_fog(training_essays_df.iloc[i]['essay']))
    training_essays_df.set_value(i, "text_standard", textstat.text_standard(training_essays_df.iloc[i]['essay']))

writer = pd.ExcelWriter(sys.argv[2])
training_essays_df.to_excel(writer, sheet_name="results",index=False)
writer.save()
