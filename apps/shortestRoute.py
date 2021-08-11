import pandas as pd
from math import cos, asin, sqrt
import streamlit as st
import base64

def app():
    st.sidebar.header('User Input Features')
    st.sidebar.write('Enter coordinates of your starting point')
    
    st.write("""
# Minimum Route for The SalesPerson
This app finds the **minimum route** that the sales person should follow inorder to minimize the travel cost , 
keeping in mind that he can travel to only 12 stores a day.

**NOTE :** The distance is calculated using **Haversine Formula** which may vary from the actual distance.


""")
    
    
    data = pd.read_csv('Data Test - Sheet1.csv')
    df=data.copy()
    df=df.sort_values(by=['Latitude','Longitude'])
    df=df.reset_index(drop=True)
    df['Visited'] = 0

    
    def distance(lat1, lon1, lat2, lon2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
        return 12742 * asin(sqrt(a))
    
    
    #find the store closest to the cuurent location
    
    
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
    
    st.header('Enter the day you want to view')
    user_day = st.text_area("Day input (clear the text field and enter the day you wan to view. Enter -1 if you want to view all the days)", height=50 )              
    # display the index of the next 12 stores that he should go to
    d = pd.DataFrame()
    
    for day in range(1,(340//12)+2):
        
        ind=[]
        lat=float(latitude)
        lon=float(longitude)
        index=next(lat,lon)
        
        while len(ind) != 12 and index !=-1:
            df['Visited'][index]=1
            ind.append(index)
            lat=df['Latitude'][index]
            lon=df['Longitude'][index]
            index=next(lat,lon)
                 
                
        lat=float(latitude)
        lon=float(longitude)
        for i in ind:
            dist= distance(lat,lon,df['Latitude'][i],df['Longitude'][i])
            lat=df['Latitude'][i]
            lon=df['Longitude'][i]
            d = d.append({"Day":day,"Company Name":df['Company Name'][i],"Phone":df["Phone"][i],"Link":df["Link"][i],"Address":df['Address'][i],
                             "Pin Code":df['Pin Code'][i],"Distance":dist},ignore_index=True)
    
    
    
    st.header('INPUT (Origin Location)')
    st.write("Origin( " +str(latitude) + " , " + str(longitude) +" )")
    
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="minimalRoute.csv">Download CSV File</a>'
        return href
    
    st.header('OUTPUT (The Minimum Route)')
    if(user_day not in ""):
        for day in range(1,(340//12)+2):
            display = pd.DataFrame()
            display=d[d['Day']==day].copy()
            display.drop(columns=["Day"],inplace=True)
            if(int(user_day)==day):
                st.subheader("Day - "+str(day))
                st.dataframe(display)
                st.markdown(filedownload(display), unsafe_allow_html=True)
                st.subheader("Detailed trip info -")
                for i in range (12*(day-1),12*(day-1)+12):
                    if i<=339:
                        st.subheader("Trip - "+str(i+1))
                        st.write('Company Name - '+ str(display['Company Name'][i]))
                        st.write('Address - '+ str(display['Address'][i]))
                        st.write('Pin Code - '+ str(display['Pin Code'][i]))
                        st.write('Distance from current trip - '+ str(display['Distance'][i]))
            elif(int(user_day)==-1):
                st.subheader("Day - "+str(day))
                st.dataframe(display)
                st.markdown(filedownload(display), unsafe_allow_html=True)
