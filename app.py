import streamlit as st
import pandas as pd
import altair as alt

# Load datasets for all countries
data_us = pd.read_csv('./data/US/job_postings_by_sector_US.csv')
data_gb = pd.read_csv('./data/GB/job_postings_by_sector_GB.csv')
data_fr = pd.read_csv('./data/FR/job_postings_by_sector_FR.csv')
data_de = pd.read_csv('./data/DE/job_postings_by_sector_DE.csv')
data_ca = pd.read_csv('./data/CA/job_postings_by_sector_CA.csv')
data_au = pd.read_csv('./data/AU/job_postings_by_sector_AU.csv')

# Dictionary for country data
data_dict = {
    'US': data_us,
    'GB': data_gb,
    'FR': data_fr,
    'DE': data_de,
    'CA': data_ca,
    'AU': data_au
}

# Country flags (use emojis or image URLs)
country_flags = {
    'US': '🇺🇸',
    'GB': '🇬🇧',
    'FR': '🇫🇷',
    'DE': '🇩🇪',
    'CA': '🇨🇦',
    'AU': '🇦🇺'
}

# Select country
selected_country = st.selectbox(
    'Select a country',
    options=list(data_dict.keys()),
    format_func=lambda x: f"{country_flags[x]} {x}"
)

# Load the selected country's data
data = data_dict[selected_country]

# Convert the 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'])

# Create a Streamlit multiselect for filtering
sectors = data['display_name'].unique()
selected_sectors = st.multiselect(
    'Select sectors to display', 
    sectors, 
    default=sectors,
    key='multiselect'
)

# Filter the data based on the selected sectors
filtered_data = data[data['display_name'].isin(selected_sectors)]

# Create an Altair selection to highlight a line when clicked
highlight = alt.selection_single(fields=['display_name'], empty='none')

# Base chart with all lines
base = alt.Chart(filtered_data).mark_line().encode(
    x='date:T',
    y='indeed_job_postings_index:Q',
    color=alt.condition(highlight, 'display_name:N', alt.value('lightgray')),  # Highlight selected line
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.2)),  # Dim others
    tooltip=[
        alt.Tooltip('date:T', title='Date'), 
        alt.Tooltip('indeed_job_postings_index:Q', title='Job Posts'),
        alt.Tooltip('display_name:N', title='Sector')
    ]
).add_selection(
    highlight
).properties(
    title='Indeed Job Postings Index by Sector Over Time',
    width=1000,
    height=500
).interactive()

# Bar chart
bar_chart = alt.Chart(filtered_data).mark_bar().encode(
    x='display_name:N',
    y='sum(indeed_job_postings_index):Q',
    color='display_name:N',
    tooltip=[
        alt.Tooltip('display_name:N', title='Sector'),
        alt.Tooltip('sum(indeed_job_postings_index):Q', title='Total Job Posts')
    ]
).properties(
    title='Total Job Posts by Sector',
    width=1000,
    height=500
)

# Apply custom styles
st.markdown("""
    <style>
        [data-testid="block-container"] {
            display: flex;
            width: 100%;
            max-width: 1586px;
        }
        @media (min-width: 1024px) {
            [data-testid="block-container"] {
                padding-left: 10rem;
                padding-right: 10rem;
            }
        }
        [data-testid="stVerticalBlock"] {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        [data-testid="stArrowVegaLiteChart"] {
            display: flex;
        }
        [data-testid="stVerticalBlock"] > * + * {
            margin-top: 2.5rem; 
        }
    </style>
""", unsafe_allow_html=True)

# Add a fixed or sticky GitHub link
st.markdown("""
    <style>
        .github-link {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #f3f3f3;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 999;
        }
        .github-link a {
            text-decoration: none;
            color: #333;
            display: flex;
            align-items: center;
        }
        .github-link img {
            width: 20px;
            height: 20px;
            margin-right: 8px;
        }
    </style>
    <div class="github-link">
        <a href="https://github.com/your-repo-link" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/180px-GitHub_Invertocat_Logo.svg.png" alt="GitHub"> Find on GitHub
        </a>
    </div>
""", unsafe_allow_html=True)

# Add a custom container for charts
with st.container():
    # Display the charts in Streamlit
    st.altair_chart(base, use_container_width=True)
    st.altair_chart(bar_chart, use_container_width=True)
