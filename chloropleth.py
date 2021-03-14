import pycountry
import plotly.express as px
import pandas as pd
import sys
import os
import numpy as np
# ----------- Step 1 ------------
URL_DATASET = r'/home/kunika/Desktop/Data_viz/Datathon_3/COVID19/archive/covid_19_data.csv'
df1 = pd.read_csv(URL_DATASET)

df = df1.replace({"Mainland China": "China", "Macau": "Macao", "South Korea" : "Korea, Republic of", "Ivory Coast": "Côte d'Ivoire", "North Ireland" : "United Kingdom of Great Britain", "Congo (Brazzaville)": "Congo", "Republic of Ireland" : "Ireland", "St. Martin" : "Saint Martin (French part)","('St. Martin',)": "Saint Martin (French part)", "occupied Palestinian territory":"Palestine, State of", "Congo (Kinshasa)":"Congo, the Democratic Republic of the",


                "Bahamas, The": "Bahamas", "Gambia, The" : "Gambia", "Channel Islands" :"United Kingdom", "Cape Verde" : "Cabo Verde", "East Timor" :"Timor-Leste","Laos": "Lao People's Democratic Republic", "Burma" : "Myanmar", "West Bank and Gaza":"Palestine, State of" })
# print(df1.head) # Uncomment to see what the dataframe is like
# ----------- Step 2 ------------
list_countries = df['Country/Region'].unique().tolist()
# print(list_countries) # Uncomment to see list of countries
d_country_code = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        country_data = pycountry.countries.search_fuzzy(country)
        # country_data is a list of objects of class pycountry.db.Country
        # The first item  ie at index 0 of list is best fit
        # object of class Country have an alpha_3 attribute
        country_code = country_data[0].alpha_3
        d_country_code.update({country: country_code})
    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_country_code.update({country: ' '})

# print(d_country_code) # Uncomment to check dictionary  

# create a new column iso_alpha in the df
# and fill it with appropriate iso 3 code
for k, v in d_country_code.items():
    df.loc[(df["Country/Region"] == k), 'iso_alpha'] = v

# print(df1.head)  # Uncomment to confirm that ISO codes added
# ----------- Step 3 ------------

col = lambda x: "Tealgrn" if sys.argv[1] == "Confirmed" else ("Viridis" if sys.argv[1] == "Deaths" else "RdYlBu")

maxi = lambda x: np.max(df["Confirmed"]) if sys.argv[1] == "Confirmed" else (np.max(df["Deaths"]) if sys.argv[1] == "Deaths" else np.max(df["Recovered"]))

mini = lambda x: np.min(df["Confirmed"]) if sys.argv[1] == "Confirmed" else (np.min(df["Deaths"]) if sys.argv[1] == "Deaths" else np.min(df["Recovered"]))
fig = px.choropleth(data_frame = df, 
                    locations= "iso_alpha",
                    color= sys.argv[1],  #opts. - Confirmed, Deaths, Recovered
                    hover_name= "Country/Region",
                    color_continuous_scale= col(sys.argv[1]),  #  color scale red, yellow green
                    animation_frame= "ObservationDate",
                    range_color = [mini(sys.argv[1]), maxi(sys.argv[1])])

# fig.show()
head, tail = os.path.split(URL_DATASET)

if os.path.exists(head + '/Results/chloropleth'):
    pass
else:
    os.makedirs(head + '/Results/chloropleth')

results_dir = head + '/Results/chloropleth/'

fname = sys.argv[1] + ".html"

fig.write_html(os.path.join(results_dir + fname))
