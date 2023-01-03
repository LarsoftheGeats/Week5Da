import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

df = pd.read_csv('supermarket.csv')
df['sales_per_customer']=df['store_sales']/df['daily_customer_count']
df_area_sales=df.groupby('store_area').sum('store_sales').reset_index()
df_area_sales=df_area_sales[['store_area','store_sales']]

st.subheader('Table')

# st.write(df.sort_values(by=['store_sales','store_area'], axis=0, ascending=False).iloc[0:5])
Ascending_list=False
if st.checkbox('Ascending'):
    Ascending_list=True

option = st.radio('Sort column',options=['items_available','daily_customer_count','store_sales','sales_per_customer'])

def highlight_emphasized(Ascending):
    color = 'green' if (not Ascending) else 'red'
    return f'backgroun-color: {color}'


def load_table(nrows=5,sortby='store_sales',data=df,Ascending=False):
    st.dataframe(data.sort_values(by=[sortby],axis=0, ascending=Ascending).iloc[0:nrows].style.applymap(highlight_emphasized, subset=[sortby]))

number_of_rows=st.slider('rows',5,10,5)
load_table(nrows=number_of_rows, sortby=option,data=df,Ascending=Ascending_list)