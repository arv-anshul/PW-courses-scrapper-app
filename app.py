import streamlit as st
import pandas as pd
import json
from pwskills_scraper import URLS, fetch_overview, scrape_pwskills, enhance_my_data, fetch_instructor

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


def present_df(df: pd.DataFrame):
    topic_list = df['start_date'].dt.strftime('%d %b') + ' - ' + df['title']
    topic = str(st.selectbox('Select topic to see sub-topics',
                             options=topic_list)).split(' - ')[1]

    parts = df.query('title==@topic')['parts'].values[0]

    # Replace all anomalies with str.replace method.
    parts = str(parts).replace("', '", '", "').replace(
        "['", '["').replace("']", '"]').replace("][", ', ').replace('", \'', '", "')

    # Turn the resultant string into a list.
    parts = json.loads(parts)

    # Display the subparts as a unordered list
    st.write(f'### :notebook: {topic} - {len(parts)}')
    for i in parts:
        st.write(f'&nbsp; &nbsp; ✒ &nbsp; {i}')


def present_pr(pr: pd.DataFrame):
    pass


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
        # choice2 = st.sidebar.selectbox('Choose Course', ['Data Science', 'Web Development', 'Java'])
        st.title('Free courses are not processed.')


# url = ''
# match choice2:
#     case 'Data Science':
#         url = URLS[0]
#         df = scrape_pwskills(url, 'curriculum')
#         df = enhance_my_data(df)
#         pr = scrape_pwskills(url, 'projects')

#         if st.sidebar.checkbox('Display Course Overview'):
#             course_overview(url)
#         if st.sidebar.checkbox('Display Course Modules'):
#             df_summary(df)

#     case 'Java':
#         url = URLS[1]
#         df = scrape_pwskills(url, 'curriculum')
#         pr = scrape_pwskills(url, 'projects')

#         course_overview(url)

#     case 'Web Development':
#         url = URLS[2]
#         df = scrape_pwskills(url, 'curriculum')
#         pr = scrape_pwskills(url, 'projects')

#         course_overview(url)

match choice2:
    case 'Data Science':
        fp_names = [folder_path+filename_list[0]+j for j in ex_name_list]
        df = pd.read_csv(fp_names[0])
        df = enhance_my_data(df)
        pr = pd.read_csv(fp_names[1])

        if st.sidebar.checkbox('Display Course Overview', True):
            course_overview(fp_names[2], fp_names[3])
        if st.sidebar.checkbox('Display Course Modules'):
            df_summary(df)
            st.write('---')
            present_df(df)

    case 'Java':
        fp_names = [folder_path+filename_list[1]+j for j in ex_name_list]
        df = pd.read_csv(fp_names[0])
        df = enhance_my_data(df)
        pr = pd.read_csv(fp_names[1])

        if st.sidebar.checkbox('Display Course Overview'):
            course_overview(fp_names[2], fp_names[3])
        if st.sidebar.checkbox('Display Course Modules'):
            df_summary(df)
            st.write('---')
            present_df(df)

    case 'Web Development':
        fp_names = [folder_path+filename_list[2]+j for j in ex_name_list]
        df = pd.read_csv(fp_names[0])
        df = enhance_my_data(df)
        pr = pd.read_csv(fp_names[1])

        if st.sidebar.checkbox('Display Course Overview'):
            course_overview(fp_names[2], fp_names[3])
        if st.sidebar.checkbox('Display Course Modules'):
            df_summary(df)
            st.write('---')
            present_df(df)
