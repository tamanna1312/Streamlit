import streamlit as st
import pandas as pd
import random
from bokeh.plotting import figure
import plotly.express as px
import glob
import folium
from streamlit_folium import folium_static
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from folium import plugins

st.title('GEOROC DATA VISUALISER')
st.text('The Georoc data contains major and trace element concentrations, radiogenic and nonradiogenic isotope ratios as well as analytical ages for whole rocks, glasses, minerals and inclusions. Metadata include geospatial and other sample information, for example latitude, longitude, type of eruption etc, analytical details and references.')
st.header('Data Selection')

# This is how it looked before, the problem is, that it runs each time an interaction such as a selection is done. This takes up huge amounts of time.
# folders = st.multiselect('Select Tectonic Unit(s)', ['Cratons', 'CFBs', 'Rift Volcanics', 'Oceanic Plateaus', 'OceanBasinFlood Basalts','Complex Volcanic Settings','Convergent Margins'], ['Cratons'])

# st.session_state.all_data = []
# for i in folders:
# 	files = glob.glob(i+'/*.csv')
# 	df_list = []
# 	for file in files:
# 		df = pd.read_csv(file,encoding='ISO-8859-1')
# 		df.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE'}, inplace=True)
# 		df2 = df.fillna(0)
# 		if len(df2) < 20:
# 			df_list.append(df2.sample(len(df2)))
# 		else:
# 			df_list.append(df2.sample(20))
# 	st.session_state.all_data.append(pd.concat(df_list).reset_index())

# sel_vis = st.radio('Select Visualisation', ['map', 'plots'], horizontal=True)


with st.form('data'):
	folders = st.multiselect('Select Tectonic Unit(s)', ['Cratons', 'CFBs', 'Rift Volcanics', 'Oceanic Plateaus', 'OceanBasinFlood Basalts','Complex Volcanic Settings','Convergent Margins'], ['Cratons'])
	data_form_submitted = st.form_submit_button("load selected data")
	if data_form_submitted:
		st.session_state.all_data = []
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
			st.session_state.all_data.append(pd.concat(df_list).reset_index())


sel_vis =st.radio('Select Visualisation', ['map', 'plots'], horizontal=True)

if sel_vis == 'map':
	if st.session_state.all_data is None:
		st.write('No data loaded')
	else:
		colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
		map = folium.Map(location=[34, 100], zoom_start=5, control_scale=True,tiles = 'Stamen Terrain')
		marker_cluster = plugins.MarkerCluster().add_to(map)
		for j in range(len(folders)):
			for i in range(0,len(st.session_state.all_data[j])):
				folium.Marker(
					location=[st.session_state.all_data[j].iloc[i]['LATITUDE'], st.session_state.all_data[j].iloc[i]['LONGITUDE']],
					popup=st.session_state.all_data[j].iloc[i]['LOCATION'],
				icon=folium.Icon(color=colours[j]),
			).add_to(marker_cluster)

		folium_static(map, width=700, height=450)

else:
	if st.session_state.all_data is None:
		st.write('No data loaded')
	else:
		colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
		tab1, tab2, tab3 = st.tabs(['scatter', 'category', 'ternary'])

		with tab1:
			col1, col2 = st.columns([1,5])
			with col1:
				x = st.selectbox('x-axis', st.session_state.all_data[0].columns.tolist()[28:146])
				y = st.selectbox('y-axis', st.session_state.all_data[0].columns.tolist()[28:146], index = 9)
			with col2:
					p = figure(
					title='scatter plot',
					x_axis_label=x,
					y_axis_label=y)

					for i in range(len(folders)):
						p.scatter(st.session_state.all_data[i][x], st.session_state.all_data[i][y], legend_label=folders[i], line_width=2,color=colours[i])
					st.bokeh_chart(p, use_container_width=True)

		with tab2:
			sel_option = st.radio('Select Plot', ['REE', 'CI Normalised','CM Normalised'], horizontal=True)
			subset_elements=st.session_state.all_data[0].columns.tolist()[119:133]
			x_labels=subset_elements
			p2= figure(
			title='REE plot', x_range=x_labels, x_axis_label="Element", y_axis_label="Abundance (ppm)")
			colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
			norm_data=pd.read_csv('norm_data.csv', sep=';',decimal=',')
			normdata=norm_data.loc[:, subset_elements]
			if sel_option == 'REE':
				for j in range(len(folders)):
					a=st.session_state.all_data[j][subset_elements]
					for col in a:
						p2.line(x='index',y=col,source=a,color=colours[j],line_width=2,legend_label=folders[j])
			if sel_option == 'CI Normalised':
				for j in range(len(folders)):
					a=st.session_state.all_data[j][subset_elements]
					final=a.div(normdata.iloc[0], axis=1)
					for col in final:
						p2.line(x='index',y=col,source=final,color=colours[j],line_width=2,legend_label=folders[j])
			else:
				for j in range(len(folders)):
					a=st.session_state.all_data[j][subset_elements]
					final=a.div(normdata.iloc[1], axis=1)
					for col in final:
						p2.line(x='index',y=col,source=final,color=colours[j],line_width=2,legend_label=folders[j])
			st.bokeh_chart(p2, use_container_width=True)
			
				
				
		with tab3:
			col1, col2 = st.columns([1,5])
			with col1:
				tern_top = st.selectbox('top', st.session_state.all_data[0].columns.tolist()[28:146])
				tern_left = st.selectbox('left', st.session_state.all_data[0].columns.tolist()[28:146], index=9)
				tern_right = st.selectbox('right', st.session_state.all_data[0].columns.tolist()[28:146], index=3)
			with col2:
				tern_plot_data = []
				for i in range(len(st.session_state.all_data)):
					df_tmp = st.session_state.all_data[i]
					df_tmp['tectonic unit'] = pd.Series([folders[i]] * len(st.session_state.all_data[i]))
					tern_plot_data.append(df_tmp)

				p=px.scatter_ternary(pd.concat(tern_plot_data), a=tern_top, b=tern_left, c=tern_right, color='tectonic unit')

				st.plotly_chart(p, use_container_width=True)
