#!/usr/bin/env python2.7

import re
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# from imp import reload
# import sys


# reload(sys)
# sys.setdefaultencoding('utf8')

def get_character_count(essay):
    return len(essay)

def get_word_count(essay):
    return len(re.findall(r"\s", essay))+1

def extract_features(essays, feature_functions):
    return [[f(es) for f in feature_functions] for es in essays]

def main():
    print("Reading Dataset")
    normalized_data_set = pd.DataFrame(pd.read_table('../data/normalized_data_set.tsv', encoding
= 'ISO-8859-1'))
    # randomly shuffle before splitting into training and test set
    shuffled_normalized_data_set = normalized_data_set.sample(frac=1)

    for index, row in shuffled_normalized_data_set.iterrows():
        # extract features for each essay
        shuffled_normalized_data_set.set_value(index, "character_count", get_character_count(row['essay']))
        shuffled_normalized_data_set.set_value(index, "word_count", get_word_count(row['essay']))

    train, test = train_test_split(shuffled_normalized_data_set, test_size = 0.2)

    # feature_functions = [get_character_count, get_word_count]

    essay_set_keys = train.essay_set.unique()
    for idx_essay_set in essay_set_keys:
        one_essay_set_train = train.loc[train['essay_set'] == idx_essay_set]
        one_essay_set_test = test.loc[test['essay_set'] == idx_essay_set]

        features_one_essay_set_train = []
        features_one_essay_set_test = []

        for icharacter_count, iword_count in zip(one_essay_set_train['character_count'],one_essay_set_train['word_count']):
            features_one_essay_set_train.append([icharacter_count, iword_count])
        for icharacter_count, iword_count in zip(one_essay_set_test['character_count'],one_essay_set_test['word_count']):
            features_one_essay_set_test.append([icharacter_count, iword_count])

        rf = RandomForestRegressor(n_estimators = 100)
        rf.fit(features_one_essay_set_train, one_essay_set_train["score"])
        predicted_scores = rf.predict(features_one_essay_set_test)
        one_essay_set_test['predicted_score'] = predicted_scores
        one_essay_set_test['predicted_score'] = one_essay_set_test['predicted_score'].round()
        one_essay_set_test['expected_score'] = one_essay_set_test['score'].round()
        one_essay_set_test.to_csv("test_results_"+str(idx_essay_set)+".tsv", sep='\t', encoding='ISO-8859-1', columns=['essay_set', 'essay_id', 'essay', 'score', 'expected_score', 'predicted_score'])

if __name__=="__main__":
    main()
