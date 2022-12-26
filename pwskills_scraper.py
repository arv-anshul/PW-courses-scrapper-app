import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from typing import Literal

URLS = ['https://pwskills.com/course/Data-Science-masters',
        'https://pwskills.com/course/Cracking-the-Coding-Interview-in-Java---Foundation',
        'https://pwskills.com/course/Full-Stack-web-development']


def scrape_pwskills(url: str, what: Literal['curriculum', 'projects']) -> pd.DataFrame:
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')

    tag = soup.find_all('script')
    js = json.loads(tag[20].get_text())
    program = js['props']['pageProps']['data']['meta'][what]

    df = pd.DataFrame.from_dict(program, orient='index')

    df['parts'] = df['items'].apply(
        lambda x: [i['title'] for i in x])  # type: ignore
    df['n_parts'] = df['parts'].apply(lambda x: len(x))

    def extract_date(x: str) -> str:
        x = x.replace("'23", ' 2023').replace("' 23", ' 2023')
        res = x.split()[:3]
        return '-'.join(res)

    df['date'] = df['title'].apply(extract_date)

    def filter_title(x: str) -> str:
        x = x.replace("' 23", "'23")
        return ' '.join(x.split()[2:])

    df['title'] = df['title'].apply(filter_title)

    # Additional processing on dataframe
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'id'}, inplace=True)
    df.drop(columns=['items'], inplace=True)

    return df


def enhance_my_data(data: pd.DataFrame) -> pd.DataFrame:
    title_grp = data.groupby('title')
    df = title_grp[['parts', 'n_parts']].sum(False).reset_index()

    df['n_days'] = title_grp['date'].count().values
    df['start_date'] = title_grp['date'].first().values
    df['last_date'] = title_grp['date'].last().values

    df['start_date'] = pd.to_datetime(df['start_date'])
    df['last_date'] = pd.to_datetime(df['last_date'])

    df.sort_values('start_date', inplace=True)
    df.reset_index(inplace=True)
    df.drop(columns=['index'], inplace=True)

    return df
