# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:36:02 2023

@author: Ronan
"""
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st
import datetime as dt
from bokeh.plotting import figure 
import datetime as dt

# Page title
st.set_page_config(page_title='CFD explorer', page_icon='📊')
st.title('📊 CFD Explorer')

@st.cache_data()
def import_xml_url(url):
    
    # Téléchargez le contenu du fichier XML depuis l'URL
    response = requests.get(url)
    
    # Vérifiez si le téléchargement s'est bien passé (statut HTTP 200 signifie succès)
    if response.status_code == 200:
        xml_content = response.text
    
        # Analysez le contenu XML
        root = ET.fromstring(xml_content)
        
        
        # Accéder à l'instruction de transformation XML (stylesheet)
        stylesheet = root.find("cfd.xls")
        #https://parapente.ffvl.fr/sites/all/modules/ffvl_compet/ffvl_cfd/cfd.xsl
        if stylesheet is not None:
            # Récupérer le contenu de l'instruction de transformation
            stylesheet_content = stylesheet.text
            print("Instruction de transformation XML :")
            print(stylesheet_content)
        
        flight_id = []
        date = []
        pilot = []
        flight_type =[]
        distance = []
        club = []
        aile = []
        aile_class  = []
        igc_tracklog  = []
        flightSeason  = []
        status  = []
        recordDate  = []
        distTot  = []
        points  = []
        takeOff  = []
        landing  = []
        duration  = []
        speed  = []
        
        # Accédez aux données du fichier XML comme précédemment
        cfdflightlist = root.find('cfdflightlist')
        
        for flight in cfdflightlist.iter('flight'):
            
            flight_id.append(flight.get('id'))
            date.append(flight.get('date'))
            pilot.append(flight.get('pilot'))
            flight_type.append(flight.get('flight_type'))
            distance.append(flight.get('distance'))
            club.append(flight.get('club'))
            aile.append(flight.get('aile'))
            aile_class.append(flight.get('aile_class'))
            igc_tracklog.append(flight.get('igc_tracklog'))
            flightSeason.append(flight.get('flightSeason'))
            status.append(flight.get('status'))
            recordDate.append(flight.get('recordDate'))
            distTot.append(flight.get('distTot'))
            points.append(flight.get('points'))
            takeOff.append(flight.get('takeOff'))
            landing.append(flight.get('landing'))
            duration.append(flight.get('duration'))
            speed.append(flight.get('speed'))
   
            # Vous pouvez accéder à d'autres attributs de la balise 'flight' ici
        
        dict_df = {'pilot':pilot, 
                   'points':points,
                   'club':club,
                   'date':date,  
                   'aile':aile,
                   'aile_class':aile_class,
                   #'flightSeason':flightSeason,
                   #'status':status,
                   #'recordDate':recordDate,
                   #'distTot':distTot,
                   'takeOff':takeOff,
                   'landing':landing,
                   'distance':distance, 
                   'duration':duration,
                   'speed':speed,
                   'igc_tracklog':igc_tracklog,
                   'flight_type':flight_type,
                   'flight_id':flight_id}
        

        
        df = pd.DataFrame(dict_df)#,dtype = [("points", "float64"), ("distance", "float64"), ("duration", "float64")])
        
        df = df.astype({'points': 'float32',
                        'distance': 'float32',
                        'date': 'string'})
        df['date'] = pd.to_datetime(df['date'])#.dt.date
        df_out = df.round({'points':1})
                       
        # Vous pouvez continuer à travailler avec les données du fichier XML de la même manière.
    else:
        print(f"Échec de la récupération du fichier XML depuis l'URL. Code d'état HTTP : {response.status_code}")
        
    
    return df_out

url = "https://parapente.ffvl.fr/cfd/liste/2023?xml=1"
df = import_xml_url(url) 

#for year in ['2010','2011','2012','2013','2014','2015','2016','2017','2018',
#             '2019','2020','2021','2022']:
#    df = pd.concat([df,import_xml_url('https://parapente.ffvl.fr/cfd/liste/'+year+'?xml=1')]) 

with st.expander('About this app'):
  st.markdown('**Que fait cette app?**')
  st.info('Cette app explore les données de la CFD pour la saison 2023-2024. Toutes les données sont extraites du site de la FFVL: https://parapente.ffvl.fr ')
  st.markdown('**Comment l\'utiliser ?**')
  st.warning('Naviguez dans les menus, utilisez les filtres. Plusieurs pages sont disponibles dans la barre latérale ')
  st.markdown('**Contact**')
  st.warning('cfdexplorer.pro@gmail.com')
  
st.subheader('Actu de la CFD (28/03/2024)')

st.write('Alors que le printemps émerge timidement, les premiers vols de plus de 100 km ont déjà été réalisé, laissant entrevoir les beaux cross à venir !')
st.write('Dans les Pyrénées, Florian Rivière nous a éblouis avec un vol de 107 km, survolant les paysages de Loudenvielle à Tarascon. ([vol](https://parapente.ffvl.fr/cfd/liste/vol/20356513))')
st.write('En plaine, dans les confins de la Moselle et des Ardennes, Etienne Coupez a navigué avec audace sur 114 km le long des frontières du Luxembourg et de la Belgique. ([vol](https://parapente.ffvl.fr/cfd/liste/vol/20356622))')
st.write('Du haut des Alpes, Justin Puthod a réalisé une très belle trace de 177 km, s\'envolant depuis Meruz, en direction des Aravis, vallée de Chamonix, Annecy, Bauges. ([vol](https://parapente.ffvl.fr/cfd/liste/vol/20356318)) ')
st.write('Et avec une EN-B, Johan Le Bars décolle depuis Bar sur Aube pour boucler un vol de 97 km ([vol](https://parapente.ffvl.fr/cfd/liste/vol/20355964))')
st.write('Ces premières prouesses aériennes ne font que présager des perfs dans les semaines à venir. La magie du parapente au printemps nous réserve encore de belles surprises.')
st.write('')
#df = df.sort_values('points',ascending = False)
df = df.sort_values('date',ascending = False)
df['month'] = df['date'].apply(lambda x: x.month)
df['year'] = df['date'].apply(lambda x: x.year)
df['week'] = df['date'].apply(lambda x: x.week)

df['flight_link']='https://parapente.ffvl.fr/cfd/liste/vol/' + df['flight_id']

# Using "with" notation
#with st.sidebar:
#    add_radio = st.radio(
#        "Selection",
#        ("News","Classement dernier mois", "Vue pilote","Vue Club","Contact")
#    )

#if add_radio == "Classement par points":
#    st.dataframe(df.head(100))

#if add_radio == "News":


#if add_radio == "Classement dernier mois":
# Get today's date
st.subheader('Classement par point sur le dernier mois')
today = dt.datetime.now()

# Calculate the date less than 1 month ago
less_than_one_month_ago = dt.datetime.now() - dt.timedelta(days=30)
#st.write(less_than_one_month_ago)
df_show = df[df['date']>less_than_one_month_ago]
df_show = df_show.sort_values('points',ascending = False)

sel_cat = st.multiselect('Catégorie d''aile selectionnée : ',list(df_show['aile_class'].unique()),list(df_show['aile_class'].unique()))

df_show = df_show[(df_show['aile_class'].isin(sel_cat))].sort_values('points',ascending = False)


df_show['Classement'] = range(0,df_show.shape[0]) 
df_show['Classement'] = df_show['Classement'] + 1

df_show = df_show.set_index('Classement')

df_show = df_show[df_show.index <30]

date = df_show['date']
flight_id = df_show['flight_id']
takeOff = df_show['takeOff']
takeOff2 =[]
kk=0
for el in takeOff:
    kk += 1
    takeOff2.append(el + ' - ' +str(kk))

pilot = df_show['pilot']
pilot2 =[]
kk=0
for el in pilot:
    kk += 1
    pilot2.append(el + ' - ' +str(kk))
    
counts = df_show['points']
    
#p = figure(x_range=takeOff2, title="Score",
#            toolbar_location=None, tools="")

#p.vbar(x=takeOff2, top=counts,width=0.8)



p = figure(x_range=pilot2, title="TOP 30 score",
            toolbar_location=None, tools="")

p.vbar(x=pilot2, top=counts,width=0.8)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = 3.14/2
st.bokeh_chart(p, use_container_width=True)

st.write('TOP 100')
st.dataframe(df_show.head(100))


#elif add_radio == "Vue pilote":
st.subheader("Vue pilote")
pilot = st.selectbox(
    "Selection du pilote",
    df['pilot'].unique()
)

df_select = df[df['pilot'] == pilot].sort_values('points',ascending = False)
st.dataframe(df_select)
df_select_plt = df_select['points']  

#st.write(df_select['date'].dtype)
date = df_select['date']
flight_id = df_select['flight_id']
takeOff = df_select['takeOff']
takeOff2 =[]
kk=0
for el in takeOff:
    kk += 1
    takeOff2.append(el + ' - ' +str(kk))
    
counts = df_select['points']
    
p = figure(x_range=takeOff2, title="Meilleur score",
            toolbar_location=None, tools="")

p.vbar(x=takeOff2, top=counts,width=0.8)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = 3.14/2
st.bokeh_chart(p, use_container_width=True)

#elif add_radio == "Vue Club":
st.subheader("Vue Club")
pilot = st.selectbox(
    "Selection du club",
    df['club'].sort_values().unique()
)

df_select = df[(df['club'] == pilot)].sort_values('points',ascending = False)

sel_cat = st.multiselect('Catégorie d''aile selectionnée : ',list(df_select['aile_class'].unique()),list(df_select['aile_class'].unique()))

df_select = df[(df['club'] == pilot) & (df['aile_class'].isin(sel_cat))].sort_values('points',ascending = False)

df_select['Classement'] = range(0,df_select.shape[0]) 
df_select['Classement'] = df_select['Classement'] + 1

df_select = df_select.set_index('Classement')

st.dataframe(df_select)

#df_select_plt = df_select['points']  

df_select = df_select[df_select.index <30]

date = df_select['date']
flight_id = df_select['flight_id']
takeOff = df_select['takeOff']
takeOff2 =[]
kk=0
for el in takeOff:
    kk += 1
    takeOff2.append(el + ' - ' +str(kk))

pilot = df_select['pilot']
pilot2 =[]
kk=0
for el in pilot:
    kk += 1
    pilot2.append(el + ' - ' +str(kk))
    
counts = df_select['points']
    
#p = figure(x_range=takeOff2, title="Score",
#            toolbar_location=None, tools="")

#p.vbar(x=takeOff2, top=counts,width=0.8)



p = figure(x_range=pilot2, title="TOP 30 score",
            toolbar_location=None, tools="")

p.vbar(x=pilot2, top=counts,width=0.8)

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = 3.14/2
st.bokeh_chart(p, use_container_width=True)
    
st.subheader('Nombre de vols par semaine')
df_show = df[["year","week","points"]].groupby(['year','week']).sum()
df_show = df_show.sort_values(['year' , 'week'],ascending = True)

df_show_count = df[["year","week","points"]].groupby(['year','week']).count()
df_show_count = df_show_count.sort_values(['year' , 'week'],ascending = True)

p2 = figure( title="Nombre de vols par semaine",
    toolbar_location=None, tools="",x_axis_label="n° semaine (2023-2024)")    
p2.vbar(x=df_show_count.index.get_level_values('week').to_list(), top=df_show_count['points'],width=0.8)
p2.xgrid.grid_line_color = None
p2.y_range.start = 0

st.bokeh_chart(p2, use_container_width=True)

#st.subheader('Recherche libre')
#st.dataframe(df)
