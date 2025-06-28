
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

def part1a(df_clean, country):
    df_clean_2 = df_clean[df_clean['Country'] == country]
    df_clean_2 = df_clean_2[['Year', 'Inflation']]
    return df_clean_2

# Scatter plot comparing two inflation measures for a given country through the years
def part2(df1_clean, df2_clean, country, suffix1, suffix2):
    name1 = suffix1 + " Inflation"
    name2 = suffix2 + " Inflation"
    col_name_1 = "Inflation " + suffix1 + ":Q"
    col_name_2 = "Inflation " + suffix2 + ":Q"
    zoom = altair.selection_interval(bind = 'scales')
    if df1_clean.equals(df2_clean):
        df1_clean = df1_clean[df1_clean['Country'] == country]
        chart = altair.Chart(df1_clean).mark_point().properties(title = f"{name1} vs {name2}: {country}").encode(
            altair.X('Inflation:Q', title = name1),
            altair.Y('Inflation:Q', title = name2),
            altair.Color('Year:T', timeUnit = 'year', title = 'Year').scale(scheme = altair.SchemeParams(name = 'yellowgreenblue', extent = [-1, 2])),
            tooltip = [altair.Tooltip('Year:T', format = "%Y"), altair.Tooltip('Inflation:Q'), altair.Tooltip('Inflation:Q')]
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

def part2a(df1_clean, df2_clean, country, suffix1, suffix2):
    if df1_clean.equals(df2_clean):
        df_display = df1_clean
        df_display = df_display[df_display['Country'] == country]
        df_display = df_display[['Year', 'Inflation']]
    else:
        df_combined = pandas.merge(df1_clean, df2_clean, on = ["Country Code", "Year"], how = "left", suffixes = (" " + suffix1, " " + suffix2))
        df_combined = df_combined[df_combined['Country ' + suffix1] == country]
        df_display = df_combined
        df_display = df_display[['Year', 'Inflation ' + suffix1, 'Inflation ' + suffix2]]
    return df_display

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

def part3a(df_clean, year, countries):
    df_clean_2 = df_clean[df_clean['Year'] == pandas.to_datetime(str(year), format = "%Y")]
    df_clean_2 = df_clean_2[df_clean_2['Country'].isin(countries)]
    df_clean_2 = df_clean_2[['Country', 'Inflation']]
    return df_clean_2

def parts1and2alt(df1_clean, df2_clean, country, suffix1, suffix2):    
    brush = altair.selection_interval(encodings = ['x'])
    conditional = altair.when(brush).then(altair.value(1.0)).otherwise(altair.value(0.4))
    df1_clean_2 = df1_clean[df1_clean['Country'] == country]
    line_chart = altair.Chart(df1_clean_2).mark_line(point = True).properties(title = f"Inflation in {country}").encode(
        altair.X('Year:T'),
        altair.Y('Inflation:Q'),
        tooltip = [altair.Tooltip('Year:T', format = "%Y"), altair.Tooltip('Inflation:Q')],
        opacity = conditional
    ).add_params(
        brush
    )
    
    zoom = altair.selection_interval(bind = 'scales')
    name1 = suffix1 + " Inflation"
    name2 = suffix2 + " Inflation"
    col_name_1 = "Inflation " + suffix1 + ":Q"
    col_name_2 = "Inflation " + suffix2 + ":Q"
    if df1_clean.equals(df2_clean):
        scatterplot = altair.Chart(df1_clean).mark_point().properties(title = f"{name1} vs {name2}: {country}").encode(
            altair.X('Inflation:Q', title = name1),
            altair.Y('Inflation:Q', title = name2),
            altair.Color('Year:T', timeUnit = 'year', title = 'Year').scale(scheme = altair.SchemeParams(name = 'yellowgreenblue', extent = [-1, 2])),
            tooltip = [altair.Tooltip('Year:T', format = "%Y"), altair.Tooltip(col_name_1), altair.Tooltip(col_name_2)],
            opacity = altair.condition(brush, altair.value(0.8), altair.value(0.05))
        ).add_params(
            zoom
        )
    else:
        df_combined = pandas.merge(df1_clean, df2_clean, on = ["Country Code", "Year"], how = "left", suffixes = (" " + suffix1, " " + suffix2))
        df_combined = df_combined[df_combined['Country ' + suffix1] == country]
        scatterplot = altair.Chart(df_combined).mark_point().properties(title = f"{name1} vs {name2}: {country}").encode(
            altair.X(col_name_1, title = name1),
            altair.Y(col_name_2, title = name2),
            altair.Color('Year:T', timeUnit = 'year', title = 'Year').scale(scheme = altair.SchemeParams(name = 'yellowgreenblue', extent = [-1, 2])),
            tooltip = [altair.Tooltip('Year:T', format = "%Y"), altair.Tooltip(col_name_1), altair.Tooltip(col_name_2)],
            opacity = altair.condition(brush, altair.value(0.8), altair.value(0.05))
        ).add_params(
            zoom
        )
    
    return altair.vconcat(line_chart, scatterplot).configure_point(size = 75)

streamlit.set_page_config(page_title = "Term Project Dashboard - Inflation")

streamlit.title("Visualizing Global Inflation")

streamlit.write("**Multiple metrics since 1970**")
streamlit.write("by Salvatore Nuzzo")
streamlit.write("CSCI 3311 - created June 13, 2025 - updated June 26, 2025")

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

streamlit.write("**Introduction**")

streamlit.write("My dashboard deals with global inflation since 1970, as reported in the metrics below. This gives the meaning of the acronyms used throughout. Inflation for all measures is reported on an annual basis, in percentage points.")
streamlit.write("HCPI - Headline Consumer Price Index")
streamlit.write("FCPI - Food CPI")
streamlit.write("ECPI - Energy CPI")
streamlit.write("CCPI - Official Core CPI")
streamlit.write("PPI - Producer Price Index")
streamlit.write("Do you wonder how inflation has changed over time in a given country? Where has it spiked? Has it trended up or down? Are the metrics we use to measure inflation effective? Are they all more or less the same as one another, or are some more correlated than others? Does it depend on the country, or on what timeframe we are considering? This dashboard takes advantage of the World Bank's great inflation dataset, which includes inflation data around the world in a period spanning more than fifty years, measured across five different metrics. Whatever your questions, I hope you find something to interest you here.")
streamlit.write("That said, generally, the questions my dashboard explores are:")
streamlit.write("How do the differing measures of inflation compare to one another? Do they generally agree? Is this true within a specific country?")
streamlit.write("How do we see the inflation in the United States and the world changing over time?")
streamlit.write("As you use this dashboard, I encourage you to ask these kind of questions about how inflation has changed over time, or how it differs country-to-country. Due to the large number of countries included, you may have to wait some time while the data is updated to represent your selections.")
streamlit.write("To use the dashboard, follow the instructions for each chart. Use the filters at the left to control the data displayed in the first two charts.")
streamlit.write("Please note that while you may select any metrics and combinations of data to diplay that you would like, not all inflation metrics are available for all countries in the full year range. The default inflation metric is HCPI, which is generally more supported, but feel free to experiment trying whichever metrics you would like. Note also that for some countries, not all years in inflation are available regardless of the metric, and there may be some gaps in the data presented. Often what may seem like errors are simply the result of missing data based on the current selections.")
streamlit.write("The source of the data is the World Bank updated [Global Database of Inflation](%s)" % "https://www.worldbank.org/en/research/brief/inflation-database")

streamlit.sidebar.header("Filters")
streamlit.sidebar.write("The options below apply to the data displayed in the first two charts, which show data for a particular country. If you are looking to compare multiple countries on inflation, use the bar chart country comparison.")
year_range = streamlit.sidebar.slider("Select range of years to include", datetime.datetime(1970, 1, 1), datetime.datetime(2024, 1, 1), (datetime.datetime(1970, 1, 1), datetime.datetime(2024, 1, 1)), format = "YYYY")

filtered_df_hcpia_clean = df_hcpia_clean[df_hcpia_clean['Year'].between(*year_range)]
filtered_df_fcpia_clean = df_fcpia_clean[df_fcpia_clean['Year'].between(*year_range)]
filtered_df_ecpia_clean = df_ecpia_clean[df_ecpia_clean['Year'].between(*year_range)]
filtered_df_ccpia_clean = df_ccpia_clean[df_ccpia_clean['Year'].between(*year_range)]
filtered_df_ppia_clean = df_ppia_clean[df_ppia_clean['Year'].between(*year_range)]

country = streamlit.sidebar.selectbox("Select a country for the first two charts", options = filtered_df_hcpia_clean['Country'].unique(), index = 190)

with streamlit.expander("Additional instructions for the first two charts"):
    streamlit.write("The first chart shows inflation over time for a particular inflation metric, while the second shows similar data, but allows you to compare two metrics. To use, you may select any country in the sidebar dropdown, which will show its data for both charts. To find the country you want quickly, you can type directly in the dropdown to search for it. If you would like to focus on a specific range of years, you have two options. You may filter for the first and second chart at the same time using the sidebar slider. In this case, be sure to select 'Charts filtered by range.' Or, if you select 'Charts filtered interactively,' the line chart shows all years available, and allows you to select on it directly to highlight your years of interest on the scatterplot below. If you use this method of filtering, the first inflation metric you select will be both the horizontal axis on the scatterplot and the one shown in the line chart. The second will be the vertical axis on the scatterplot. Whether you choose to use the slider to filter, or the interactive charts, the data remains the same. Choose whichever functionality is better for you.")

tab1, tab2 = streamlit.tabs(["Charts Filtered by Range", "Charts Filtered Interactively (Brushing)"])

with tab1:
    streamlit.subheader("Inflation over time for a particular country")
    streamlit.write("This graph shows the inflation in the country you selected. It is filtered by year. The default country is the United States.")

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

    with streamlit.expander("Table Format: Inflation in " + country):
        streamlit.dataframe(part1a(df_to_use_1, country), column_config = {"Year": streamlit.column_config.DateColumn("Year", format = "YYYY")}, width = 200, hide_index = True)
    
    streamlit.subheader("Scatter plot comparing two inflation measures for a particular country through the years")
    streamlit.write("This plot helps you to compare correlations of two inflation metrics that you select below. The country selected is the same as in the line chart. This plot may also be filtered by year.")

    inf_measure_2 = streamlit.selectbox("Select first inflation metric", options = ['HCPI', 'FCPI', 'ECPI', 'CCPI', 'PPI'], index = 0, key = "Scatterplot 1 1")
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
    
    inf_measure_3 = streamlit.selectbox("Select second inflation metric", options = ['HCPI', 'FCPI', 'ECPI', 'CCPI', 'PPI'], index = 1, key = "Scatterplot 1 2")
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

    with streamlit.expander("Table Format: " + inf_measure_2 + " vs " + inf_measure_3 + " Inflation: " + country):
        streamlit.dataframe(part2a(df_to_use_1, df_to_use_2, country, inf_measure_2, inf_measure_3), column_config = {"Year": streamlit.column_config.DateColumn("Year", format = "YYYY")}, width = 400, hide_index = True)

with tab2:
    streamlit.subheader("Inflation over time and comparing two inflation measures for a particular country")

    streamlit.write("These charts show inflation in the country you selected. The default country is the United States. The second chart lets you compare two metrics with one another. To filter and highlight points in the scatterplot, drag and brush the range of years of interest on the line chart. Please note that the filter slider at the side does not have an effect on these charts! To use the slider filter, go to 'Charts filtered by range.'")

    inf_measure_2 = streamlit.selectbox("Select first inflation metric", options = ['HCPI', 'FCPI', 'ECPI', 'CCPI', 'PPI'], index = 0, key = "Scatterplot 2 1")
    if inf_measure_2 == "HCPI":
        df_to_use_1 = df_hcpia_clean
    elif inf_measure_2 == "FCPI":
        df_to_use_1 = df_fcpia_clean
    elif inf_measure_2 == "ECPI":
        df_to_use_1 = df_ecpia_clean
    elif inf_measure_2 == "CCPI":
        df_to_use_1 = df_ccpia_clean
    elif inf_measure_2 == "PPI":
        df_to_use_1 = df_ppia_clean
    
    inf_measure_3 = streamlit.selectbox("Select second inflation metric", options = ['HCPI', 'FCPI', 'ECPI', 'CCPI', 'PPI'], index = 1, key = "Scatterplot 2 2")
    if inf_measure_3 == "HCPI":
        df_to_use_2 = df_hcpia_clean
    elif inf_measure_3 == "FCPI":
        df_to_use_2 = df_fcpia_clean
    elif inf_measure_3 == "ECPI":
        df_to_use_2 = df_ecpia_clean
    elif inf_measure_3 == "CCPI":
        df_to_use_2 = df_ccpia_clean
    elif inf_measure_3 == "PPI":
        df_to_use_2 = df_ppia_clean
    
    streamlit.altair_chart(parts1and2alt(df_to_use_1, df_to_use_2, country, inf_measure_2, inf_measure_3), use_container_width = True)

    with streamlit.expander("Table Format: Inflation in " + country):
        streamlit.dataframe(part1a(df_to_use_1, country), column_config = {"Year": streamlit.column_config.DateColumn("Year", format = "YYYY")}, width = 200, hide_index = True)
    
    with streamlit.expander("Table Format: " + inf_measure_2 + " vs " + inf_measure_3 + " Inflation: " + country):
        streamlit.dataframe(part2a(df_to_use_1, df_to_use_2, country, inf_measure_2, inf_measure_3), column_config = {"Year": streamlit.column_config.DateColumn("Year", format = "YYYY")}, width = 400, hide_index = True)

streamlit.subheader("Bar chart showing inflation levels in a particular year for the countries selected")
streamlit.write("Here you can select all the countries you would like below, as well as a particular year, and compare their inflation levels. You must select at least one country to see a chart. You may choose as many as have data available. To find the countries you want quickly, you can type directly in the dropdown to search for them.")

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

with streamlit.expander("Table Format: Inflation by country, " + str(year_to_use)):
    if len(countries) > 0:
        streamlit.dataframe(part3a(df_to_use_1, year_to_use, countries), width = 200, hide_index = True)
    else:
        streamlit.write("Select countries for the plot above to get the table")

