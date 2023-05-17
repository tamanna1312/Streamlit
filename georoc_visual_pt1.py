import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import plotly.express as px
import glob
import folium
from streamlit_folium import folium_static
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

st.title('GEOROC DATA VISUALISER')
st.text('The Georoc data contains major and trace element concentrations, radiogenic and nonradiogenic isotope ratios as well as analytical ages for whole rocks, glasses, minerals and inclusions. Metadata include geospatial and other sample information, for example latitude, longitude, type of eruption etc, analytical details and references.')
st.header('Data Selection')
folders = st.multiselect('Select Tectonic Unit(s)', ['Cratons', 'CFBs', 'Rift Volcanics', 'Oceanic Plateaus', 'OceanBasinFlood Basalts','Complex Volcanic Settings','Convergent Margins'], ['Cratons'])

all_data = []
for i in folders:
	files = glob.glob(i+'/*.csv')
	df_list = []
	for file in files:
		df = pd.read_csv(file,encoding='ISO-8859-1')
		df.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE'}, inplace=True)
		df2 = df.fillna(0)
		if len(df2) < 20:
			df_list.append(df2.sample(len(df2)))
		else:
			df_list.append(df2.sample(20))
	all_data.append(pd.concat(df_list).reset_index())

sel_vis = st.radio('Select Visualisation', ['map', 'plots'], horizontal=True)

if sel_vis == 'map':
	colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
	map = folium.Map(location=[22, 87], zoom_start=5, control_scale=True,tiles = 'Stamen Terrain')
	for j in range(len(folders)):
		for i in range(0,len(all_data[j])):
			folium.Marker(
				location=[all_data[j].iloc[i]['LATITUDE'], all_data[j].iloc[i]['LONGITUDE']],
				popup=all_data[j].iloc[i]['LOCATION'],
			icon=folium.Icon(color=colours[j]),
		).add_to(map)

	folium_static(map, width=700, height=450)

else:
	colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
	tab1, tab2, tab3 = st.tabs(['scatter', 'category', 'ternary'])

	with tab1:
		col1, col2 = st.columns([1,5])
		with col1:
			x = st.selectbox('x-axis', all_data[0].columns.tolist()[28:146])
			y = st.selectbox('y-axis', all_data[0].columns.tolist()[28:146], index = 9)
		with col2:
				p = figure(
				title='scatter plot',
				x_axis_label=x,
				y_axis_label=y)

				for i in range(len(folders)):
					p.scatter(all_data[i][x], all_data[i][y], legend_label=folders[i], line_width=2,color=colours[i])
				st.bokeh_chart(p, use_container_width=True)

	with tab2:
		sel_option = st.radio('Select Plot', ['REE', 'CI Normalised','CM Normalised'], horizontal=True)
		if sel_option == 'REE':
			
			subset_elements=all_data[0].columns.tolist()[119:133]
			#for j in range(len(folders)):
			for i in range(0,len(all_data)):
				a=all_data[i][subset_elements]
				
			x_labels=a.columns.tolist()
			#st.write(x_labels)
			p2= figure(
			title='REE plot', x_range=x_labels, x_axis_label="Element", y_axis_label="Abundance (ppm)")
			colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
			for j in range(len(folders)):
				for i in range(0,len(all_data[j])):
					a=all_data[i][subset_elements]
			for col in a:
				p2.line(x='index',y=col,source=a,color=colours[j],line_width=2,legend_label=folders[j])
			st.bokeh_chart(p2, use_container_width=True)
		if sel_option == 'CI Normalised':
			subset_elements=all_data[0].columns.tolist()[119:133]
			norm_data=pd.read_csv('norm_data.csv', sep=';',decimal=',')
			normdata=norm_data.loc[:, subset_elements]
			st.write(normdata)
			for i in range(0,len(all_data)):
				a=all_data[i][subset_elements]
			x_labels=a.columns.tolist()
			p3= figure(
			title='REE plot',x_range=x_labels, x_axis_label="Element", y_axis_label="Abundance/CI (ppm)")
			colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
			for j in range(len(folders)):
				final=a.div(normdata.iloc[0], axis=1)
				for col in a:
					p3.line(x='index',y=col,source=a,color=colours[j],line_width=2,legend_label=folders[j])
			st.bokeh_chart(p3, use_container_width=True)
			
		else:
			subset_elements=all_data[0].columns.tolist()[119:133]
			norm_data=pd.read_csv('norm_data.csv', sep=';',decimal=',')
			normdata=norm_data.loc[:, subset_elements]
			for i in range(0,len(all_data)):
				a=all_data[i][subset_elements]
			x_labels=a.columns.tolist()
			p4= figure(
			title='REE plot',x_range=x_labels, x_axis_label="Element", y_axis_label="Abundance/CM (ppm)")
			colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
			for j in range(len(folders)):
				for i in range(0,len(all_data[j])):
					#a=all_data[i][subset_elements]
					final=a.div(normdata.iloc[1], axis=1)
					for col in a:
						p4.line(x='index',y=col,source=a,color=colours[j],line_width=2,legend_label=folders[j])
			st.bokeh_chart(p4, use_container_width=True)
			
			
			
		

	with tab3:
		col1, col2 = st.columns([1,5])
		with col1:
			tern_top = st.selectbox('top', all_data[0].columns.tolist()[28:146])
			tern_left = st.selectbox('left', all_data[0].columns.tolist()[28:146], index=9)
			tern_right = st.selectbox('right', all_data[0].columns.tolist()[28:146], index=3)
		with col2:
			tern_plot_data = []
			for i in range(len(all_data)):
				df_tmp = all_data[i]
				df_tmp['tectonic unit'] = pd.Series([folders[i]] * len(all_data[i]))
				tern_plot_data.append(df_tmp)

			p=px.scatter_ternary(pd.concat(tern_plot_data), a=tern_top, b=tern_left, c=tern_right, color='tectonic unit')

			st.plotly_chart(p, use_container_width=True)
