import os
import json
import pandas as pd
import time

def preprocess_data(pc_list):
    start = time.time()

    df = pd.DataFrame()

    chunksize = 3000

    for chunk in pd.read_csv(DATAFILE, header=None, low_memory=False, chunksize=chunksize):
        ch_time1 = time.time()
        print("Dataframe chunk read in {}".format(ch_time1 - start))
        for pc in pc_list:
            pc_start = time.time()
            pc_df = pd.DataFrame()
            pc_df = chunk[chunk[13].str.contains(pc, na=False)].copy() #filter only postcodes of interest
            df = pd.concat([df, pc_df])
    print(df.head())
    df = df.rename(columns=HEADINGS)
    print(df.head())
    df["year_of_transfer"] = df["date_of_transfer"].apply(lambda x: x.split('-')[0])  # date of transfer
    df.to_csv('/Users/courtneyirwin/Documents/GITREPO/House_Sales_UK/01_data/pp-complete-preprocessed-ALL.csv'.format(pc))
    end = time.time()
    print("Total time: {}".format((end-start)))

if __name__ == '__main__':
    print(os.getcwd())
    config_file= {}

    with open("../00_utils/config.json", "r") as f:
        config_file = json.load(f)

    DATAFILE = config_file.get("RAW_DATA_INPUT_FILE_PATH")
    DATAFILETYPES = config_file.get("RAW_DATA_INPUT_FILE_TYPES")
    HEADINGS = config_file.get("RAW_DATA_INPUT_FILE_HEADINGS")
    POSTCODE_LIST = config_file.get("POSTCODES_OF_INTEREST")

    preprocess_data(POSTCODE_LIST)

