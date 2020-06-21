import os
import json
import pandas as pd
import time

def preprocess_data(pc_list):
    start = time.time()

    df = pd.read_csv(DATAFILE, header=None)
    ch_time1 = time.time()
    print("Dataframe read in {}".format(ch_time1 - start))

    df = df.rename(columns=HEADINGS)
    ch_time2 = time.time()
    print("Dataframe renamed at {}".format(ch_time2 - start))

    for pc in pc_list:
        pc_start = time.time()
        pc_df = pd.DataFrame()
        pc_df = df[df['postcode'].str.contains(pc, na=False)].copy()
        pc_df["year_of_transfer"] = pc_df['date_of_transfer'].apply(lambda x: x.split('-')[0])
        pc_df.to_csv('/Users/courtneyirwin/Documents/GITREPO/House_Sales_UK/01_data/pp-complete-preprocessed-{}.csv'.format(pc))
        pc_end = time.time()
        print("Time for postcode {} was {}".format(pc, (pc_end - pc_start)))
    end = time.time()

    print("Total time: {}".format((end-start)))

if __name__ == '__main__':
    print(os.getcwd())
    config_file= {}

    with open("../00_utils/config.json", "r") as f:
        config_file = json.load(f)

    DATAFILE = config_file.get("RAW_DATA_INPUT_FILE_PATH")
    HEADINGS = config_file.get("RAW_DATA_INPUT_FILE_HEADINGS")
    POSTCODE_LIST = config_file.get("POSTCODES_OF_INTEREST")

    preprocess_data(POSTCODE_LIST)

