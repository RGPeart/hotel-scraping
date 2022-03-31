import webbrowser

import pandas as pd
import numpy as np
import folium

# export du csv général
df = pd.read_csv("csv/hotel_scrap.csv", sep = ";")
df2 = pd.read_csv("csv/csv_par_site/hotelsCom_general.csv", sep=";")


# création de la carte
carte = folium.Map([48.850928, 2.346260], zoom_start=20)

# suppression des lignes jumelles pout le même hotel
df_carte = df[['gps','name','address','prices']]
df_carte2 = df2[['gps','name','address','prices']]
df_affich = pd.concat([df_carte,df_carte2],axis=0, ignore_index=True)
info_carte = df_affich.drop_duplicates(subset=['name'], ignore_index = True)

# récupération des données
x = info_carte['gps']
y = info_carte['name']
z = info_carte['address']
p = info_carte['prices']


# ajout des points sur la carte
for i in range(len(info_carte)):
    if x[i] == 'gps':
        None
    elif x[i] is not  np.nan:
        html = str(y[i]) + "<br>" + str(z[i]) + "<br>"  + str(p[i])
        iframe = folium.IFrame(html, width=200, height=100)
        popup = folium.Popup(iframe, max_width=200)
        loc = x[i].split(",")
        characters = "[]"
        latitude = ''.join( x for x in loc[0] if x not in characters)
        longitude = ''.join(x for x in loc[1] if x not in characters)
        folium.Marker([latitude, longitude], popup = popup).add_to(carte)
    else:
        None

carte.save('Carte_hotel.html')
webbrowser.open("Carte_hotel.html")
