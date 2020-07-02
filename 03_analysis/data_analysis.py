import pandas as pd
from scipy import stats
import numpy as np
import json

STATS_COLUMN_NAMES = {'postcode', 'year', 'property_type', 'max_price', 'min_price', 'avg_price'}

file_format = '/Users/courtneyirwin/Documents/GITREPO/House_Sales_UK/01_data/pp-complete-preprocessed-{}.csv'

def remove_outliers_by_year(df):
    '''
    :param df:
    :return: df with outliers removed
    '''
    no_rec_start = df.shape[0]
    years_in_frame = df["year_of_transfer"].unique()
    df_no_out = pd.DataFrame()
    for yr in years_in_frame:
        yr_df = df[df["year_of_transfer"] == yr].copy()
        price_index = (np.abs(stats.zscore(yr_df['price'])) < OUTLIER_DEF)
        yr_df_no_out = yr_df[price_index]
        df_no_out = pd.concat([df_no_out, yr_df_no_out])
    no_rec_end = df_no_out.shape[0]
    print("No. Records start: {}, No. Records end: {}".format(no_rec_start, no_rec_end))
    return df_no_out

def stats_by_year(pc, df):
    ''''
    Takes a dataframe of house price records, returns a dataframe of the stats by year
    '''
    stats_by_year_df = pd.DataFrame(columns=STATS_COLUMN_NAMES)
    years_in_frame = df["year_of_transfer"].unique()
    property_type_in_frame = df['property_type'].unique()
    for yr in years_in_frame:
        for pt in property_type_in_frame:
            pc_yr_dict = {}
            pc_yr_dict['postcode'] = pc
            pc_yr_dict['year'] = yr
            pc_yr_dict['property_type'] = pt
            yr_df = df[(df["year_of_transfer"] == yr) & (df["property_type"] == pt)].copy()
            pc_yr_dict['max_price'] = np.max(yr_df['price'])
            pc_yr_dict['min_price'] = np.min(yr_df['price'])
            pc_yr_dict['avg_price'] = np.mean(yr_df['price'])
            stats_by_year_df = stats_by_year_df.append(pc_yr_dict, ignore_index=True)
    return stats_by_year_df

def postcode_stats_by_year():

    all_pc_no_out = pd.DataFrame(columns=STATS_COLUMN_NAMES)

    for pc in POSTCODE_LIST:
        print("Reading data for postcode {}...".format(pc))
        pc_df = pd.read_csv(file_format.format(pc))

        #Remove Outliers
        pc_df_no_out = remove_outliers_by_year(pc_df)

        #Calculate stats
        stats = stats_by_year(pc, pc_df_no_out)

        #Add to df
        all_pc_no_out =pd.concat([all_pc_no_out, pc_df_no_out]) #adding the details for each new postcode to the list
        all_pc_no_out.to_csv('/Users/courtneyirwin/Documents/GITREPO/House_Sales_UK/01_data/stats-all_pc.csv')

if __name__ == '__main__':
    config_file = {}

    with open("../00_utils/config.json", "r") as f:
        config_file = json.load(f)

    POSTCODE_LIST = config_file.get("POSTCODES_OF_INTEREST")
    OUTLIER_DEF = config_file.get("OUTLIERS_DEF_SD")

    postcode_stats_by_year()



