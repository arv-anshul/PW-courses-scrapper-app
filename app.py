from typing import Literal
import streamlit as st
import pandas as pd
import json
from pwskills_scraper import enhance_my_data

# --- Page config ---
st.set_page_config('PW Skills Courses', '📚', layout='wide')


def course_overview(inst_fp, ovv_fp):
    instructors = overview = dict()

    with open(ovv_fp, 'r') as ovv:  # importing the overview.json file
        overview = json.load(ovv)
    with open(inst_fp, 'r') as inst:  # importing the instructor.json file
        instructors = json.load(inst)

    st.title(f'👁️‍🗨️ Overview of {choice2} Course by PW Skills.')

    # Make a 2 columns section for instructor {links | description}
    with st.expander(f'**:male-teacher: &nbsp; Instructors Details - {len(instructors)}**', True):
        for meta in instructors.values():
            # inst_social = meta['social'].values()
            st.write(f'''
                ### :male-teacher: &nbsp; {meta['name']} \n
                ##### E-mail : {meta['email']}
                ''')
            for key, value in meta['social'].items():
                st.write(f""" 
                ##### {key.capitalize()} : {value}
                """)
            '---'

    with st.expander(f'**:notebook: &nbsp; What you have learn from this Course - {len(overview["learn"])}**'):
        for meta in overview['learn']:
            st.write(f':notebook: &nbsp; {meta}')

    with st.expander(f'**:bookmark: &nbsp; Features of this Course - {len(overview["features"])}**'):
        for meta in overview['features']:
            st.write(f':bookmark: &nbsp; {meta}')


def df_summary(df: pd.DataFrame):
    start = df['start_date'].dt.strftime('%d %b')[0]
    last = df['last_date'].dt.strftime('%d %b')[len(df)-1]
    with st.expander('Summary', True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Start Date', start)
        col2.metric('Course of Days',
                    df['n_days'].sum(), help='No. of days classes will be conducted.')
        col3.metric(
            'No. of Topics', df.shape[0], help='No. of different topics will be covered.')
        col4.metric('Start Date', last)


def present_df(df: pd.DataFrame, what: Literal['curriculum', 'projects']):
    if what == 'curriculum':
        topic_list = df['start_date'].dt.strftime(
            '%d %b') + ' - ' + df['title']
        text = 'Select topic to see sub-topics'
        topic = str(st.selectbox(text, options=topic_list)).split(' - ')[1]
    else:
        topic_list = df['title'].values
        text = 'Select course topic to see related projects'
        topic = str(st.selectbox(text, options=topic_list))

    parts = df.query('title==@topic')['parts'].values[0]

    # Replace all anomalies with str.replace method.
    parts = str(parts).replace("', '", '", "').replace(
        "['", '["').replace("']", '"]').replace("][", ', ').replace('", \'', '", "')

    # Turn the resultant string into a list.
    parts = json.loads(parts)

    # Display the subparts as a unordered list
    st.write(f'### :notebook: {topic} - {len(parts)}')

    if what == 'projects':
        project_date = df.query('title==@topic')['date'].values[0]
        st.write(
            '#### &nbsp;', f'▶▶ Held by _{project_date}_.'.upper())

    for i in parts:
        st.write(f'&nbsp; &nbsp; ✒ &nbsp; {i}')


def pr_summary(pr: pd.DataFrame):
    start = pr['date'].str.replace(r'[- 2023]', ' ', regex=True)[0]
    last = pr['date'].str.replace(r'[- 2023]', ' ', regex=True)[len(pr)-1]
    with st.expander('Summary', True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Type of Projects', len(pr))
        col2.metric('No.of Projects', pr['n_parts'].sum())
        col3.metric('First Project Date', start)
        col4.metric('Last Project Date', last)


# --- Sidebar ---
st.sidebar.title('PW Skills Courses')
choice1 = st.sidebar.selectbox('Choose Type', ['Paid', 'Free'])
choice2 = ''

# --- Variables ---
folder_path = './data_files/'
filename_list = ['DS', 'JAVA', 'WEB_DEV']
ex_name_list = ['-main.csv', '-projects.csv',
                '-instructor.json', '-overview.json']

match choice1:
    case 'Paid':
        choice2 = st.sidebar.selectbox(
            'Choose Course', ['Data Science', 'Web Development', 'Java'])
    case 'Free':
        st.title('Free courses are not processed.')


# Getting all filenames for respective course selection from the user
fp_names: list[str] = []
match choice2:
    case 'Data Science':
        fp_names = [folder_path+filename_list[0]+j for j in ex_name_list]
    case 'Java':
        fp_names = [folder_path+filename_list[1]+j for j in ex_name_list]
    case 'Web Development':
        fp_names = [folder_path+filename_list[2]+j for j in ex_name_list]

df = pd.read_csv(fp_names[0])
df = enhance_my_data(df)
pr = pd.read_csv(fp_names[1])

if st.sidebar.checkbox('Display Course Overview', True):
    course_overview(fp_names[2], fp_names[3])

# --- Display Course Modules ---
if st.sidebar.checkbox('Display Course Modules'):
    df_summary(df)
    st.write('---')
    present_df(df, 'curriculum')

# --- Display Course Projects ---
if st.sidebar.checkbox('Display Course Projects'):
    pr_summary(pr)
    st.write('---')
    present_df(pr, 'projects')
