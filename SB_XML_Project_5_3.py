import xml.etree.ElementTree as ET

import pandas as pd

# import XML data
tree = ET.parse('mondial_database.xml')
root = tree.getroot()

# 1. find 10 countries with the lowest infant mortality rates
# 3. 10 ethnic groups with the largest overall populations (sum of best/latest estimates over all countries)
# We will use the loops from question 1 and retrive info about ethnic groups as well

# create an empty data frame to hold all countries and their matching infant mortality rate & ethnic group information
ctry_info = pd.DataFrame({'country': [], 'infant_mortality': [], 'largest_ethn_grp_name': [], 'largest_ethn_percentage': []})

# loop over all countries
for cntry in root.findall('country'):
    country_nm = cntry.find('name').text
    # answer to question 1
    # extract the infant mortality rate
    if cntry.findall('infant_mortality'):
        inf_mor = cntry.find('infant_mortality').text
    # if country doesn't have infant mortality, save as empty text. This is done so we won't
    # have issue in the append statment
    else:
        inf_mor = '9999'

    # answer to question 3
    if cntry.findall('ethnicgroup'):
        # loop through all ethnic groups in country using df to save the ethnic group population and
        df = pd.DataFrame({'ethn_grp_name': [], 'ethn_percentage': []})
        for ethn in cntry.findall('ethnicgroup'):
            df = df.append({'ethn_grp_name': ethn.text, 'ethn_percentage': ethn.attrib['percentage']}, ignore_index=True)
        df['ethn_percentage'] = df['ethn_percentage'].astype(float)
        df_max = df[df['ethn_percentage'] == df['ethn_percentage'].max()].reset_index(drop=True)
    else:
        df_max = pd.DataFrame({'ethn_grp_name': ['None'], 'ethn_percentage': ['0']})
    # not necessary to print, but it helps to see the progress of each country
    print(country_nm)

    # save all the country info to one date frame from which we will answer questions 1, 3
    ctry_info = ctry_info.append({'country': country_nm, 'infant_mortality': inf_mor, 'largest_ethn_grp_name': df_max['ethn_grp_name'][0], 'largest_ethn_percentage': df_max['ethn_percentage'][0]}, ignore_index=True)


# infant mortality are saved as object, for the sorting to work properly we change dtype to float
ctry_info.infant_mortality = ctry_info.infant_mortality.astype(dtype=float)
ctry_info = ctry_info.set_index('country')

# sort the df by infant mortality in descending order and extract only the first 10 rows
print('The 10 countries with the lowest infant mortality rate are:')
print(ctry_info.sort_values('infant_mortality', axis=0, ascending=True)[0:11].infant_mortality)

# 3. 10 ethnic groups with the largest overall populations (sum of best/latest estimates over all countries)
# We will add to the country df and extract the % of the ethnic group

# largest_ethn_percentage are saved as object, for the sorting to work properly we change dtype to float
ctry_info.largest_ethn_percentage = ctry_info.largest_ethn_percentage.astype(dtype = float)

# sort the df by largest_ethn_percentage in descending order and extract only the first 10 rows
# There are several countries with 100% ethnic groups, reviewing online I can see this is bad data. This is the reason
# I am showing top 20, so we can see countries with more diversity
print('The 10 countries with the largest ethnic groups are:')
print(ctry_info.sort_values('largest_ethn_percentage', axis=0, ascending=False)[0:20][['largest_ethn_grp_name','largest_ethn_percentage']])




# 2. find 10 cities with the largest population
# create an empty data frame to hold all countries and their matching infant mortality rate
city_pop = pd.DataFrame({'cty_name': [], 'population': [], 'year': [], 'measured': []})


for cntry in list(root):
    for cty in cntry:
        if cty.tag == 'city':
            for cty_info in cty:
                if cty_info.tag == 'population':
                    city_pop = city_pop.append({'cty_name': cty.find('name').text, 'population': cty_info.text, 'year': [], 'measured': []}, ignore_index=True)
                    for key, val in cty_info.attrib.items():
                        city_pop[key].iloc[-1] = val

# population and year are saved as type object, for the sorting to work properly we change dtype to int
city_pop.population = city_pop.population.astype(int)
city_pop.year = city_pop.year.astype(int)


print('The 10 city with the largest population are:')
print(city_pop.groupby('cty_name').max().sort_values('population', axis=0, ascending=False)[0:11])

