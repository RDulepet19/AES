#!/usr/bin/env python2.7

import re
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

import sys
from imp import reload
sys.path.insert(0, "../Evaluation_Metrics/Python/score")
import score
reload(score)


# from imp import reload
# import sys


# reload(sys)
# sys.setdefaultencoding('utf8')

def main():
    print("Reading test results")
    combined_predicted_test_results = pd.DataFrame(pd.read_table(sys.argv[1], encoding
= 'ISO-8859-1'))

    essay_set_keys = combined_predicted_test_results.essay_set.unique()
    
    essay_set_kappa_scores = []

    for idx_essay_set in essay_set_keys:
        kappa_score = score.quadratic_weighted_kappa(combined_predicted_test_results[combined_predicted_test_results.essay_set == idx_essay_set]['predicted_score'].tolist(), combined_predicted_test_results[combined_predicted_test_results.essay_set == idx_essay_set]['expected_score'].tolist())
        essay_set_kappa_scores.append(kappa_score)
        print("quadratic_weighted_kappa for essay_set="+str(idx_essay_set)+" = "+ str(kappa_score))

    # generated
    combined_kappa_score = score.mean_quadratic_weighted_kappa(essay_set_kappa_scores)
    print("\n\n==============combined_quadratic_weighted_kappa for entire dataset = "+str(combined_kappa_score))
if __name__=="__main__":
    main()
