# Streamlit app for PW Skills Courses.

Clone this repository to run the web app by running following commands:

```bash
# To install streamlit library
pip install streamlit

# To open the streamlit web app in your browser
streamlit run app.py
```

## Process:

1. Scrape the PW Skills website to fect the particular course information.
2. Turn the `DataFrame` object to `csv | json` files.

```bash
# File Structure:
./data_files/
├── DS-instructor.json
├── DS-main.csv
├── DS-overview.json
├── DS-projects.csv
├── JAVA-instructor.json
├── JAVA-main.csv
├── JAVA-overview.json
├── JAVA-projects.csv
├── WEB_DEV-instructor.json
├── WEB_DEV-main.csv
├── WEB_DEV-overview.json
└── WEB_DEV-projects.csv
```

3. Made a `streamlit app` as `app.py` which displays each course information as `module` with its parts and sub-parts.

4. Now, it also shows the projects related to each course and their parts.

---

## Created by [arv-anshul](https://github.com/arv-anshul)

> I am purchasing the Data Science Course.
