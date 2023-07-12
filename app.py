import streamlit as st
import pandas as pd
import numpy as np
import base64

st.write("# Welcome to NBA Explorer!")
st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")
st.sidebar.write("## User Input Features")

selected_year = st.sidebar.selectbox("Enter the year",list(reversed(range(1950,2024))))
st.sidebar.write(selected_year)

# @st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_"+str(year)+"_per_game.html"
    html = pd.read_html(url,header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats



playerstats = load_data(selected_year)

teams = sorted(playerstats.Tm.unique())
selected_teams = st.sidebar.multiselect(" ## Enter the teams:",teams)
# st.sidebar.write("###### **Note:**  Deselect the teams you are not looking for.")
unique_pos = ['C','PF','SF','PG','SG','All']
selected_pos = st.sidebar.multiselect(" ## Enter the positions you are looking for:",unique_pos)
# st.sidebar.write("###### **Note:** Deselect the positions you are not looking for.")
df_selected_team = playerstats[(playerstats.Tm.isin(selected_teams)) & (playerstats.Pos.isin(selected_pos))]
if 'All' in selected_pos:
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_teams))]

if not df_selected_team.empty:
    st.write("#### Filtered Data:")
    st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
    st.dataframe(df_selected_team)
    df_selected_team = df_selected_team.to_csv(index=False)
    st.download_button(label="Download",data = df_selected_team,mime='text/csv',file_name="stats.csv")
