""" Scraper for PWSkills courses to make a DataFrame. """

import json
import os
from typing import Literal

import pandas as pd
import requests
from bs4 import BeautifulSoup


def tag_no(script_tag) -> int:
    """ This is tag number which signify the tag who cantains all the infos. """
    for i, txt in enumerate(script_tag):
        # I checked that the desired script has approx. 159060 length.
        if len(txt.text) > 10e+4:    # 10e+4 == 1,00,000
            return i
    else:
        return 20


def scrape_pwskills(url: str, what: Literal['curriculum', 'projects']) -> pd.DataFrame:
    """
    Scraper for PW SKills `paid courses`.

    Returns the DataFrame which contains the `['title', 'date', 'parts', 'n_parts']` columns.
    """
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')

    tag = soup.find_all('script')

    # Give the tag number in which the json data is stored.
    tagNo = tag_no(tag)
    js = json.loads(tag[tagNo].get_text())
    program = js['props']['pageProps']['data']['meta'][what]

    df = pd.DataFrame.from_dict(program, orient='index')

    df['parts'] = df['items'].apply(
        lambda x: [i['title'] for i in x])  # type: ignore
    df['n_parts'] = df['parts'].apply(len)

    def extract_date(x: str) -> str:
        x = x.replace("'23", ' 2023').replace("' 23", ' 2023')
        res = x.split()[:3]
        return '-'.join(res)

    df['date'] = df['title'].apply(extract_date)

    def filter_title(x: str) -> str:
        x = x.replace("' 23", "'23").replace(" '23", "'23")
        return ' '.join(x.split()[2:])

    df['title'] = df['title'].apply(filter_title)

    # Additional processing on dataframe
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'id'}, inplace=True)
    df.drop(columns=['items'], inplace=True)

    return df


def enhance_my_data(data: pd.DataFrame) -> pd.DataFrame:
    """ Enhances the given `paid course` DataFrame. """
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


def fetch_instructor(url: str) -> dict[str, dict[str, str]]:
    """ Fetches instructors names from the given course url. """
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')

    tag = soup.find_all('script')

    # Give the tag number in which the json data is stored.
    tagNo = tag_no(tag)
    js = json.loads(tag[tagNo].get_text())

    program_instructors = js['props']['pageProps']['data']['meta']['instructors']
    instructors = js['props']['pageProps']['initialState']['init']['instructors']

    instructors_details: dict[str, dict[str, str]] = {
        i: instructors[i] for i in program_instructors}
    return instructors_details


def fetch_overview(url: str) -> dict[str, list[str]]:
    """ Fetches learnning and features overview from the given course url. """
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')

    tag = soup.find_all('script')

    # Give the tag number in which the json data is stored.
    tagNo = tag_no(tag)
    js = json.loads(tag[tagNo].get_text())
    overview = js['props']['pageProps']['data']['meta']['overview']

    return {
        'learn': overview['learn'],
        'features': overview['features']
    }


def url_to_file(url: str, course_name: str) -> None:
    """ Add another PW Skills course by providing its `url` and `course_name` as arguments. """

    folder_path = './new_data_files/'
    course_name = course_name.upper()
    ex_name_list = ['-main.csv', '-projects.csv',
                    '-instructor.json', '-overview.json']

    # All DataFrames
    df: pd.DataFrame = scrape_pwskills(url, 'curriculum')
    projects: pd.DataFrame = scrape_pwskills(url, 'projects')
    instructor = fetch_instructor(url)
    overview = fetch_overview(url)

    df_list: list[pd.DataFrame] = [df, projects]
    json_list: list[dict] = [instructor, overview]

    # Create a new directory for new data files
    if not os.path.isdir('new_data_files'):
        os.mkdir('new_data_files')

    for j in range(2):
        df_list[j].to_csv(folder_path + course_name + ex_name_list[j],
                          index=False)

    for k in range(2):
        with open(folder_path + course_name + ex_name_list[k+2], 'w') as f:
            json.dump(json_list[k], f, indent=2)
