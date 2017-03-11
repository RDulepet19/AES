import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import PersonalityInsightsV3
import pandas as pd
import os.path
import sys
import re

reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout.flush()
pd.options.mode.chained_assignment = None
training_essays_df = pd.read_excel(open(sys.argv[1],"rb"), sheetname="training_set")
tone_analyzer = ToneAnalyzerV3(username=sys.argv[2],
  password=sys.argv[3],
  version='2016-02-11')

'''
personality_insights = PersonalityInsightsV3(
    version='2016-10-20',
    username='c5586564-27eb-4cd1-ae5c-be1f53855be6',
    password='ZuJQQ4bQ5Wnt')

profile = personality_insights.profile("text", raw_scores=True, consumption_preferences=False)
profile['needs'][0]['name'] = profile['needs'][0]['raw_score']
profile['values'][0]['name'] = profile['values'][0]['raw_score']
profile['personality'][0]['name'] = profile['personality'][0]['raw_score']
profile['personality'][0]["children"][0]['name'] = profile['personality'][0]["children"][0]['raw_score']
print(json.dumps(profile, indent=2))
'''

# initialize new feature columns
# training_essays_df["Anger"]=0

#'''
#for i in range(0, len(training_essays_df)):
# myrow = int(sys.argv[4])
transformed_df = pd.DataFrame()
first_row = int(sys.argv[4])
last_row = first_row + int(sys.argv[5])
# print "myrow start="+str(myrow)
print "lastrow="+str(last_row) +",firstrow="+str(first_row)
for i in range(first_row, last_row):
    if i > (len(training_essays_df)-1):
        break

    tone_json = None
    try:
        tone_json = tone_analyzer.tone(text=training_essays_df.iloc[i]['essay'])
        for j in range(0, len(tone_json["document_tone"]["tone_categories"])):
            tone_category_tones_json = tone_json["document_tone"]["tone_categories"][j]["tones"]
            for k in range(0, len(tone_category_tones_json)):
                training_essays_df.set_value(i, tone_category_tones_json[k]["tone_name"], tone_category_tones_json[k]["score"])
                # print str(training_essays_df.iloc[i][tone_category_tones_json[k]["tone_name"]])
                # training_essays_df.iloc[0][[3,4,5,6]].values
                # print(training_essays_df.iloc[1][7:].values)
    except Exception as e:
        print "ERROR i="+str(i)
        print "\t" + str(e)
        print "\t"+training_essays_df.iloc[i]['essay']
        pass

    transformed_df = transformed_df.append(training_essays_df.iloc[i])
'''
for i in range(0, len(training_essays_df)):
    print(training_essays_df.iloc[i][[0,1,7,8,9,10,11,12,13,14,15,16,17,18,19]].values)
'''
writer = pd.ExcelWriter(sys.argv[2]+"_tone_results.xlsx")
transformed_df.to_excel(writer, sheet_name="results",index=False)
writer.save()
