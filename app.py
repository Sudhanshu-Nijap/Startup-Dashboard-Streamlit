import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(layout='wide', page_title='StartUp Analysis')

# Load data
try:
    df = pd.read_csv('startup_cleaned.csv')
except Exception as e:
    st.error(f"Error loading data: {e}")

def load_investor_details(investor):
    st.title(investor)
    last_5df = df[df['Investors'].str.contains(investor)].head(5)[['Date', 'Startup', 'Vertical', 'City', 'Round', 'Amount']].set_index('Date')
    if last_5df.empty:
        st.warning("No recent investments found for this investor.")
        return
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)

    big_5df = df[df['Investors'].str.contains(investor)].groupby('Startup')['Amount'].sum().sort_values(ascending=False).head()
    st.subheader('Biggest Investments')
    fig, ax = plt.subplots()
    ax.bar(big_5df.index, big_5df.values)
    ax.set_ylabel('Amount')
    ax.set_title('Top 5 Investments')
    st.pyplot(fig)

st.sidebar.title('StartUp Funding Analysis')
options = st.sidebar.selectbox('Select One', ['Overall Analysis', 'StartUp', 'Investor'])

if options == 'Overall Analysis':
    st.title('Overall Analysis')
    # Add overall analysis visuals here
elif options == 'StartUp':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['Startup'].unique().tolist()))
    if st.sidebar.button('Find StartUp Details'):
        st.title(selected_startup)
        startup_data = df[df['Startup'] == selected_startup]
        st.dataframe(startup_data)
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['Investors'].str.split(',').sum())))
    if st.sidebar.button('Find Investor Details'):
        load_investor_details(selected_investor)
