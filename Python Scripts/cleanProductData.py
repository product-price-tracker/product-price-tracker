import pandas as pd

def loadData(path):
    return pd.read_pickle(path)

def cleanProductData(asin):
    df = loadData('../Data/{}.pkl'.format(asin))
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
                    df[column].iloc[i] = first_vals[column]
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



    # print(df.isna().sum().sum())
    assert df.isna().sum().sum() == 0
    return df

def save_clean_data_for_product(asin):
    df = cleanProductData(asin)
    df.to_pickle('../Data/Clean/{}.pkl'.format(asin))
    print(df)

if __name__ == '__main__':
    save_clean_data_for_product('B00BWU3HNY')
