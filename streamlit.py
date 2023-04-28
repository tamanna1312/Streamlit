import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import glob
import folium
from streamlit_folium import st_folium

header = st.container()
data= st.container()
features=st.container()
plots= st.container()


with header:
	st.title('GEOROC DATA')
	st.text('The Georoc data contains major and trace element concentrations, radiogenic and nonradiogenic isotope ratios as well as analytical ages for whole rocks, glasses, minerals and inclusions. Metadata include geospatial and other sample information, for example latitude, longitude, type of eruption etc, analytical details and references.')
	
with data:
	col1, col2= st.columns(2)
	with col1:
	
		craton_files = glob.glob('Cratons/*.csv')
		df_list1 = [pd.read_csv(file,encoding='ISO-8859-1') for file in craton_files]
		craton_data   = pd.concat(df_list1, ignore_index=True)
		cfb_files=glob.glob('CFBs/*.csv')
		df_list2 = [pd.read_csv(file,encoding='ISO-8859-1') for file in cfb_files]
		cfb_data   = pd.concat(df_list2, ignore_index=True)
		rifts_files=glob.glob('Rift Volcanics/*.csv')
		df_list3 = [pd.read_csv(file,encoding='ISO-8859-1') for file in rifts_files]
		rift_data   = pd.concat(df_list3, ignore_index=True)
		oceanicPlat_files=glob.glob('Oceanic Plateaus/*.csv')
		df_list4 = [pd.read_csv(file,encoding='ISO-8859-1') for file in oceanicPlat_files]
		oceanicPlat_data=pd.concat(df_list4, ignore_index=True)
		floodbasalt_files=glob.glob('OceanBasinFlood Basalts/*.csv')
		df_list5 = [pd.read_csv(file,encoding='ISO-8859-1') for file in floodbasalt_files]
		floodbasalt_data=pd.concat(df_list5, ignore_index=True)
		
		#st.header('To download files')
		#cratonData=craton_data.to_csv().encode('utf-8')
		#st.download_button(
			#label='Download Craton file',
			#data=cratonData,
			#file_name='Craton Data',
			#mime='text/csv'
			#)
		#CFBData=cfb_data.to_csv().encode('utf-8')
		#st.download_button(
			#label='Download CFB file',
			#data=CFBData,
			#file_name='Continental Flood Basalts Data',
			#mime='text/csv'
			#)
		#RiftData=rift_data.to_csv().encode('utf-8')
		#st.download_button(
			#label='Download Rift Volcanics file',
			#data=RiftData,
			#file_name='Rift Volcanics Data',
			#mime='text/csv'
			#)
		#OcnPlatData=oceanicPlat_data.to_csv().encode('utf-8')
		#st.download_button(
			#label='Download Convergent Margin file',
			#data=RiftData,
			#file_name='Oceanic Plateaus',
			#mime='text/csv'
			#)

	with st.sidebar:
		st.header('Data Selection')
		ck1=st.checkbox('Craton Data')
		ck2=st.checkbox('Continental Flood Basalts')
		ck3=st.checkbox('Rift Volcanics')
		ck4=st.checkbox('Oceanic Plateaus')
		ck5=st.checkbox('Convergent Margins')
		ck6=st.checkbox('Ocean Basin Flood Basalts')
		df_list = []
		if ck1:
			df_list.extend([pd.read_csv(file,encoding='ISO-8859-1') for file in craton_files])	
		if ck2:
			df_list.extend([pd.read_csv(file,encoding='ISO-8859-1') for file in cfb_files])
		
		if ck3:
			df_list.extend([pd.read_csv(file,encoding='ISO-8859-1') for file in rifts_files])
		if ck4:
			df_list.extend([pd.read_csv(file,encoding='ISO-8859-1') for file in oceanicPlat_files])
		if ck5:
			df_list.extend([pd.read_csv(file,encoding='ISO-8859-1') for file in floodbasalt_files])
			
		df_data = pd.concat(df_list, ignore_index=True)
		final_data=df_data.fillna(0)
		final_data.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE'}, inplace=True)
		craton_data.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE'}, inplace=True)
		cfb_data.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE'}, inplace=True)
		rift_data.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE'}, inplace=True)
		
		st.write(final_data)
	
		#sck1=st.sidebar.checkbox(('Craton Data'),key=0)
		#sck2=st.sidebar.checkbox(('Continental Flood Basalts'),key=1)
		#sck3=st.sidebar.checkbox(('Rift Volcanics'),key=2)
		#sck4=st.sidebar.checkbox(('Oceanic Plateaus'),key=3)
		#sck5=st.sidebar.checkbox(('Flood Basalts'),key=6)
		#if sck1:
			#st.write(craton_files)
		#if sck2:
			#st.write(cfb_files)
		#if sck3:
			#st.write(rifts_files)
		#if sck4:
			#st.write(oceanicPlat_files)
		#if sck5:
			#st.write(floodbasalt_files)
		
				
with plots:
	st.header('Location of datapoints  on a map')
	st.text('Plot 1')
	#button2=st.expander('Plot 1')
	#if button2:
		#st.map(final_data)
	if ck1:
		craton_data1=craton_data.fillna(0)
		map = folium.Map(location=[22, 87], zoom_start=5, control_scale=True,tiles = 'Stamen Terrain')
		for i in range(0,len(final_data)):
    			folium.Marker(
      			location=[final_data.iloc[i]['LATITUDE'], final_data.iloc[i]['LONGITUDE']],
      			popup=final_data.iloc[i]['LOCATION'],
			icon=folium.Icon(color='blue', icon='pushpin'),
  	 	).add_to(map)
	if ck2:
		cfb_data1=cfb_data.fillna(0)
		for i in range(0,len(cfb_data1)):
    			folium.Marker(
      			location=[cfb_data1.iloc[i]['LATITUDE'], cfb_data1.iloc[i]['LONGITUDE']],
      			popup=cfb_data1.iloc[i]['LOCATION'],
			icon=folium.Icon(color='red', icon='pushpin'),
  	 	).add_to(map)
	if ck3:
		rift_data1=rift_data.fillna(0)
		for i in range(0,len(rift_data1)):
    			folium.Marker(
      			location=[rift_data1.iloc[i]['LATITUDE'], rift_data1.iloc[i]['LONGITUDE']],
      			popup=rift_data1.iloc[i]['LOCATION'],
			icon=folium.Icon(color='green', icon='pushpin'),
  	 	).add_to(map)
	if ck4:
		oceanicPlat_data1=oceanicPlat_data.fillna(0)
		for i in range(0,len(oceanicPlat_data1)):
    			folium.Marker(
      			location=[oceanicPlat_data1.iloc[i]['LATITUDE'], oceanicPlat_data1.iloc[i]['LONGITUDE']],
      			popup=oceanicPlat_data1.iloc[i]['LOCATION'],
			icon=folium.Icon(color='purple', icon='pushpin'),
  	 	).add_to(map)
	if ck5:
		floodbasalt_data1=floodbasalt_data.fillna(0)
		for i in range(0,len(floodbasalt_data1)):
    			folium.Marker(
      			location=[floodbasalt_data1.iloc[i]['LATITUDE'], floodbasalt_data1.iloc[i]['LONGITUDE']],
      			popup=floodbasalt_data1.iloc[i]['LOCATION'],
			icon=folium.Icon(color='pink', icon='pushpin'),
  	 	).add_to(map)
		
	st_map=st_folium(map, width=700, height=450)
	
	st.text('Plot 2')
	st.markdown('PLOTS')
	
	tab1,tab2=st.tabs(['Scatter Plot','Category Plot'])
	with tab1:
		col1, col2 = st.columns([1,5])
		with col1:
			x = st.selectbox('x-axis', final_data.columns.tolist()[27:146])
			y = st.selectbox('y-axis', final_data.columns.tolist()[27:146], index = 9)
		with col2:
				p = figure(
				title='scatter plot',
				x_axis_label=x,
				y_axis_label=y)

		if ck1:
			p.scatter(craton_data[x], craton_data[y], legend_label='Craton Data', line_width=2,color='green')
		if ck2:
			p.scatter(cfb_data[x], cfb_data[y], legend_label='Continental Flood Basalts', line_width=2,color='blue')
		if ck3:
			p.scatter(rift_data[x], rift_data[y], legend_label='Rift Data', line_width=2,color='red')
		if ck4:
			p.scatter(oceanicPlat_data[x], oceanicPlat_data[y], legend_label='Oceanic Plateaus', line_width=2,color='yellow')
		st.bokeh_chart(p, use_container_width=True)
		
	with tab2:
		col1, col2 = st.columns([1,5])
		with col1:
			x = st.selectbox('x-axis', final_data.columns.tolist()[27:146],key=4)
			y = st.selectbox('y-axis', final_data.columns.tolist()[27:146],key=5,index = 9)
		with col2:
				p1 = figure(
				title='line plot',
				x_axis_label=x ,
				y_axis_label=y)
		
		if ck1:
			p1.line(craton_data[x], craton_data[y], legend_label='Craton Data', line_width=2,color='green')
		if ck2:
			p1.line(cfb_data[x], cfb_data[y], legend_label='Continental Flood Basalts', line_width=2,color='blue')
		if ck3:
			p1.line(rift_data[x], rift_data[y], legend_label='Rift Data', line_width=2,color='red')
		if ck4:
			p1.line(oceanicPlat_data[x], oceanicPlat_data[y], legend_label='Oceanic Plateaus', line_width=2,color='yellow')

		#p.line(final_data[x]/10000, final_data[y]/10000, legend_label='Trend', line_width=2)
		st.bokeh_chart(p1, use_container_width=True)
		
