import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from random import randint, random
from sentence_transformers import SentenceTransformer
from yaml.loader import SafeLoader
from utils import *


st.set_page_config(layout="wide")

def show_app():

    in_file = 'embedded_tickets.pkl'
    colum_name_map = {'Titel': 'Title', 'Beschreibung': 'Description'}

    df = get_data(filename=in_file)
    model = get_model()

    if 'number_of_similar_tickets' not in st.session_state:

        st.session_state['number_of_similar_tickets'] = 5

    if 'similar_tickets' not in st.session_state:

        st.session_state['similar_tickets'] = pd.DataFrame()
    

    col1, col2 =  st.columns([1,2])
    with col1:

        st.subheader('Aktuelles Ticket')
        st.divider()

        col1_1, col1_2 = col1.columns([1,1], vertical_alignment='bottom')

        with col1_1:

            st.number_input(label='Ticketnummer', min_value=0, max_value=len(df), key='current_ticket_number', on_change=reset_similar_tickets)
        
        with col1_2:

            st.button('Neues zufälliges Ticket', on_click=pick_random_ticket, args=(df, ))

        st.text_input(label='Titel', value=get_ticket_title(df=df, ticket_number=st.session_state['current_ticket_number']), key='current_ticket_title')
        st.text_area(label='Beschreibung', value=get_ticket_text(df=df, ticket_number=st.session_state['current_ticket_number'], include_title=False), height=600, key='current_ticket_description')


    with col2:

        st.subheader('Ähnliche Tickets')
        st.divider()

        col2_1, col2_2, col2_3 = col2.columns([1,1,1], vertical_alignment='bottom')
        
        with col2_1:

            st.slider(label='Anzahl ähnliche Tickets', min_value=1, max_value=20, key='number_of_similar_tickets')
        
        with col2_2:

            st.selectbox('Ähnlichkeit', ['Titel', 'Beschreibung'], key='similarity_column')

        with col2_3:
            
            st.button('Ähnliche Tickets finden', on_click=get_similar_tickets, args=(model, df, st.session_state['current_ticket_number'], st.session_state['number_of_similar_tickets'], colum_name_map[st.session_state['similarity_column']]))


        similar_tickets = st.session_state['similar_tickets']

        for t_num in range(len(similar_tickets)):

            st.divider()
            col2_1, col2_2 = col2.columns([1,1])

            with col2_1:
                similarity = round(similar_tickets.iloc[t_num]['sim'], 3)
                st.write('Similarity: ' + get_html_confidence(similarity), unsafe_allow_html=True)
                st.write(get_ticket_text(df=similar_tickets, ticket_number=t_num, suffix='_ref'))
        
            with col2_2:

                st.write('*Lösung*')
                st.write(get_solution_text(df=similar_tickets, ticket_number=t_num, suffix='_ref'))


### Authentication
with open('_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state["authentication_status"]:

    authenticator.logout(location='main', use_container_width=False)
    st.write(f'Welcome *{st.session_state["name"]}*')
    show_app()

elif st.session_state["authentication_status"] is False:

    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    
    st.warning('Please enter your username and password')
