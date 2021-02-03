# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 21:39:57 2021

@author: gusta
"""

# Still have to do: 
# Fix names
# Fix dates
    

import pandas as pd
import numpy as np

#%% 1. read data
    
CAT = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_CAT_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)
CEDAW = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_CEDAW_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)
CPED = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_CPED_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)
CRC = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_CRC_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)
CRPD = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_CRPD_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)
ICCPR = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_ICCPR_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)
ICERD = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_ICERD_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)
ICESCR = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_ICESCR_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198) 
ICRMW = pd.read_excel('C:/Users/gusta/Documents/Datasets/9talt/UnderlyingData_ICRMW_OHCHR_23_01_2021.xls',skiprows=[0],nrows=198)

df_list = [CAT,CEDAW,CPED,CRC,CRPD,ICCPR,ICERD,ICESCR,ICRMW]

#%% 2. add critical date

ICCPR['sdate'] = pd.to_datetime("1966-12-06")
ICESCR['sdate'] =  pd.to_datetime("1966-12-06")
ICERD['sdate'] =  pd.to_datetime("1965-12-21")
CEDAW['sdate'] =  pd.to_datetime("1980-03-01")
CRC['sdate'] =  pd.to_datetime("1989-11-20")
CAT['sdate'] =  pd.to_datetime("1984-12-10")
CRPD['sdate'] =  pd.to_datetime("1990-12-18")
ICRMW['sdate'] =  pd.to_datetime("2007-02-06")
CPED['sdate'] =  pd.to_datetime("2007-03-30")

for i in df_list:
    print(i.columns)

#%% 3. drop unnecessary variables

CAT.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure',
            'Date of acceptance of inquiry procedure'],axis=1,inplace=True)

CEDAW.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure',
            'Date of acceptance of inquiry procedure'],axis=1,inplace=True)

CPED.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure',
            'Date of acceptance of inquiry procedure'],axis=1,inplace=True)

CRC.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure',
            'Date of acceptance of inquiry procedure'],axis=1,inplace=True)

CRPD.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure',
            'Date of acceptance of inquiry procedure'],axis=1,inplace=True)

ICCPR.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure'],
            axis=1,inplace=True)

ICERD.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure'],axis=1,inplace=True)

ICESCR.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure',
            'Date of acceptance of inquiry procedure'],axis=1,inplace=True)

ICRMW.drop(['Date of Signature (dd/mm/yyyy)',
            'Date of acceptance of individual communications procedure'],
            axis=1,inplace=True)

for i in df_list:
    i.rename({'Date of Ratification/Accession':'rdate'},axis=1,inplace=True)

#%% 4. make sure dates are as dates

for i in df_list:
    pd.to_datetime(i['rdate'])
    pd.to_datetime(i['sdate'])    

#%% 5. get date differences

for i in df_list:
    i['d_diff'] = (i['rdate']-i['sdate']).dt.days

#%% 6. merge    

dfX = ICCPR.merge(ICESCR,on='Country',suffixes=('_iccpr','_icescr'))
dfX = dfX.merge(ICERD,on='Country',suffixes=(None,'_icerd'))
dfX = dfX.merge(CAT,on='Country',suffixes=(None,'_cat'))
dfX = dfX.merge(CEDAW,on='Country',suffixes=(None,'_cedaw'))
dfX = dfX.merge(CRC,on='Country',suffixes=(None,'_crc'))
dfX = dfX.merge(CRPD,on='Country',suffixes=(None,'_crpd'))
dfX = dfX.merge(CPED,on='Country',suffixes=(None,'_cped'))
dfX = dfX.merge(ICRMW,on='Country',suffixes=(None,'_icrmw'))

dfX.columns

dfX.rename({'rdate':'rdate_icerd','sdate':'sdate_icerd','d_diff':'d_diff_icerd'},
           axis=1, inplace=True)


# pd version of antijoin...
# key_diff = set(ICCPR.Country).difference(ICESCR.Country)



#%% 7. add binary col 

# in pandas you can only transmute with functions
# # works but impractical
# def binarizer(row):
#     if np.isnan(row['d_diff_cat']):
#         val = 0
#     else: 
#         val = 1
#     return val
# dfX['bin_cat'] = dfX.apply(binarizer,axis=1)

dfX['bin_iccpr'] = dfX['d_diff_iccpr'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_icescr'] = dfX['d_diff_icescr'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_icerd'] = dfX['d_diff_icerd'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_cedaw'] = dfX['d_diff_cedaw'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_cat'] = dfX['d_diff_cat'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_crc'] = dfX['d_diff_crc'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_icrmw'] = dfX['d_diff_icrmw'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_cped'] = dfX['d_diff_cped'].apply(lambda x: 0 if np.isnan(x) else 1)
dfX['bin_crpd'] = dfX['d_diff_crpd'].apply(lambda x: 0 if np.isnan(x) else 1)

#%% 8 drop unnecessary cols

dfX.info()
dfX.columns

dfXC = dfX[['Country', 'd_diff_iccpr', 'd_diff_icescr', 
            'd_diff_icerd', 'd_diff_cat', 'd_diff_cedaw', 'd_diff_crc',
           'd_diff_crpd', 'd_diff_cped', 'd_diff_icrmw', 'bin_cat',
           'bin_iccpr', 'bin_icescr', 'bin_cedaw', 'bin_crc', 'bin_icrmw',
           'bin_cped', 'bin_crpd', 'bin_icerd']]


#%% 9. save and reset

dfXC.to_csv('C:/Users/gusta/Documents/Datasets/9talt/dfXC.csv')

dfXC = pd.read_csv('C:/Users/gusta/Documents/Datasets/9talt/dfXC.csv')


#%% 10. load hdi

hdi = pd.read_csv("C:/Users/gusta/Documents/Datasets/controls/human-development-index.csv")

hdi.rename({'Entity':'Country','Human Development Index (UNDP)':'score_hdi'},
           axis = 1, inplace=True)

hdi = hdi.pivot('Country', 'Year', 'score_hdi')

key_diff = set(dfXC.Country).difference(hdi.index)
print(key_diff)
len(key_diff)

hdi = hdi.reset_index()

dfXC.Country.replace(names,inplace=True)
hdi.replace(names,inplace=True)

key_diff = set(dfXC.Country).difference(hdi.Country)
print(key_diff)
len(key_diff)



#%% load religion

religion = pd.read_csv("C:/Users/gusta/Documents/Datasets/controls/main-religion-of-the-country-in.csv")
religion.head()

religion.drop('Code',axis= 1, inplace=True)
religion.rename({'Entity':'Country'}, axis = 1, inplace=True)

religion.replace(names,inplace=True)
key_diff = set(dfXC.Country).difference(religion.Country)
print(key_diff)


#%% load gdp

gdp = pd.read_csv('C:/Users/gusta/Documents/Datasets/controls/average-real-gdp-per-capita-across-countries-and-regions.csv')
print(gdp.columns)

gdp.drop('Code',axis= 1, inplace=True)
gdp.rename({'Entity':'Country'}, axis = 1, inplace=True)
gdp.rename({'Real GDP per capita in 2011US$, multiple benchmarks (Maddison Project Database (2018))':'gdp_score',},axis=1, inplace=True)

gdp2 = gdp.pivot('Country', 'Year', 'gdp_score')
gdp2.columns
gdp2.head()
gdp2.info()
gdp2.drop(gdp2.iloc[:,0:701].columns.tolist(),axis=1,inplace=True)

# also works
# gdp2['gdp_means'] = gdp2.apply(np.mean,axis=1)

gdp2['gdp_means'] = gdp2.mean(axis=1)

gdp2['gdp_means'].hist()

gdp2.drop(gdp2.iloc[:,0:40].columns.tolist(),axis=1,inplace=True)

gdp2 = gdp2.reset_index()

gdp2.replace(names,inplace=True)
key_diff = set(dfXC.Country).difference(gdp2.Country)
print(key_diff)

#%% years of democracy

age = pd.read_csv('C:/Users/gusta/Documents/Datasets/controls/age-of-democracies.csv')
age.head()
age.columns
age.rename({'Entity':'Country', 'Age of democracies at the end of 2015 (Boix, Miller, and Rosato, 2013, 2018)': 'years_d'}, axis = 1, inplace=True)
age.drop('Code',axis=1,inplace=True)

age['years_d'] = age['years_d'].apply(lambda x: 0 if x == "Not a democracy in 2015" else x)
age['years_d'] = pd.to_numeric(age['years_d'])

age.replace(names,inplace=True)
key_diff = set(dfXC.Country).difference(age.Country)
print(key_diff)


#%% Merge

dfall =dfXC.merge(hdi,on='Country')
dfall = dfall.merge(religion, on='Country')
dfall = dfall.merge(age, on='Country')
dfall = dfall.merge(gdp2, on='Country')

dfall.columns
dfall.d_diff_iccpr.value_counts(bins=10)

dfall.to_csv('C:/Users/gusta/Documents/Datasets/controls/dfall')

#%% state standarizer

old_names = ['Bolivia (Plurinational State of)',
             "Venezuela (Bolivarian Republic of)"
             ,"Côte d'Ivoire","Iran (Islamic Republic of)",
             "Lao People's Democratic Republic",
             "Micronesia (Federated States of)",
             "State of Palestine",
             'Swaziland',
             "Syrian Arab Republic",
             "The former Yugoslav Republic of Macedonia",
             "United Kingdom of Great Britain and Northern Ireland",
             "United Republic of Tanzania",
             'Viet Nam',
             "Cote d'Ivoire",
             "Micronesia (country)",
             "United States of America",
             "Czech Republic",
             'Democratic Republic of the Congo',
             'Republic of Korea',
             'Timor-Leste',
             'Russian Federation']
new_names = ['Bolivia',
             'Venezuela',
             'Ivory Coast',
             'Iran',
             'Laos',
             'Micronesia',
             'Palestine',
             'Eswatini',
             'Syria',
             'North Macedonia',
             'United Kingdom',
             'Tanzania',
             'Vietnam',
             'Ivory Coast',
             'Micronesia',
             'United States',
             'Czechia',
             "Democratic Republic of Congo",
             'South Korea',
             'Timor',
             'Russia']

names = dict(zip(old_names,new_names))


