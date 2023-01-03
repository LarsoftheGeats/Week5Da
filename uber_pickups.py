import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')



def pasfunc (x):
    return x

@st.cache
def load_data(nrows):
    data=pd.read_csv(DATA_URL, nrows=nrows)
    lowercase= lambda x:str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state= st.text('Loading data...')
color = st.color_picker(label="page background")

st.markdown(
        """
    <style>

        .reportview-container .markdown-text-container {
        font-family: monospace;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }

    canvas {
        stroke: black;
        stroke-width: 2;
    }
    .Widget>label {
        color: white;
        font-family: monospace;
    }
    .main {
        background-color: %s;
        opacity: 0.5
    }
    </style>
    """ % (color),
    unsafe_allow_html=True,
)

data=load_data(10000)

data_load_state.text('Done! (using st.cache)')

st.write('The current color is', color)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)

filtered_data= data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

st.subheader('Pick ups per hour line chart')
data_derived=data.groupby(data[DATE_COLUMN].dt.hour, as_index=False).count().drop(['lat','lon','base'],axis='columns')
st.line_chart(data_derived)

