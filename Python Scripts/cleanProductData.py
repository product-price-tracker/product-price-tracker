from getProductData import get_now_string, get_data_for_product
import os
import pandas as pd
import sys
import numpy as np

def loadData(path):
    return pd.read_pickle(path)

def get_clean_path(asin):
    return '../Data/Clean/{}/{}.pkl'.format(get_now_string(), asin)

def get_clean_data_for_product(asin):
    df = get_data_for_product(asin)
    clean_path = get_clean_path(asin)

    if not os.path.isfile(clean_path):

        # Store first non-null values for each col

        first_vals = {}
        for index, row in df.iterrows():
            for column in df.columns:
                if column not in first_vals:
                    if not pd.isna(row[column]):
                        first_vals[column] = row[column]

        # Fill out first null values with first value
        reached_first_vals = {}
        for column in df.columns:
            reached_first_vals[column] = False

        for i in range(len(df)):
            for column in df.columns:
                if not reached_first_vals[column]:
                    if pd.isna(df.iloc[i][column]):
                        if column in first_vals:
                            df[column].iloc[i] = first_vals[column]
                        else: # If all nulls—i.e. no price history, set to 100000 (fake value).
                            df[column].iloc[i] = 100000

                    else:
                        reached_first_vals[column] = True

        # For each Non-starting null sequence, replace null with previous value.
        last_vals = {}
        for column in df.columns:
            if column in first_vals:
                last_vals[column] = first_vals[column]
            else:
                last_vals[column] = None

        for i in range(len(df)):
            for column in df.columns:
                if pd.isna(df.iloc[i][column]):
                    df[column].iloc[i] = last_vals[column]
                else:
                    last_vals[column] = df.iloc[i][column]

        # Cleaning Counts (if -1, set to 0 b/c none.)
        counts = ['COUNT_NEW', 'COUNT_USED']
        for count in counts:
            if count in df.columns:
                new_count = df[count].replace(to_replace = -1, value = 0)
                df[count] = new_count

        # Adding MIN_UNUSED
        df['MIN_UNUSED'] = df[['NEW', 'AMAZON']].min(axis=1)
        # print(df.isna().sum().sum())
        assert df.isna().sum().sum() == 0
        clean_date_path = '../Data/Clean/{}'.format(get_now_string())
        if not os.path.isdir(clean_date_path):
            os.mkdir(clean_date_path)
        df.to_pickle(get_clean_path(asin))
    else:
        df = pd.read_pickle(clean_path)
    print(df)
    return df


if __name__ == '__main__':
    get_clean_data_for_product('B07C2PYWGZ')
