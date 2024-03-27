# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:36:02 2023

@author: Ronan
"""
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import streamlit as st
#import datetime as dt
from bokeh.plotting import figure 
import datetime as dt

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
        
        dict_df = {'date':date, 
                   'pilot':pilot, 
                   'points':points,
                   'club':club, 
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

# Page title
st.set_page_config(page_title='CFD explorer', page_icon='📊')
st.title('📊 Interactive CFD Explorer')

with st.expander('About this app'):
  st.markdown('**Que fait cette app?**')
  st.info('Cette app explore les classements de la CFD pour la saison 2023-2024')
  st.markdown('**Comment l''utiliser ?**')
  st.warning('Naviguez dans les menus, utilisez les filtres et ')
  
st.subheader('Which Movie Genre performs ($) best at the box office?')


st.title('CFD explorer')
#st.title('Welcome the CFD explorer!👋')

st.text('Data provided by FFVL : https://parapente.ffvl.fr')

#df = df.sort_values('points',ascending = False)
df = df.sort_values('date',ascending = False)
df['month'] = df['date'].apply(lambda x: x.month)
df['year'] = df['date'].apply(lambda x: x.year)
df['week'] = df['date'].apply(lambda x: x.week)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Selection",
        ("Introduction","Classement dernier mois", "Vue pilote","Vue Club","Contact")
    )
    
#if add_radio == "Classement par points":
#    st.dataframe(df.head(100))

if add_radio == "Introduction":
    st.text('Cette app explore les classements de la CFD, saison 2023-2024')
    st.text('Plusieurs vues sont disponibles dans la barre latérale')
    df_show = df[["year","week","points"]].groupby(['year','week']).sum()
    df_show = df_show.sort_values(['year' , 'week'],ascending = True)

    df_show_count = df[["year","week","points"]].groupby(['year','week']).count()
    df_show_count = df_show_count.sort_values(['year' , 'week'],ascending = True)

    #st.dataframe(df_show.head(100))
    #sns.barplot(penguins, x="island", y="body_mass_g")
    #st.write(df_show.index.get_level_values('week'))
    #p = figure( title="Sum points",
    #           toolbar_location=None, tools="")
    
    #p.vbar(x=df_show.index.get_level_values('week').to_list(), top=df_show['points'],width=0.8)
    #p.xgrid.grid_line_color = None
    #p.y_range.start = 0
    #st.bokeh_chart(p, use_container_width=True)

    p2 = figure( title="Nombre de vols par semaine",
        toolbar_location=None, tools="",x_axis_label="Semaine (2023-2024)")    
    p2.vbar(x=df_show_count.index.get_level_values('week').to_list(), top=df_show_count['points'],width=0.8)
    p2.xgrid.grid_line_color = None
    p2.y_range.start = 0
    
    st.bokeh_chart(p2, use_container_width=True)

if add_radio == "Classement dernier mois":
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

    st.dataframe(df_show.head(10))

elif add_radio == "Vue pilote":
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
    p.xaxis.major_label_orientation = 3.14/4
    st.bokeh_chart(p, use_container_width=True)

elif add_radio == "Vue Club":
    pilot = st.selectbox(
       "Selection du club",
       df['club'].sort_values().unique()
    )
    
    df_select = df[(df['club'] == pilot)].sort_values('points',ascending = False)

    sel_cat = st.multiselect('Catégorie d''aile selectionnée : ',list(df_select['aile_class'].unique()),list(df_select['aile_class'].unique()))

    df_select = df[(df['club'] == pilot) & (df['aile_class'].isin(sel_cat))].sort_values('points',ascending = False)

    st.dataframe(df_select)
    
    df_select_plt = df_select['points']  
    

    date = df_select['date']
    flight_id = df_select['flight_id']
    takeOff = df_select['takeOff']
    takeOff2 =[]
    kk=0
    for el in takeOff:
        kk += 1
        takeOff2.append(el + ' - ' +str(kk))
        
    counts = df_select['points']
        
    p = figure(x_range=takeOff2, title="Score",
               toolbar_location=None, tools="")
    
    p.vbar(x=takeOff2, top=counts,width=0.8)
    
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = 3.14/4
    st.bokeh_chart(p, use_container_width=True)
    
if add_radio == "Contact":
    st.write('App created by : cfdexplorer.pro@gmail.com')
  





# Load data
df = pd.read_csv('data/movies_genres_summary.csv')
df.year = df.year.astype('int')

# Input widgets
## Genres selection
genres_list = df.genre.unique()
genres_selection = st.multiselect('Select genres', genres_list, ['Action', 'Adventure', 'Biography', 'Comedy', 'Drama', 'Horror'])

## Year selection
year_list = df.year.unique()
year_selection = st.slider('Select year duration', 1986, 2006, (2000, 2016))
year_selection_list = list(np.arange(year_selection[0], year_selection[1]+1))

df_selection = df[df.genre.isin(genres_selection) & df['year'].isin(year_selection_list)]
reshaped_df = df_selection.pivot_table(index='year', columns='genre', values='gross', aggfunc='sum', fill_value=0)
reshaped_df = reshaped_df.sort_values(by='year', ascending=False)


# Display DataFrame

df_editor = st.data_editor(reshaped_df, height=212, use_container_width=True,
                            column_config={"year": st.column_config.TextColumn("Year")},
                            num_rows="dynamic")
df_chart = pd.melt(df_editor.reset_index(), id_vars='year', var_name='genre', value_name='gross')

# Display chart
chart = alt.Chart(df_chart).mark_line().encode(
            x=alt.X('year:N', title='Year'),
            y=alt.Y('gross:Q', title='Gross earnings ($)'),
            color='genre:N'
            ).properties(height=320)
st.altair_chart(chart, use_container_width=True)
