import streamlit as st
import pandas as pd
import random
from bokeh.plotting import figure
import plotly.express as px


craton_files = glob.glob('Cratons/*.csv')
df_list1 = [pd.read_csv(file,encoding='ISO-8859-1') for file in craton_files]
craton_data   = pd.concat(df_list1, ignore_index=True)
st.write(craton_data)

st.title('Normalised Plot Testing')
st.header('Loading GEOROC Data')
#georoc=pd.read_csv(Cratons/2023-03-1KRR1P_BUNDELKHAND_CRATON.csv, encoding='ISO-8859-1')
#georoc_file=georoc.fillna(0)
#st.write(georoc_file)
st.header('Loading Normalising Data')
norm_data=pd.read_csv('C:\\Users\\PC Galena\\Downloads\\norm_data_copy.csv', sep=';',decimal=',')
st.write(norm_data)

st.header('Lookup Elements')
df=pd.read_csv("C:\\Users\\PC Galena\\Downloads\\lookup_element_characteristics.csv", encoding='ISO-8859-1')
#st.write(df)
select_options = st.radio('Select Plot Type', ['REE', 'HSE','VOLATILE(high)','VOLATILE'], horizontal=True)
if select_options == 'REE':
	ree=df.loc[df['REE'] == 1]
	ree_selected=ree['ALL ELEMENTS']
	st.write(ree_selected)
	normdata=norm_data.loc[:,ree_selected]
	georoc_data=georoc_file.loc[:,ree_selected]
	x_labels=ree_selected
	p2= figure(
	title='REE plot', x_range=x_labels, x_axis_label="Element", y_axis_label="Abundance (ppm)")
	final=georoc_data.div(normdata.iloc[0], axis=1)
	for col in final:
		p2.line(x='index',y=col,source=final,color='blue',line_width=2)
	st.bokeh_chart(p2, use_container_width=True)
if select_options == 'HSE':
	hse=df.loc[df['HSE'] == 1]
	hse_selected=hse['ALL ELEMENTS'].tolist()
	st.write(hse_selected)
if select_options == 'VOLATILE(high)':
	vol_high=df.loc[df['VOLATILE(high)'] == 1]
	vol_high_selected=vol_high['ALL ELEMENTS'].tolist()
	st.write(vol_high_selected)
if select_options == 'VOLATILE':
	vol=df.loc[df['VOLATILE'] == 1]
	vol_selected=vol['ALL ELEMENTS'].tolist()
	st.write(vol_selected)




#st.write('Selected only REE ELEMENTS')
#normdata=norm_data.loc[:,ree_selected]
#georoc_data=georoc_file.loc[:,ree_selected]
#st.write(normdata)
#st.write(georoc_data)
