import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import glob


st.title('Normalised Plot Testing')
st.header('Loading GEOROC Data')
craton_files = glob.glob('Cratons/*.csv')
df_list1 = [pd.read_csv(file,encoding='ISO-8859-1') for file in craton_files]
craton_data   = pd.concat(df_list1, ignore_index=True)
st.write(craton_data)
st.header('Loading Normalising Data')
norm_data=pd.read_csv('norm_data_copy.csv', sep=';',decimal=',')
st.write(norm_data)

st.header('Lookup Elements')
df=pd.read_csv('lookup_element_characteristics.csv', encoding='ISO-8859-1')
st.write(df)
select_options = st.radio('Select Plot Type', ['REE', 'HSE','VOLATILE(high)','VOLATILE'], horizontal=True)

selected_elements=df.loc[df[select_options] == 1]
ree_selected=selected_elements['ALL ELEMENTS']
st.write(selected_elements)
normdata=norm_data.loc[:,ree_selected]
georoc_data=georoc_file.loc[:,ree_selected]
x_labels=ree_selected
p2= figure(
title=select_options, x_range=x_labels, x_axis_label="Element", y_axis_label="Abundance (ppm)")
final=georoc_data.div(normdata.iloc[0], axis=1)
for col in final:
	p2.line(x='index',y=col,source=final,color='blue',line_width=2)
st.bokeh_chart(p2, use_container_width=True)




#st.write('Selected only REE ELEMENTS')
#normdata=norm_data.loc[:,ree_selected]
#georoc_data=georoc_file.loc[:,ree_selected]
#st.write(normdata)
#st.write(georoc_data)
