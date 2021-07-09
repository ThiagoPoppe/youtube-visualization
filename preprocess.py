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

def preprocess(df):
    data = df.copy()
    data = data.dropna()
    data['publish_time'] = data['publish_time'].apply(lambda x : x.split('T')[0])
    data['publish_time'] = pd.to_datetime(data['publish_time'])
    data['trending_date'] = pd.to_datetime(data['trending_date'], format='%y.%d.%m')

    return data

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
        country_data = pd.read_csv(file)
        youtube_data[country] = preprocess(country_data)

    print('Reading category data...')
    category_data = {}
    for file in tqdm(json_files):
        country = get_country(file)
        category_data[country] = read_category_data(file)

    print('Merging country and category data...')
    country_list = youtube_data.keys()
    for country in tqdm(country_list):
        youtube_data[country] = pd.merge(youtube_data[country], category_data[country])
    
    output_path = 'processed/'
    os.makedirs(output_path, exist_ok=True)

    print('Saving final dataframes...')
    for country in tqdm(country_list):
        filename = ospj(output_path, f'{country}data.csv')
        youtube_data[country].to_csv(filename, index=False)

    # Checking if all data was saved properly
    print('Checking integrity of saved dataframes...')
    for country in tqdm(country_list):
        filename = ospj(output_path, f'{country}data.csv')
        df = pd.read_csv(filename, parse_dates=['trending_date', 'publish_time'])
        assert youtube_data[country].equals(df)