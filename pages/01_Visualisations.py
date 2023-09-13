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
from bokeh.models import Range1d
import matplotlib.pyplot as plt

st.title('GEOCHEMICAL DATA VISUALISER')
#st.text('The Georoc data contains major and trace element concentrations, radiogenic and nonradiogenic isotope ratios as well as analytical ages for whole rocks, glasses, minerals and inclusions. Metadata include geospatial and other sample information, for example latitude, longitude, type of eruption etc, analytical details and references.')
st.header('Data Selection')

# This is how it looked before, the problem is, that it runs each time an interaction such as a selection is done. This takes up huge amounts of time.
# folders = st.multiselect('Select Tectonic Unit(s)', ['Cratons', 'CFBs', 'Rift Volcanics', 'Oceanic Plateaus', 'OceanBasinFlood Basalts','Complex Volcanic Settings','Convergent Margins'], ['Cratons'])

# st.session_state.all_data = []
# for i in folders:
# 	files = glob.glob(i+'/*.csv')
# 	df_list = []
# 	for file in files:
# 		df = pd.read_csv(file,encoding='ISO-8859-1')
# 		df.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE '}, inplace=True)
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
				df.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE','SIO2(WT%)':'SiO2(wt%)', 'TIO2(WT%)':'TiO2(wt%)',
		       'B2O3(WT%)':'B2O3(wt%)', 'AL2O3(WT%)':'Al2O3(wt%)', 'CR2O3(WT%)':'Cr2O3(wt%)', 'FE2O3(WT%)':'Fe2O3(wt%)', 'FEO(WT%)':'FeO(wt%)',
		       'FEOT(WT%)':'FeOT(wt%)', 'CAO(WT%)': 'CaO(wt%)', 'MGO(WT%)':'MgO(wt%)', 'MNO(WT%)':'MnO(wt%)', 'NIO(WT%)':'NiO(wt%)', 'K2O(WT%)':'K2O(wt%)',
		    	'NA2O(WT%)': 'Na2O(wt%)', 'P2O5(WT%)':'P2O5(wt%)', 'H2O(WT%)':'H2O(wt%)', 'F(WT%)':'F(wt%)', 'CL(WT%)':'Cl(wt%)', 'LI(PPM)':'Li', 'B(PPM)':'B',
			    'BE(PPM)':'Be', 'C(PPM)':'C', 'CO2(PPM)':'CO2', 'F(PPM)':'F', 'NA(PPM)':'Na', 'MG(PPM)':'Mg', 'AL(PPM)':'Al', 'P(PPM)':'P', 'S(PPM)':'S',
			    'CL(PPM)':'Cl', 'K(PPM)':'K', 'CA(PPM)':'Ca', 'SC(PPM)':'Sc', 'TI(PPM)':'Ti', 'V(PPM)':'V', 'CR(PPM)':'Cr', 'MN(PPM)':'Mn', 'FE(PPM)':'Fe',
			    'CO(PPM)':'Co', 'NI(PPM)':'Ni', 'CU(PPM)':'Cu', 'ZN(PPM)':'Zn', 'GA(PPM)':'Ga', 'GE(PPM)':'Ge', 'AS(PPM)':'As', 'SE(PPM)':'Se', 'BR(PPM)':'Br',
			    'RB(PPM)':'Rb',  'SR(PPM)': 'Sr',  'Y(PPM)': 'Y', 'ZR(PPM)':'Zr', 'NB(PPM)':'Nb', 'MO(PPM)':'Mo', 'RU(PPM)':'Ru', 'RH(PPM)':'Rh', 'PD(PPM)':'Pd',
			    'AG(PPM)':'Ag', 'CD(PPM)':'Cd', 'IN(PPM)':'In', 'SN(PPM)':'Sn', 'SB(PPM)':'Sb', 'TE(PPM)':'Te', 'I(PPM)':'I', 'CS(PPM)':'Cs', 'BA(PPM)':'Ba', 
				'LA(PPM)':'La', 'CE(PPM)':'Ce', 'PR(PPM)':'Pr', 'ND(PPM)':'Nd', 'SM(PPM)':'Sm', 'EU(PPM)':'Eu', 'GD(PPM)':'Gd', 'TB(PPM)':'Tb', 'DY(PPM)':'Dy',
				'HO(PPM)':'Ho', 'ER(PPM)':'Er', 'TM(PPM)':'Tm', 'YB(PPM)':'Yb',  'LU(PPM)': 'Lu', 'HF(PPM)':'Hf', 'TA(PPM)':'Ta', 'W(PPM)':'W', 'RE(PPM)':'Re',
				'OS(PPM)':'Os', 'IR(PPM)':'Ir', 'PT(PPM)':'Pt', 'AU(PPM)':'Au', 'HG(PPM)':'Hg', 'TL(PPM)':'Tl', 'PB(PPM)':'Pb', 'BI(PPM)':'Bi', 'TH(PPM)':'Th',
				'U(PPM)':'U'}, inplace=True)
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
			st.header('Loading Normalising Data')
			norm_data=pd.read_csv('norm_data_copy.csv', sep=';',decimal=',')
			st.write(norm_data)
			df=pd.read_csv("LOOKUP_ELEMENTS_CHARACTERISTICS.csv", encoding='ISO-8859-1',sep=';',decimal=',')
			select_options = st.radio('Select Plot Type', ['REE', 'HSE','VOLATILE(high)','VOLATILE'], horizontal=True)
			selected_plot=df.loc[df[select_options] == 1]
			selected_elements=selected_plot['Element']
			st.write(selected_elements)
			normdata=norm_data.loc[:,selected_elements]
			x_labels=selected_elements
			colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
			select_normalising=st.radio('Select Normalising Option', ['CI','CH','CM'])
			#p2= figure(
			#title=select_options, x_range=x_labels, x_axis_label="Element",y_axis_label=select_normalising )
			#p2.y_range = Range1d(0, 500)
			fig = plt.figure()
			for j in range(len(folders)):
					a=st.session_state.all_data[j][selected_elements]
				
					if select_normalising=='CI':
						CI_Norm=a.div(normdata.iloc[0], axis=1)
						CI_Norm1= CI_Norm.T
						st.write(a)
						st.write(CI_Norm1)
						plt.plot(CI_Norm1[CI_Norm1 != 0], c = colours[j])
						plt.ylabel('sample / CI')
						#for col in CI_Norm1:
							#p2.line(x='index',y=col,source=CI_Norm1,color=colours[j],line_width=2,legend_label=folders[j])
					if select_normalising=='CH':
						CH_Norm=a.div(normdata.iloc[1], axis=1)
						st.write(a)
						st.write(CH_Norm)
						CH_Norm1 = CH_Norm.T
						plt.plot(CH_Norm1[CH_Norm1 != 0], c = colours[j])
						plt.legend(folders)
						plt.ylabel('sample / CH')
						#plt.legend(folders[j])
						#for col in CH_Norm:
						#	p2.line(x='index',y=col,source=CH_Norm,color=colours[j],line_width=2,legend_label=folders[j])
					if select_normalising=='CM':
						CM_Norm=a.div(normdata.iloc[2], axis=1)
						CM_Norm1 = CM_Norm.T
						plt.plot(CM_Norm1[CM_Norm1 != 0], c = colours[j])
						plt.ylabel('sample / CM')
						#plt.legend(folders[j])
						#for col in CM_Norm:
						#	p2.line(x='index',y=col,source=CM_Norm,color=colours[j],line_width=2,legend_label=folders[j])
					plt.legend(folders[j])

			#st.bokeh_chart(p2, use_container_width=True)
			
			#plt.show()
					#plt.legend(folders)
			plt.yscale('log')
			
			st.pyplot(fig)

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
