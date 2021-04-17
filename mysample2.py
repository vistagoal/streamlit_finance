# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 18:10:34 2021

@author: milol
"""

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Stock Explorer Russel 2000')

st.markdown("""
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Yahoo Fin for Russel 2000](https://finance.yahoo.com/).
""")


df=pd.read_csv("nasdaqfiveball.csv",index_col=0)

sorted_unique_sector = sorted(df.sector.unique())

country= sorted(df.country.unique(),reverse=True)

#Selection in sidebar
st.sidebar.header('Select Sector')
selected_sector = st.sidebar.selectbox('Sector', sorted_unique_sector)
df_selection=df.query('sector==@selected_sector')
country= sorted(df_selection.country.unique(),reverse=True)
selected_country=st.sidebar.multiselect("Country",country,country)

df_data_selected=df_selection[(df_selection.country.isin(selected_country))]

df_data_display=df_data_selected.iloc[:,0:15].drop(df_selection.columns[[1,9,10,12]],axis = 1)
st.header('Display Stats')
st.write('Data Dimension: ' + str(df_data_display.shape[0]) + ' rows and ' + str(df_data_display.shape[1]) + ' columns.')

st.dataframe(df_data_display)

# Download Stock  data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df_data_display):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_data_display), unsafe_allow_html=True)