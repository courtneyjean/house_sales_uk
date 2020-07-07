import numpy as np
import pandas as pd
import streamlit as st

PC_STAT_FILE = '../01_data/stats-all_pc.csv'
STATS_COLUMN_NAMES = {'postcode', 'year', 'max_price', 'min_price', 'avg_price'}

@st.cache
def load_data():
    df = pd.read_csv(PC_STAT_FILE)
    return df

if __name__ == '__main__':

    stats_df = load_data()
    st.title('Exploring London house price growth over time')

    #Select a suburb
    suburb_pcs = st.multiselect('Which suburb do you want to explore?',list(stats_df['postcode'].unique()),
                            default=pd.unique(stats_df['postcode']))
    st.write('Prices in ', ', '.join(suburb_pcs), ' over time')

    #Filter by the selected suburb
    stats_df = stats_df[stats_df['postcode'].isin(suburb_pcs)]

    #Property type
    pt = st.radio('What property type?', list(stats_df['property_type'].unique()))
    st.write("D = Detached, S = Semi-Detached, T = Terraced, F = Flats/Maisonettes, O = Other")

    # Filter by the property type
    stats_df = stats_df[(stats_df['property_type'] == pt)]

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

    #Radio button for reported price
    reported_price = st.radio("Which prices are you interested in reporting for each year?",
                              ("Maximum", "Minimum", "Average"), index=2)

    #Set the default as average price
    selected_reported_price = "avg_price"
    #update if the other options are selected
    if reported_price == "Maximum":
        selected_reported_price = "max_price"
    if reported_price == "Minimum":
        selected_reported_price = "min_price"

    # Required format for streamlit chat: Index = year, columns = postcode, filtered by selected_reported_price
    graphing_data = pd.pivot_table(stats_df, values=selected_reported_price, index='year', columns='postcode',
                                   aggfunc=np.sum)
    flattened = pd.DataFrame(graphing_data.to_records())
    flattened.set_index(['year'], inplace=True)
    st.line_chart(flattened)
    st.write(flattened)


