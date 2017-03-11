#!/usr/local/bin/python3

import json
import pandas as pd
import os.path
import sys
import re
import imp
from enchant.checker import SpellChecker

chkr = SpellChecker("en_US-large")

pattern = re.compile(r'@\w+', re.IGNORECASE)
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

    # first do entities
    res = re.findall(pattern, training_essays_df.iloc[i]['essay'])
    training_essays_df.set_value(i, "number_of_entities", len(res))

    # next to do spell checking errors, remove entities first
    an_essay = training_essays_df.iloc[i]['essay']
    big_regex = re.compile('|'.join(map(re.escape, res)))
    without_entities_an_essay = big_regex.sub("", an_essay)
    # now count spelling errors
    chkr.set_text(without_entities_an_essay)
    num_spelling_errors = 0
    for err in chkr:
        # print ("ERROR:" , err.word)
        num_spelling_errors += 1

    training_essays_df.set_value(i, "spelling_errors", num_spelling_errors)


writer = pd.ExcelWriter(sys.argv[2])
training_essays_df.to_excel(writer, sheet_name="results",index=False)
writer.save()

# BIG ML API key - 256aab6e37fbd064edc631f862d98a3bbd219663
# BIG ML userid - riyadulepet123@gmail.com
# BIG ML password - pinecrestschool
# 0.3136
# 0.7056
# 0.0784
