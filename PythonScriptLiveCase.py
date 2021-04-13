# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:21:46 2020

@author: kadzi
"""
############################# Clean and Tidy Data #################################
import pandas as pd
import numpy as np
import statistics
# Not this one 
filename = '18zp24mn.csv'
def data(filename):
    df = pd.read_csv(filename, encoding = 'iso-8859-1', na_values = ['**','** '],
                    thousands=',' )
    df = df.replace([','],'', regex = True)
    df = df[['MINNESOTA','Unnamed: 1','Unnamed: 19','Unnamed: 20']]
    df = df.drop([0,1,2,3,4])
    df = df.drop(list(range(6324,6342)))
    df.columns = ['Zip Code','Size of Adjusted Gross Income','Total Income: Number of Returns','Total Income: Amount (in thousands of $)']
    df = df.dropna(axis=0, how='all')
    df['Size of Adjusted Gross Income'] = df['Size of Adjusted Gross Income'].replace(np.nan, 'Total', regex=True)
    export_csv = df.to_csv ('MNtax2018.csv', index = None, header=True)
    return export_csv

# Not this one
def df_2019():
    df_2019 = pd.read_csv('df_2019.csv')
    S = pd.Series()
    for row in range(0,11535):
        if df_2019['race_ethnicity'][row] == 'Asian/Pacific Islander':
            S = S.append(pd.Series(df_2019['people'][row] / df_2019['POP1_ASN'][row]), 
                         ignore_index=True, verify_integrity=False)
        elif df_2019['race_ethnicity'][row] == 'Black/African American':
            S = S.append(pd.Series(df_2019['people'][row] / df_2019['POP1_BLK'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df_2019['race_ethnicity'][row] == 'Hispanic or Latino':
            S = S.append(pd.Series(df_2019['people'][row] / df_2019['POP_HSPLAT'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df_2019['race_ethnicity'][row] == 'Other or Unknown':
            S = S.append(pd.Series(df_2019['people'][row] / df_2019['POP1_OTHR'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df_2019['race_ethnicity'][row] == 'White':
            S = S.append(pd.Series(df_2019['people'][row] / df_2019['POP1_WHT'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df_2019['race_ethnicity'][row] == 'American Indian or Alaskan Native':
            S = S.append(pd.Series(df_2019['people'][row] / df_2019['POP1_AMIND'][row]),
                        ignore_index=True, verify_integrity=False) 
        else:
            continue
    S = pd.DataFrame(S)
    S.columns = ['Perc_of_ethnicityPopulation_perTract_using_SNAP']
    merged = pd.merge(df_2019,S, left_index = True, right_index = True)
    export_csv = merged.to_csv('df_2019_percent_usingSNAP.csv', index = None, header=True)
    return export_csv
    


# This one
def md():
    df_full = pd.read_csv('df_2019_full.csv')
    df = pd.read_csv('df_2019.csv')
    #ok = df[df['tract'] == 27053126200]
    l = list(dict.fromkeys(list(df['tract'])))
    s = pd.Series()
    #Base ratios
    w = pd.DataFrame({'Ratio':[0.399674494, 1.039204615,0.424685289,0.66785133,0.663710544,1],
                  'race_ethnicity': ["American Indian or Alaskan Native","Asian/Pacific Islander",
                           "Black/African American","Hispanic or Latino","Other or Unknown","White"]})
    o = pd.DataFrame({'Ratio':[0.602181927, 1.565749746,0.639865214,1.006238844,1,1.506680901],
                  'race_ethnicity': ["American Indian or Alaskan Native","Asian/Pacific Islander",
                           "Black/African American","Hispanic or Latino","Other or Unknown","White"]})
    hl = pd.DataFrame({'Ratio':[0.598448302,1.556041843,0.635897946,1,0.993799838,1.497339235],
                  'race_ethnicity': ["American Indian or Alaskan Native","Asian/Pacific Islander",
                           "Black/African American","Hispanic or Latino","Other or Unknown","White"]})
    b = pd.DataFrame({'Ratio':[0.941107461,2.446999322,1,1.572579384,1.562829136,2.354684812],
                  'race_ethnicity': ["American Indian or Alaskan Native","Asian/Pacific Islander",
                           "Black/African American","Hispanic or Latino","Other or Unknown","White"]})
    a = pd.DataFrame({'Ratio':[0.384596535,1,0.408663783,0.64265624,0.638671667,0.962274403],
                  'race_ethnicity': ["American Indian or Alaskan Native","Asian/Pacific Islander",
                           "Black/African American","Hispanic or Latino","Other or Unknown","White"]})
    ami = pd.DataFrame({'Ratio':[1,2.600127427,1.062577911,1.670988116,1.660627718,2.502036067],
                  'race_ethnicity': ["American Indian or Alaskan Native","Asian/Pacific Islander",
                           "Black/African American","Hispanic or Latino","Other or Unknown","White"]})
    for GEOID in l:
        mdian = list()
        GEOIDframe = df[df['tract'] == GEOID]
        wht = [90321] * GEOIDframe['POP1_WHT'].unique().tolist()[0]
        mdian.extend(wht)
        other = [59947] * GEOIDframe['POP1_OTHR'].unique().tolist()[0]
        mdian.extend(other)
        hsplat = [60321] * GEOIDframe['POP_HSPLAT'].unique().tolist()[0]
        mdian.extend(hsplat)
        blk = [38358] * GEOIDframe['POP1_BLK'].unique().tolist()[0]
        mdian.extend(blk)
        asn = [93862] * GEOIDframe['POP1_ASN'].unique().tolist()[0]
        mdian.extend(asn)
        amind = [36099] * GEOIDframe['POP1_AMIND'].unique().tolist()[0]
        mdian.extend(amind)
        res = int(statistics.median(mdian)) 
        if res == 90321:
            merged = pd.merge(GEOIDframe,w, on = ['race_ethnicity'])
            s = s.append(merged['median_income_ffiec'] * merged['Ratio'],
                         ignore_index=True, verify_integrity=False)
        elif res == 59947:
            merged = pd.merge(GEOIDframe,o, on = ['race_ethnicity'])
            s = s.append(merged['median_income_ffiec'] * merged['Ratio'],
                         ignore_index=True, verify_integrity=False)
        elif res == 60321:
            merged = pd.merge(GEOIDframe,hl, on = ['race_ethnicity'])
            s = s.append(merged['median_income_ffiec'] * merged['Ratio'],
                         ignore_index=True, verify_integrity=False)
        elif res == 38358:
            merged = pd.merge(GEOIDframe,b, on = ['race_ethnicity'])
            s = s.append(merged['median_income_ffiec'] * merged['Ratio'],
                         ignore_index=True, verify_integrity=False)
        elif res == 93862:
            merged = pd.merge(GEOIDframe,a, on = ['race_ethnicity'])
            s = s.append(merged['median_income_ffiec'] * merged['Ratio'],
                         ignore_index=True, verify_integrity=False)
        elif res == 36099:
            merged = pd.merge(GEOIDframe,ami, on = ['race_ethnicity'])
            s = s.append(merged['median_income_ffiec'] * merged['Ratio'],
                         ignore_index=True, verify_integrity=False)
        else:
            print(f'error Here {GEOID}')
    s = pd.DataFrame(s, columns=['AdjustedByMedianIncome'])
    final = pd.merge(df,s,left_index=True,right_index=True)
    #final.to_csv('df_2019_By_Median_December.csv', index = None, header=True)   
    return final     



def df():
    df = pd.read_csv('df.csv')
    S = pd.Series()
    for row in range(0,48263):
        if df['race_ethnicity'][row] == 'Asian/Pacific Islander':
            S = S.append(pd.Series(df['people'][row] / df['POP1_ASN'][row]), 
                         ignore_index=True, verify_integrity=False)
        elif df['race_ethnicity'][row] == 'Black/African American':
            S = S.append(pd.Series(df['people'][row] / df['POP1_BLK'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df['race_ethnicity'][row] == 'Hispanic or Latino':
            S = S.append(pd.Series(df['people'][row] / df['POP_HSPLAT'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df['race_ethnicity'][row] == 'Other or Unknown':
            S = S.append(pd.Series(df['people'][row] / df['POP1_OTHR'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df['race_ethnicity'][row] == 'White':
            S = S.append(pd.Series(df['people'][row] / df['POP1_WHT'][row]),
                         ignore_index=True, verify_integrity=False)
        elif df['race_ethnicity'][row] == 'American Indian or Alaskan Native':
            S = S.append(pd.Series(df['people'][row] / df['POP1_AMIND'][row]),
                        ignore_index=True, verify_integrity=False) 
        else:
            continue
    S = pd.DataFrame(S)
    S.columns = ['Perc_of_ethnicityPopulation_perTract_using_SNAP']
    merged = pd.merge(df,S, left_index = True, right_index = True)
    export_csv = merged.to_csv('df_SNAP.csv', index = None, header=True)
    return export_csv
        


def t():
    df = pd.read_csv('snap_analysis.txt')
    return df.to_csv('snap_analysis.csv', index = None, header = True)
