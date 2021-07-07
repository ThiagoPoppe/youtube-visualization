import os
import json
import argparse

from glob import glob
from os.path import join as ospj

import pandas as pd
from tqdm import tqdm

def get_country(filename):
    key_name = filename.split('/')[-1]
    return key_name[:2]

def get_country_encoding(country):
    if country in ('RU', 'KR', 'JP', 'IN'):
        return 'ISO-8859-1'
    
    return 'latin1' if country == 'MX' else 'utf-8'

def standarize_dates(df):
    df['publish_time'] = pd.to_datetime(df['publish_time']).dt.normalize()
    df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m', utc=True)

    return df

def read_category_data(filepath):
    with open(filepath, 'r') as f:
        category_json = json.load(f)
    
    category_data = []
    for item in category_json['items']:
        category_id = int(item['id'])
        category_name = item['snippet']['title']
        category_data.append((category_id, category_name))
        
    category_data = pd.DataFrame(category_data, columns=['category_id', 'category_name'])    
    return category_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--datapath', type=str, required=True, help='Path to folder containing YouTube trending data')
    args = parser.parse_args()
   
    csv_files = glob(ospj(args.datapath, '*.csv'))
    json_files = glob(ospj(args.datapath, '*.json'))

    print('Reading country data...')
    youtube_data = {}
    for file in tqdm(csv_files):
        country = get_country(file)
        country_data = pd.read_csv(file, encoding=get_country_encoding(country))
        youtube_data[country] = standarize_dates(country_data)

    print('Reading category data...')
    category_data = {}
    for file in tqdm(json_files):
        country = get_country(file)
        category_data[country] = read_category_data(file)

    print('Merging country and category data...')
    country_list = youtube_data.keys()
    for country in tqdm(country_list):
        youtube_data[country] = youtube_data[country].merge(category_data[country], on=['category_id'])
    
    basepath = ospj(args.datapath, 'processed')
    os.makedirs(basepath, exist_ok=True)

    print('Saving final dataframes...')
    for country in tqdm(country_list):
        filename = ospj(basepath, f'{country}data.csv')
        youtube_data[country].to_csv(filename, index=False)