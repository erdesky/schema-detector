#!/usr/bin/env python

import glob
import math
import pandas as pd
import os

def success(f, x):
    try:
        f(x)
        return True
    except:
        return False

def prec_scale(x):
    '''This function courtesy of
    https://stackoverflow.com/questions/3018758/determine-precision-and-scale-of-particular-number-in-python'''
    max_digits = 14
    try:
        int_part = int(abs(x))
        magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
        if magnitude >= max_digits:
            return (magnitude, 0)
        frac_part = abs(x) - int_part
        multiplier = 10 ** (max_digits - magnitude)
        frac_digits = multiplier + int(multiplier * frac_part + 0.5)
        while frac_digits % 10 == 0:
            frac_digits /= 10
        scale = int(math.log10(frac_digits))
    except:
        magnitude, scale = 0, 0
    return pd.Series([magnitude + scale, scale])

def parse_type(row):
    d = data[row['column_name']]
    if row['pandas_type'] in ['float64', 'int64']:
        max_ps = d.apply(prec_scale).max().tolist()
        if row['pandas_type'] == 'int64':
            if max_ps[1] <= 5:
                res = 'smallint'
            elif max_ps[1] <= 10:
                res = 'int'
            else:
                res = 'bigint'
        else:
            res = 'numeric({},{})'.format(*max_ps)
    elif success(pd.to_datetime, d):
        if pd.to_datetime(d).equals(pd.to_datetime(pd.to_datetime(d).dt.date)):
            res = 'date'
        else:
            res = 'datetime'
    else:
        res = 'nvarchar({})'.format(int(d.str.len().max()))
    return res

def schema_detect_file(file, nrows, rate):
    global data
    data = pd.read_csv(file, nrows=nrows)
    data = data.sample(int(rate * len(data))) if (rate < 1 & len(data) > 100) else data
    types = data.dtypes
    final = pd.DataFrame({'column_name': types.index, 'pandas_type': types.values})
    final['table_name'] = os.path.basename(file).split('.')[0]
    final['ansi_type'] = final.apply(parse_type, axis=1)
    return final[['table_name', 'column_name', 'ansi_type']]

def schema_detect_directory(path, nrows, rate):
    files = glob.glob(path + "/*.csv")
    tables = pd.DataFrame(columns = ['table_name', 'column_name', 'ansi_type'])
    for file in files:
        tables = tables.append(schema_detect_file(file, nrows, rate))
    return tables.sort_values(by=['table_name', 'column_name']).reset_index(drop=True)

def schema_detect(src, nrows=500, rate=1):
    '''
    Accepts a delimited file or directory containing such files
    Returns a DataFrame of table and column name(s) and ANSI data types
    '''
    return schema_detect_directory(src, nrows, rate) if os.path.isdir(src) else schema_detect_file(src, nrows, rate)
