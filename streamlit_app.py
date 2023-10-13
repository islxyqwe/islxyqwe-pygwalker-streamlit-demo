import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import init_streamlit_comm, StreamlitRenderer
import pygwalker as pyg
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Use Pygwalker In Streamlit: Typhoon Viewer",
    layout="wide"
)

st.title("Typhoon Viewer")
st.subheader("data source: https://www.kaggle.com/datasets/chriszhengao/rsmc-tokyo-typhoon-center-best-track-data")

# Initialize pygwalker communication
init_streamlit_comm()

@st.cache_resource
def getDataframe():
    df = pd.read_csv("./RSMC_Best_Track_Data.csv")

    return (pd.read_csv("./RSMC_Best_Track_Data.csv"), df["International number ID"].unique())

(df, ids) = getDataframe()

# When using `use_kernel_calc=True`, you should cache your pygwalker renderer, if you don't want your memory to explode
@st.cache_resource
def get_pyg_renderer(id) -> "StreamlitRenderer":
    filtered = df[(df['International number ID'] == id)]
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    return StreamlitRenderer(filtered, spec="./charts.json", debug=False)
 
id = st.selectbox('Typhoon International number ID', ids, index=1730)

renderer = get_pyg_renderer(id)

# display chart ui
st.subheader("Max wind speed")
renderer.render_pure_chart(1)
st.subheader("Center Pressure")
renderer.render_pure_chart(2)
st.subheader("Map View")
renderer.render_pure_chart(0)
