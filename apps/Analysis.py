import pandas as pd
from math import cos, asin, sqrt
import streamlit as st
import base64


def app():
    st.sidebar.header('User Input Features')
    st.sidebar.write('Enter coordinates of your Location')
    st.subheader('1. Top N stores closest to your location')
    st.subheader('2. Top N highly rated stores')
    
    data = pd.read_csv('Data Test - Sheet1.csv')
    df=data.copy()
    df=df.sort_values(by=['Rating','NumReview'] , ascending=False )
    df=df.reset_index(drop=True)
    df['Visited'] = 0
    
    
    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(a))
    
    
    
    def next(lat,lon):
        min_dist = 10000.0
        min_index=-1
        for i in range(0,len(df)):
            if df['Visited'][i]==0:
                if distance(lat,lon,df['Latitude'][i],df['Longitude'][i]) < min_dist :
                    min_dist=distance(lat,lon,df['Latitude'][i],df['Longitude'][i])
                    min_index=i
                    if min_dist==0.0:
                        return min_index
        return min_index
    
    lat_input = 13.945281
    latitude = st.sidebar.text_area("Latitude input", lat_input, height=50)
    
    st.write("""
    
    """)
    
    lon_input = 77.7364
    longitude = st.sidebar.text_area("longitude input", lon_input, height=50)
    
    st.header('Enter the value of N you want')
    n_input=10
    n = st.text_area("Value of N ",n_input, height=50 ) 
    
    st.header('INPUT (Origin Location)')
    st.write("Origin( " +str(latitude) + " , " + str(longitude) +" )")
    
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="minimalRoute.csv">Download CSV File</a>'
        return href
            
    # display top n stores closest to your location
    st.header('Top N stores closest to your location - ')

    d1 = pd.DataFrame()
    ind=[]
    lat=float(latitude)
    lon=float(longitude)
    index=next(lat,lon)
    
    while len(ind) != int(n) :
        df['Visited'][index]=1
        ind.append(index)
        index=next(lat,lon)

    for i in ind:
        dist= distance(lat,lon,df['Latitude'][i],df['Longitude'][i])
        d1 = d1.append({"Company Name":df['Company Name'][i],"Phone":df["Phone"][i],"Link":df["Link"][i],"Address":df['Address'][i],
                             "Pin Code":df['Pin Code'][i],"Distance":dist},ignore_index=True)
    
    st.write(d1)
    st.markdown(filedownload(d1), unsafe_allow_html=True)
    
    # display top n highly rated stores
    d2 = pd.DataFrame()
    st.header('Top N stores that are highly rated - ')
    df.columns
    d2= df.drop(columns=['Phone','Link','Pin Code','Latitude','Longitude','Visited'])
    st.write(d2.iloc[:int(n)])
    st.markdown(filedownload(d1), unsafe_allow_html=True)