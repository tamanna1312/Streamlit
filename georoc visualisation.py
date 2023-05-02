import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import plotly.express as px
import glob
import folium
from streamlit_folium import folium_static


st.title('GEOROC data visualiser')

sel_tect_unit = st.multiselect('select tectonic unit(s)', ['Cratons', 'CFBs', 'Rift Volcanics', 'Oceanic Plateaus', 'OceanBasinFlood Basalts'], ['Cratons'])

nr_of_rand_smp = 20

df_all_tect_units = []
for i in sel_tect_unit:
	files = glob.glob(i+'/*.csv')
	df_list = []
	for file in files:
		l = pd.read_csv(file,encoding='ISO-8859-1')
		l.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE'}, inplace=True)
		l2 = l.fillna(0)
		if len(l2) > nr_of_rand_smp:
			df_list.append(l2.sample(nr_of_rand_smp))
	df_all_tect_units.append(pd.concat(df_list).reset_index())

# st.write(df_all_tect_units[0])


sel_vis = st.radio('select visualisation', ['map', 'plots'], horizontal=True)

if sel_vis == 'map':
	colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
	map = folium.Map(location=[22, 87], zoom_start=1, control_scale=True,tiles = 'Stamen Terrain')
	for j in range(len(sel_tect_unit)):
		for i in range(0,len(df_all_tect_units[j])):
			folium.Marker(
				location=[df_all_tect_units[j].iloc[i]['LATITUDE'], df_all_tect_units[j].iloc[i]['LONGITUDE']],
				popup=df_all_tect_units[j].iloc[i]['LOCATION'],
			icon=folium.Icon(color=colours[j], icon='pushpin'),
		).add_to(map)

	folium_static(map, width=700, height=450)

else:
	colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
	tab1, tab2, tab3 = st.tabs(['scatter', 'category', 'ternary'])

	with tab1:
		col1, col2 = st.columns([1,5])
		with col1:
			x = st.selectbox('x-axis', df_all_tect_units[0].columns.tolist()[28:146])
			y = st.selectbox('y-axis', df_all_tect_units[0].columns.tolist()[28:146], index = 9)
		with col2:
				p = figure(
				title='scatter plot',
				x_axis_label=x,
				y_axis_label=y)

				for i in range(len(sel_tect_unit)):
					p.scatter(df_all_tect_units[i][x], df_all_tect_units[i][y], legend_label=sel_tect_unit[i], line_width=2,color=colours[i])
				st.bokeh_chart(p, use_container_width=True)
	
	with tab2:
		st.write('I think these did not make too much sense - what did you want to show with these?')

	with tab3:
		col1, col2 = st.columns([1,5])
		with col1:
			tern_top = st.selectbox('top', df_all_tect_units[0].columns.tolist()[28:146])
			tern_left = st.selectbox('left', df_all_tect_units[0].columns.tolist()[28:146], index=9)
			tern_right = st.selectbox('right', df_all_tect_units[0].columns.tolist()[28:146], index=3)
		with col2:
			tern_plot_data = []
			for i in range(len(df_all_tect_units)):
				df_tmp = df_all_tect_units[i]
				df_tmp['tectonic unit'] = pd.Series([sel_tect_unit[i]] * len(df_all_tect_units[i]))
				tern_plot_data.append(df_tmp)

			p=px.scatter_ternary(pd.concat(tern_plot_data), a=tern_top, b=tern_left, c=tern_right, color='tectonic unit')

			st.plotly_chart(p, use_container_width=True)