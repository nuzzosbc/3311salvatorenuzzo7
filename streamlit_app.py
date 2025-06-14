
# Salvatore Nuzzo
# CSCI 3311 File 7A Term Project Dashboard Streamlit-enhanced version
# June 13, 2025

# Term Project Dashboard

import altair
import datetime
import pandas
import pickle
import streamlit

def cleaning(df):
    df_clean = df
    df_clean = df_clean.drop('Note', axis = 'columns')
    df_clean = df_clean.melt(id_vars = ['Country Code', 'IMF Country Code', 'Country', 'Indicator Type', 'Series Name'], var_name = 'Year', value_name = 'Inflation')
    df_clean['Year'] = df_clean['Year'].apply(lambda row: pandas.to_datetime(row, format = "%Y"))
    return df_clean

# Line chart showing inflation over time for a specified country, full range of years
def part1(df_clean, country):
    zoom = altair.selection_interval(bind = 'scales')
    df_clean_2 = df_clean[df_clean['Country'] == country]
    chart = altair.Chart(df_clean_2).mark_line(point = True).properties(title = f"Inflation in {country}").configure_point(size = 75).encode(
        altair.X('Year:T'),
        altair.Y('Inflation:Q'),
        tooltip = [altair.Tooltip('Year:T', format = "%Y"), altair.Tooltip('Inflation:Q')]
    ).add_params(
        zoom
    )
    return chart

# Scatter plot comparing two inflation measures for a given country through the years
def part2(df1_clean, df2_clean, country, suffix1, suffix2):
    name1 = suffix1 + " Inflation"
    name2 = suffix2 + " Inflation"
    col_name_1 = "Inflation " + suffix1 + ":Q"
    col_name_2 = "Inflation " + suffix2 + ":Q"
    zoom = altair.selection_interval(bind = 'scales')
    if df1_clean.equals(df2_clean):
        chart = altair.Chart(df1_clean).mark_point().properties(title = f"{name1} vs {name2}: {country}").encode(
            altair.X('Inflation:Q', title = name1),
            altair.Y('Inflation:Q', title = name2),
            altair.Color('Year:T', timeUnit = 'year', title = 'Year').scale(scheme = altair.SchemeParams(name = 'yellowgreenblue', extent = [-1, 2])),
            tooltip = [altair.Tooltip('Year:T', format = "%Y"), altair.Tooltip(col_name_1), altair.Tooltip(col_name_2)]
        ).add_params(
            zoom
        )
    else:
        df_combined = pandas.merge(df1_clean, df2_clean, on = ["Country Code", "Year"], how = "left", suffixes = (" " + suffix1, " " + suffix2))
        df_combined = df_combined[df_combined['Country ' + suffix1] == country]
        chart = altair.Chart(df_combined).mark_point().properties(title = f"{name1} vs {name2}: {country}").encode(
            altair.X(col_name_1, title = name1),
            altair.Y(col_name_2, title = name2),
            altair.Color('Year:T', timeUnit = 'year', title = 'Year').scale(scheme = altair.SchemeParams(name = 'yellowgreenblue', extent = [-1, 2])),
            tooltip = [altair.Tooltip('Year:T', format = "%Y"), altair.Tooltip(col_name_1), altair.Tooltip(col_name_2)]
        ).add_params(
            zoom
        )
    return chart

# Bar chart showing inflation levels in a given year for the countries selected
def part3(df_clean, year, countries):
    df_clean_2 = df_clean[df_clean['Year'] == pandas.to_datetime(str(year), format = "%Y")]
    df_clean_2 = df_clean_2[df_clean_2['Country'].isin(countries)]
    chart = altair.Chart(df_clean_2).mark_bar().properties(title = f"Inflation by country, {year}").encode(
        altair.X('Inflation:Q'),
        altair.Y('Country:N'),
        altair.Tooltip(['Country:N', 'Inflation:Q'])
    )
    return chart

streamlit.set_page_config(page_title = "Term Project Dashboard")

streamlit.title("Term Project Dashboard")

streamlit.write("**Visualizing Global Inflation: Multiple metrics since 1970**")
streamlit.write("Salvatore Nuzzo")
streamlit.write("CSCI 3311 - June 13, 2025")

df_file = open('DF1_3311_SalvatoreNuzzo.bin', 'rb')
df_dict = pickle.load(df_file)
df_file.close()
df_hcpia = df_dict['df_hcpia']
df_fcpia = df_dict['df_fcpia']
df_ecpia = df_dict['df_ecpia']
df_ccpia = df_dict['df_ccpia']
df_ppia = df_dict['df_ppia']
df_defa = df_dict['df_defa']
df_hcpia_clean = cleaning(df_hcpia)
df_fcpia_clean = cleaning(df_fcpia)
df_ecpia_clean = cleaning(df_ecpia)
df_ccpia_clean = cleaning(df_ccpia)
df_ppia_clean = cleaning(df_ppia)

streamlit.write("I will add instructions for the user here.")

streamlit.sidebar.header("Filters")
year_range = streamlit.sidebar.slider("Select range of years to include", datetime.datetime(1970, 1, 1), datetime.datetime(2024, 1, 1), (datetime.datetime(1970, 1, 1), datetime.datetime(2024, 1, 1)), format = "YYYY")

filtered_df_hcpia_clean = df_hcpia_clean[df_hcpia_clean['Year'].between(*year_range)]
filtered_df_fcpia_clean = df_fcpia_clean[df_fcpia_clean['Year'].between(*year_range)]
filtered_df_ecpia_clean = df_ecpia_clean[df_ecpia_clean['Year'].between(*year_range)]
filtered_df_ccpia_clean = df_ccpia_clean[df_ccpia_clean['Year'].between(*year_range)]
filtered_df_ppia_clean = df_ppia_clean[df_ppia_clean['Year'].between(*year_range)]

country = streamlit.sidebar.selectbox("Select a country for the first two charts", options = filtered_df_hcpia_clean['Country'].unique(), index = 190)

streamlit.write("**Inflation over time for a particular country**")

inf_measure_1 = streamlit.selectbox("Select an inflation metric", options = ['HCPI', 'FCPI', 'ECPI', 'CCPI', 'PPI'])
if inf_measure_1 == "HCPI":
    df_to_use_1 = filtered_df_hcpia_clean
elif inf_measure_1 == "FCPI":
    df_to_use_1 = filtered_df_fcpia_clean
elif inf_measure_1 == "ECPI":
    df_to_use_1 = filtered_df_ecpia_clean
elif inf_measure_1 == "CCPI":
    df_to_use_1 = filtered_df_ccpia_clean
elif inf_measure_1 == "PPI":
    df_to_use_1 = filtered_df_ppia_clean

streamlit.altair_chart(part1(df_to_use_1, country), use_container_width = True)

streamlit.write("**Scatter plot comparing two inflation measures for a particular country through the years**")

inf_measure_2 = streamlit.selectbox("Select first inflation metric", options = ['HCPI', 'FCPI', 'ECPI', 'CCPI', 'PPI'], index = 0)
if inf_measure_2 == "HCPI":
    df_to_use_1 = filtered_df_hcpia_clean
elif inf_measure_2 == "FCPI":
    df_to_use_1 = filtered_df_fcpia_clean
elif inf_measure_2 == "ECPI":
    df_to_use_1 = filtered_df_ecpia_clean
elif inf_measure_2 == "CCPI":
    df_to_use_1 = filtered_df_ccpia_clean
elif inf_measure_2 == "PPI":
    df_to_use_1 = filtered_df_ppia_clean

inf_measure_3 = streamlit.selectbox("Select second inflation metric", options = ['HCPI', 'FCPI', 'ECPI', 'CCPI', 'PPI'], index = 1)
if inf_measure_3 == "HCPI":
    df_to_use_2 = filtered_df_hcpia_clean
elif inf_measure_3 == "FCPI":
    df_to_use_2 = filtered_df_fcpia_clean
elif inf_measure_3 == "ECPI":
    df_to_use_2 = filtered_df_ecpia_clean
elif inf_measure_3 == "CCPI":
    df_to_use_2 = filtered_df_ccpia_clean
elif inf_measure_3 == "PPI":
    df_to_use_2 = filtered_df_ppia_clean

streamlit.altair_chart(part2(df_to_use_1, df_to_use_2, country, inf_measure_2, inf_measure_3), use_container_width = True)

streamlit.write("**Bar chart showing inflation levels in a particular year for the countries selected**")

inf_measure_1 = streamlit.selectbox("Select an inflation metric", options = ['HCPI', 'FCPI', 'EPCI', 'CCPI', 'PPI'])
if inf_measure_1 == "HCPI":
    df_to_use_1 = df_hcpia_clean
elif inf_measure_1 == "FCPI":
    df_to_use_1 = df_fcpia_clean
elif inf_measure_1 == "ECPI":
    df_to_use_1 = df_ecpia_clean
elif inf_measure_1 == "CCPI":
    df_to_use_1 = df_ccpia_clean
elif inf_measure_1 == "PPI":
    df_to_use_1 = df_ppia_clean

year_to_use = streamlit.slider("Select a year", 1970, 2024, 2024)

countries = streamlit.multiselect("Select the countries to plot", options = filtered_df_hcpia_clean['Country'].unique())

if len(countries) > 0:
    streamlit.altair_chart(part3(df_to_use_1, year_to_use, countries), use_container_width = True)
else:
    streamlit.write("Select countries above to see the plot")

