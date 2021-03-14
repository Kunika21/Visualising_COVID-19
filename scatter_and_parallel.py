import json
import matplotlib.pyplot as plt
import sys
import plotly.express as px
import pandas as pd
import seaborn as sns

with open('/home/kunika/Desktop/Data_viz/Datathon_5/unece.json') as json_file:
    data = json.load(json_file)

res = [] 
for idx, sub in enumerate(data, start = 0): 
    if idx == 0: 
        res.append(sub.keys())
        res.append(sub.values())
    else: 
        res.append(sub.values())
# print(res)

#List to DF


#df = DataFrame (People_List,columns=['First_Name','Last_Name','Age'])
df = pd.DataFrame(res,columns=['Country','Year','Area', 'Total_Population', 'Population_density', 'Population_0_14_male',
                            'Population_0_14_female', 'Population_15_64_male', 'Population_15_64_female',
                            'Population_64p_male', 'Population_64p_female', 'Total_population_male_percent',
                            'Total_population_female_percent', 'Life_expec_birth_women', 'Life_expec_birth_men', 
                            'Life_expectancy_at_age65_women', 'Life_expectancy_at_age65_men', 'Total_fertility_rate',
                            'Adolescent_fertility_rate', 'Mean_age_women_at_birth_of_first_child', 'Computer_use_16_24_male',
                            'Computer_use_16_24_female', 'Computer_use_25_54_male', 'Computer_use_25_54_female', 
                            'Computer_use_55_74_male', 'Computer_use_55_74_female','Women_in_the_Labour_Force_Percent',
                            'Female_part_time_employment_percent', 'Gender_pay_gap_in_monthly_earnings',
                            'Gender_pay_gap_in_hourly_earning_wage_rate', 'Female_tertiary_students_percent',
                            'Women_Researchers_Percent', 'Female_legislators_senior_officials_managers_percent',
                            'Female_professionals_percent', 'Female_clerks_percent', 
                            'Female_craft_and_related_workers_percent', 'Female_plant_and_machine_operators_percent',
                            'Female_government_ministers_percent', 'Female_members_parliament_percent',
                            'Female_ambassadors_percent', 'Female_judges_percent', 'Women_percent_all_victims_homicides',
                            'Total_employment_growth_rate', 'Unemployment_rate', 'Youth_unemployment_rate', 
                            'Economic_acivity_rate_women_15_64', 'Economic_activity_rate_men_15_64', 
                            'GDP_at_current_prices_and_PPPs_millions_USD', 'GDP_at_current_prices_millions_of_NCUs',
                            'GDP_per_capita_current_prices_PPPs_USD', 'GDP_per_capita_current_prices_NCUs',
                            'Consumption_expenditure_per_capita_USD_PPPs', 'Purchasing_power_parity_NCU_per_USD', 
                            'Exchange_rate_NCU_per_USD','Consumer_price_index_growth_rate', 'Export_of_goods_and_services_GDP_percent',
                            'Import_of_goods_and_services_GDP_percent', 'External_balance_on_goods_and_services_GDP_percent', 
                            'GDP_in_agriculture_2005_10','GDP_in_industry_2005_10','GDP_in_services_2005_10',
                            'GDP_in_agriculture_share_GVA','GDP_in_industry_share_GVA','GDP_in_construction_share_GVA', 
                            'GDP_in_trade_share_GVA','GDP_in_finance_share_GVA',
                            'GDP_in_public_administration_share_GVA','GDP_in_other_service_share_GVA',
                            'Employment_in_agriculture','Employment_in_industry','Employment_in_construction', 
                            'Employment_in_trade', 'Employment_in_finance', 'Employment_in_public_administration',
                            'Employment_in_other_services', 'Persons_killed_road_accidents',
                            'Persons_injured_in_road_accidents', 'Total_length_of_motorways', 
                               'Total_length_of_railway_line'])
print(df.head().to_string())
#Remove the first row
df1 = df.drop(df.index[0])
df1.head()
# df1 = df1.astype(int)


# df.info()
#Convert to Numeric/Float and Country to String
#new_df = df1[["Country","Area","Total_Population","Population_density","GDP_at_current_prices_and_PPPs_millions_US$"]]
#df1['Country'] = df1['Country'].astype('|S')
cols = df1.columns.drop('Country')
df1[cols] = df1[cols].apply(pd.to_numeric, errors='coerce')

print(df1["Country"].to_string())

c = sys.argv[1]
df_country = df1.loc[df1['Country'] == c]
print(c)
#Delete 2016 as it has too many missings
df_country = df1.loc[df1['Year'] != "2016"]
df_country['Computer_use_female'] = df_country['Computer_use_16_24_female'] + df_country['Computer_use_25_54_female'] + df_country['Computer_use_55_74_female']

# print(df_us.to_string())

#Scatterplot
# 
if sys.argv[2] == "Scatter":
	df_country1 = df_country[['Country','Computer_use_female','Total_population_female_percent','Mean_age_women_at_birth_of_first_child','Economic_acivity_rate_women_15_64','Women_in_the_Labour_Force_Percent', 'Gender_pay_gap_in_monthly_earnings','Gender_pay_gap_in_hourly_earning_wage_rate', 'Women_percent_all_victims_homicides']]
	# df_country1.rename(columns = {'Women_in_the_Labour_Force_Percent' : "women_labour",'Population_density':'density' ,'Unemployment_rate':'Unemployment','Total_fertility_rate': 'fertility',
	#                 'Persons_killed_road_accidents': "killed_road_accidents",'Economic_acivity_rate_women_15_64': 'Economic acivity women','Total_length_of_motorways': "motorways"}, inplace = True) 

	sns.pairplot(df_country1)
	# fig, ax = plt.subplots()
	# ax.plot(x, y, marker='s', linestyle='none', label='small')
	plt.savefig(sys.argv[2] + "_without_hue.png")

#Parallel Coordinates: 

elif sys.argv[2] == "Parallel":
	df_wo = df_country.loc[df1['Year'] == 2015]

	df_wo_par = df_wo[['Computer_use_female','Total_population_female_percent','Mean_age_women_at_birth_of_first_child','Economic_acivity_rate_women_15_64','Women_in_the_Labour_Force_Percent', 'Gender_pay_gap_in_monthly_earnings','Gender_pay_gap_in_hourly_earning_wage_rate', 'Women_percent_all_victims_homicides']]

	#https://plotly.com/python/parallel-coordinates-plot/
	fig = px.parallel_coordinates(df_wo_par, color="Total_population_female_percent", 
		labels={'Computer_use_female':"Female_using_comp",'Total_population_female_percent':"Female_pop",'Mean_age_women_at_birth_of_first_child':"age_first_child",'Economic_acivity_rate_women_15_64':"Economic_act",'Women_in_the_Labour_Force_Percent':"Labour_force", 'Gender_pay_gap_in_monthly_earnings':"Pay_gap_monthly",'Gender_pay_gap_in_hourly_earning_wage_rate':"pay_gap_hourly", 'Women_percent_all_victims_homicides':"victims"},
	 #                                                            },
	                              color_continuous_scale=px.colors.sequential.Viridis_r)
	fig.write_html(sys.argv[2]+".html")