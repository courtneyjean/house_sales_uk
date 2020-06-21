import numpy as np
import pandas as pd
import streamlit as st

PC_STAT_FILE = '/Users/courtneyirwin/Documents/GITREPO/House_Sales_UK/01_data/stats-all_pc.csv'
STATS_COLUMN_NAMES = {'postcode', 'year', 'max_price', 'min_price', 'avg_price'}


if __name__ == '__main__':
    stats_df = pd.read_csv(PC_STAT_FILE)
    st.title('Exploring London house price growth over time')

    #Select a suburb
    suburb = st.multiselect('Which suburb do you want to explore?',list(stats_df['postcode'].unique()),
                            default=pd.unique(stats_df['postcode']))
    st.write('Prices in ', ', '.join(suburb), ' over time')

    #Filter by the selected suburb
    stats_df = stats_df[stats_df['postcode'].isin(suburb)]

    #Property type
    pt = st.multiselect('What property type?', list(stats_df['property_type'].unique()),
                        default= stats_df['property_type'].unique())
    st.write("D = Detached, S = Semi-Detached, T = Terraced, F = Flats/Maisonettes, O = Other")
    st.write('Property type', ', '.join(pt), ' over time')

    # Filter by the property type
    stats_df = stats_df[(stats_df['property_type'].isin(pt))]

    #Set up a slide for a time filter

    pt_slider_min_val = stats_df['year'].min()
    pt_slider_max_val = stats_df['year'].max()
    pt_slider_values = [pt_slider_min_val, pt_slider_max_val]

    time_period = st.slider("Over what time period?",
                                   min_value=pt_slider_min_val, max_value=pt_slider_max_val,
                            value=pt_slider_values, step=None, format=None, key=None)

    #Filter by the selected time period
    stats_df = stats_df[(stats_df['year'] > time_period[0]) &
                                      (stats_df['year'] < time_period[1])]

    # Required format for streamlit chat: Index = year, columns = min, max, average
    st.line_chart(stats_df.groupby(['year']).mean()[['avg_price', "min_price", "max_price"]])
    st.write(stats_df.groupby(['year']).mean()[['avg_price', "min_price", "max_price"]])

