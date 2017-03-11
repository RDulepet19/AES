#!/usr/bin/env python2.7

import re
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pickle

# from imp import reload
# import sys


# reload(sys)
# sys.setdefaultencoding('utf8')

global_one_essay_set_train = None
global_features_one_essay_set_train = None
global_rf = None


def selectKImportance(model, X, k=5):
     return X[:,model.feature_importances_.argsort()[::-1][:k]]

def extract_features(essays, feature_functions):
    return [[f(es) for f in feature_functions] for es in essays]

def main():
    global global_one_essay_set_train
    global global_features_one_essay_set_train
    global global_rf

    print("Reading Dataset")
    # normalized_data_set = pd.DataFrame(pd.read_table('../data/normalized_data_set.tsv', encoding = 'ISO-8859-1'))
    watson_readability_spelling_entities_features_dataset = pd.read_excel('./watson_readability_spelling_entities_features_data_set.xlsx')
    basic_stats_features_dataset = pd.read_excel('./essay_basic_stats_features_data_set.xlsx')
    
    merged_features_dataset = pd.merge(basic_stats_features_dataset, watson_readability_spelling_entities_features_dataset, on=['essay_set','essay_id'])

    # merged_features_dataset = basic_stats_features_dataset

    # randomly shuffle before splitting into training and test set
    shuffled_merged_features_dataset = merged_features_dataset.sample(frac=1)

    '''
        for index, row in shuffled_normalized_data_set.iterrows():
            # extract features for each essay
            shuffled_normalized_data_set.set_value(index, "character_count", get_character_count(row['essay']))
            shuffled_normalized_data_set.set_value(index, "word_count", get_word_count(row['essay']))
        # feature_functions = [get_character_count, get_word_count]
    '''
    train, test = train_test_split(shuffled_merged_features_dataset, test_size = 0.2)

    test_result_files = []

    essay_set_keys = train.essay_set.unique()
    for idx_essay_set in essay_set_keys:
        one_essay_set_train = train.loc[train['essay_set'] == idx_essay_set]
        one_essay_set_test = test.loc[test['essay_set'] == idx_essay_set]

        rf = RandomForestRegressor(n_estimators = 1000, max_features = 50)
        exclude_features = ['essay_set', 'essay_id', 'essay', 'score'] #, 'character_count', 'word_count', '5char_count', '6char_count', '7char_count', '8char_count', 'unique_words_count', 'fourth_root_word_count', 'flesch_reading_ease', 'smog_index', 'flesch_kincaid_grade', 'coleman_liau_index', 'automated_readability_index', 'dale_chall_readability_score', 'difficult_words', 'linsear_write_formula', 'gunning_fog']
        # rf.fit(features_one_essay_set_train, one_essay_set_train["score"])
        features_one_essay_set_train = one_essay_set_train.ix[:, one_essay_set_train.columns.difference(exclude_features)]
        rf.fit(features_one_essay_set_train.values, one_essay_set_train["score"])

        output_model = open("./model_essay_set_"+str(idx_essay_set)+".mb", 'wb')
        pickle.dump(rf, output_model)
        output_model.close()
        
        '''
        global_one_essay_set_train = one_essay_set_train
        global_features_one_essay_set_train = features_one_essay_set_train
        global_rf = rf

        top_features_one_essay_set_train = selectKImportance(rf, features_one_essay_set_train.values, 50)
        '''
        # rf_top_features = RandomForestRegressor(n_estimators = 100)
        # rf_top_features.fit(top_features_one_essay_set_train, one_essay_set_train["score"])
        # print("===IMPORTANT FEATURES====\n\t",rf.feature_importances_)
        # print("Features sorted by their score:")
        # print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), list(global_one_essay_set_train.columns)[4:],reverse=True)))

        # predicted_scores = rf.predict(features_one_essay_set_test)
        
        predicted_scores = rf.predict(one_essay_set_test.ix[:, one_essay_set_test.columns.difference(exclude_features)])
        one_essay_set_test['predicted_score'] = predicted_scores
        one_essay_set_test['predicted_score'] = one_essay_set_test['predicted_score'].round()
        one_essay_set_test['expected_score'] = one_essay_set_test['score'].round()
        # one_essay_set_test.to_csv("test_results_"+str(idx_essay_set)+".tsv", sep='\t', encoding='ISO-8859-1', columns=['essay_set', 'essay_id', 'score', 'expected_score', 'predicted_score'])
        writer = pd.ExcelWriter("./test_results_"+str(idx_essay_set)+".xlsx")
        one_essay_set_test.to_excel(writer, sheet_name="results", index=False, columns=['essay_set', 'essay_id', 'score', 'expected_score', 'predicted_score'])
        writer.save()
        test_result_files.append("./test_results_"+str(idx_essay_set)+".xlsx")

    # combine all test result files into a single file
    combined_test_results_df = pd.DataFrame()
    for a_file in test_result_files:
        a_test_result_df = pd.read_excel(a_file)
        combined_test_results_df = pd.concat([combined_test_results_df, a_test_result_df])
    # write combined file to output
    combined_test_results_df.to_csv("./combined_test_results.tsv", sep='\t', encoding='ISO-8859-1', index=False)
if __name__=="__main__":
    main()
