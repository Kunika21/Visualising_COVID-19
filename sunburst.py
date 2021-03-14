import pycountry
import plotly.express as px
import pandas as pd
import sys
import os
import numpy as np
import pycountry_convert as pc

# ----------- Step 1 ------------
URL_DATASET = r'/home/kunika/Desktop/Data_viz/Datathon_3/COVID19/archive/covid_19_data.csv'
df = pd.read_csv(URL_DATASET)
df = df.replace({"Mainland China": "China", "Macau": "Macao", "South Korea" : "Korea, Republic of", "Ivory Coast": "Côte d'Ivoire", "North Ireland" : "United Kingdom of Great Britain", "Congo (Brazzaville)": "Congo", "Republic of Ireland" : "Ireland", "St. Martin" : "Saint Martin (French part)","('St. Martin',)": "Saint Martin (French part)", "occupied Palestinian territory":"Palestine, State of", "Congo (Kinshasa)":"Congo, The Democratic Republic of the",


                "Bahamas, The": "Bahamas", "Gambia, The" : "Gambia", "Channel Islands" :"United Kingdom", "Cape Verde" : "Cabo Verde", "East Timor" :"Timor-Leste","Laos": "Lao People's Democratic Republic", "Burma" : "Myanmar", "West Bank and Gaza":"Palestine, State of" , "US" : "United States", "UK" : "United Kingdom"})

print(df)
# df = df.replace(r'^\s*$', "Unknown", regex=True)


df = df[(df[sys.argv[1]] != 0)]
df = df[(df["Province/State"] != "Recovered")]

list_countries = df['Country/Region'].unique().tolist()
# print(list_countries) # Uncomment to see list of countries
d_continent = {}  # To hold the country names and their ISO
for country in list_countries:
    try:
        # country_data = pycountry.countries.search_fuzzy(country)
        # print(country_data)
        # country_data is a list of objects of class pycountry.db.Country
        # The first item  ie at index 0 of list is best fit
        # object of class Country have an alpha_3 attribute
        country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        d_continent.update({country: continent_name})

    except:
        print('could not add ISO 3 code for ->', country)
        # If could not find country, make ISO code ' '
        d_continent.update({country: ' '})



# print(d_country_code) # Uncomment to check dictionary  

# create a new column iso_alpha in the df
# and fill it with appropriate iso 3 code
for k, v in d_continent.items():
    df.loc[(df["Country/Region"] == k), 'Continents'] = v

df = df.replace({np.nan: "Unknown"})

print(df["Continents"])
# print(df.loc[[36]])

# continents = {}
# list_iso = df['iso_alpha'].unique().tolist()
# for country in iso_alpha:

print(df[df["Country/Region"] == "United States"].to_string())
col = lambda x: "Aggrnyl_r" if sys.argv[1] == "Confirmed" else ("Bluered" if sys.argv[1] == "Deaths" else "RdYlBu")

fig = px.sunburst(df, path=['Continents','Country/Region', 'Province/State'], values= sys.argv[1],
                  color=df["Continents"], hover_data= ['Province/State'],
                  # animation_frame= "ObservationDate",
                  color_continuous_scale=col(sys.argv[1]),
                  # insidetextorientation='radial',
                  color_continuous_midpoint=np.average(df[sys.argv[1]], weights=df[sys.argv[1]]))

# fig.show()



head, tail = os.path.split(URL_DATASET)

if os.path.exists(head + '/Results/sunburst'):
    pass
else:
    os.makedirs(head + '/Results/sunburst')

results_dir = head + '/Results/sunburst/'

fname = sys.argv[1] + ".html"

fig.write_html(os.path.join(results_dir + fname))