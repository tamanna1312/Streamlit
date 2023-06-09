import streamlit as st
import pandas as pd
import random
from bokeh.plotting import figure
import plotly.express as px
from bokeh.models import Range1d
import glob

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

# st.title('Normalised Plot Testing')
# st.header('Loading GEOROC Data')
# georoc=pd.read_csv('Cratons/2023-03-1KRR1P_BUNDELKHAND_CRATON.csv', encoding='ISO-8859-1')
# #st.write(georoc.columns.tolist())
# georoc.rename(columns={'LATITUDE MAX': 'LATITUDE', 'LONGITUDE MAX': 'LONGITUDE','SIO2(WT%)':'SiO2(wt%)', 'TIO2(WT%)':'TiO2(wt%)',
# 		       'B2O3(WT%)':'B2O3(wt%)', 'AL2O3(WT%)':'Al2O3(wt%)', 'CR2O3(WT%)':'Cr2O3(wt%)', 'FE2O3(WT%)':'Fe2O3(wt%)', 'FEO(WT%)':'FeO(wt%)',
# 		       'FEOT(WT%)':'FeOT(wt%)', 'CAO(WT%)': 'CaO(wt%)', 'MGO(WT%)':'MgO(wt%)', 'MNO(WT%)':'MnO(wt%)', 'NIO(WT%)':'NiO(wt%)', 'K2O(WT%)':'K2O(wt%)',
# 		    	'NA2O(WT%)': 'Na2O(wt%)', 'P2O5(WT%)':'P2O5(wt%)', 'H2O(WT%)':'H2O(wt%)', 'F(WT%)':'F(wt%)', 'CL(WT%)':'Cl(wt%)', 'LI(PPM)':'Li', 'B(PPM)':'B',
# 			    'BE(PPM)':'Be', 'C(PPM)':'C', 'CO2(PPM)':'CO2', 'F(PPM)':'F', 'NA(PPM)':'Na', 'MG(PPM)':'Mg', 'AL(PPM)':'Al', 'P(PPM)':'P', 'S(PPM)':'S',
# 			    'CL(PPM)':'Cl', 'K(PPM)':'K', 'CA(PPM)':'Ca', 'SC(PPM)':'Sc', 'TI(PPM)':'Ti', 'V(PPM)':'V', 'CR(PPM)':'Cr', 'MN(PPM)':'Mn', 'FE(PPM)':'Fe',
# 			    'CO(PPM)':'Co', 'NI(PPM)':'Ni', 'CU(PPM)':'Cu', 'ZN(PPM)':'Zn', 'GA(PPM)':'Ga', 'GE(PPM)':'Ge', 'AS(PPM)':'As', 'SE(PPM)':'Se', 'BR(PPM)':'Br',
# 			    'RB(PPM)':'Rb',  'SR(PPM)': 'Sr',  'Y(PPM)': 'Y', 'ZR(PPM)':'Zr', 'NB(PPM)':'Nb', 'MO(PPM)':'Mo', 'RU(PPM)':'Ru', 'RH(PPM)':'Rh', 'PD(PPM)':'Pd',
# 			    'AG(PPM)':'Ag', 'CD(PPM)':'Cd', 'IN(PPM)':'In', 'SN(PPM)':'Sn', 'SB(PPM)':'Sb', 'TE(PPM)':'Te', 'I(PPM)':'I', 'CS(PPM)':'Cs', 'BA(PPM)':'Ba', 
# 				'LA(PPM)':'La', 'CE(PPM)':'Ce', 'PR(PPM)':'Pr', 'ND(PPM)':'Nd', 'SM(PPM)':'Sm', 'EU(PPM)':'Eu', 'GD(PPM)':'Gd', 'TB(PPM)':'Tb', 'DY(PPM)':'Dy',
# 				'HO(PPM)':'Ho', 'ER(PPM)':'Er', 'TM(PPM)':'Tm', 'YB(PPM)':'Yb',  'LU(PPM)': 'Lu', 'HF(PPM)':'Hf', 'TA(PPM)':'Ta', 'W(PPM)':'W', 'RE(PPM)':'Re',
# 				'OS(PPM)':'Os', 'IR(PPM)':'Ir', 'PT(PPM)':'Pt', 'AU(PPM)':'Au', 'HG(PPM)':'Hg', 'TL(PPM)':'Tl', 'PB(PPM)':'Pb', 'BI(PPM)':'Bi', 'TH(PPM)':'Th',
# 				'U(PPM)':'U'}, inplace=True)

# #st.write(georoc)
# georoc_file=georoc.fillna(0)
# st.write(georoc_file)
st.header('Loading Normalising Data')
norm_data=pd.read_csv('norm_data_copy.csv', sep=';',decimal=',')
st.write(norm_data)

#st.header('Lookup Elements')
df=pd.read_csv("LOOKUP_ELEMENTS_CHARACTERISTICS.csv", encoding='ISO-8859-1',sep=';',decimal=',')
#st.write(df)
select_options = st.radio('Select Plot Type', ['REE', 'HSE','VOLATILE(high)','VOLATILE'], horizontal=True)

selected_plot=df.loc[df[select_options] == 1]
selected_elements=selected_plot['Element']
st.write(selected_elements)
normdata=norm_data.loc[:,selected_elements]

x_labels=selected_elements
colours = ['blue', 'green', 'purple', 'pink', 'yellow', 'grey', 'black']
select_normalising=st.radio('Select Normalising', ['CI','CH','CM'])
p2= figure(
title=select_options, x_range=x_labels, x_axis_label="Element",y_axis_label=select_normalising )
p2.y_range = Range1d(0, 500)
if select_normalising=='CI':
	for j in range(len(folders)):
		a=st.session_state.all_data[j][selected_elements]
		CI_Norm=a.div(normdata.iloc[0], axis=1)
		for col in CI_Norm:
			p2.line(x='index',y=col,source=CI_Norm,color=colours[j],line_width=2,legend_label=folders[j])
if select_normalising=='CH':
	for j in range(len(folders)):
		a=st.session_state.all_data[j][selected_elements]
		CH_Norm=a.div(normdata.iloc[1], axis=1)
		for col in CH_Norm:
			p2.line(x='index',y=col,source=CH_Norm,color=colours[j],line_width=2,legend_label=folders[j])

st.bokeh_chart(p2, use_container_width=True)





