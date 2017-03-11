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
sys.argv.append("extractEssayPersonalityFeatures.py")
sys.argv.append("temp_training_set_riya.xlsx")
sys.argv.append("e255c8ca-9f1d-4c98-87cb-c33dd4f3f776")
sys.argv.append("MLDt74fuvrhh")
sys.argv.append("0")
sys.argv.append("1")
sys.argv.append("e255c8ca-9f1d-4c98-87cb-c33dd4f3f776")

# this for multiple instances using REGEX
# copy from excel userid/password/start/endrow to text file (ATOM, TEXTWRANGLER, VI etc)
# replace TAB (\t) with SPACE
# replace the ^ the prefix "nohup python extractEssayPersonalityFeatures.py training_set_riya.xlsx "
# replace ^(.*) (.*) (.*) (.*) (.*) (.*) (.*) (.*)$ with $1 $2 $3 $4 $5 $6 $7 $8 </dev/null >$5.log 2>&1 &
'''

personality_insights = PersonalityInsightsV3(
    version='2016-10-20',
    username=sys.argv[2],
    password=sys.argv[3])
'''
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

    profile_json = None
    try:
        profile_json = personality_insights.profile(training_essays_df.iloc[i]['essay'], raw_scores=True, consumption_preferences=False)
        for j in range(0, len(profile_json["needs"])):
            training_essays_df.set_value(i, "needs_"+profile_json['needs'][j]['name'], profile_json['needs'][j]['raw_score'])
        for j in range(0, len(profile_json["values"])):
            training_essays_df.set_value(i, "values_"+profile_json['values'][j]['name'], profile_json['values'][j]['raw_score'])
        for j in range(0, len(profile_json["personality"])):
            training_essays_df.set_value(i, "personality_"+profile_json['personality'][j]['name'], profile_json['personality'][j]['raw_score'])

            personality_children = profile_json['personality'][j]["children"]

            for k in range(0, len(personality_children)):
                training_essays_df.set_value(i, "personality_"+profile_json['personality'][j]['name'] + "_" + personality_children[k]['name'], personality_children[k]['raw_score'])
    except Exception as e:
        print "ERROR i="+str(i)
        print "\t" + str(e)
        print "\t"+training_essays_df.iloc[i]['essay']
        pass

    transformed_df = transformed_df.append(training_essays_df.iloc[i])

writer = pd.ExcelWriter(sys.argv[2]+"_tone_results.xlsx")
transformed_df.to_excel(writer, sheet_name="results",index=False)
writer.save()
