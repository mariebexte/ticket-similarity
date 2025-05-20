import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml

from random import randint
from sentence_transformers import SentenceTransformer
from yaml.loader import SafeLoader
from utils import *


st.set_page_config(layout="wide", page_title="Ticket Similarity")


def show_app():


    in_file = 'embedded_tickets.pkl'
    colum_name_map = {'Titel': 'Title', 'Beschreibung': 'Description'}

    df = get_data(filename=in_file)
    model = get_model()

    if 'similarity_column' not in st.session_state:

        st.session_state['similarity_column'] = 'Beschreibung'

    if 'number_of_similar_tickets' not in st.session_state:

        st.session_state['number_of_similar_tickets'] = 5

    if 'similar_tickets' not in st.session_state:

        st.session_state['similar_tickets'] = pd.DataFrame()
    

    col1, col2 =  st.columns([1,2])
    with col1:

        st.subheader('Aktuelles Ticket')
        st.text_area(label='Aktuelles Ticket', label_visibility='collapsed', on_change=get_similar_tickets, args=(model, df, st.session_state['number_of_similar_tickets'], colum_name_map[st.session_state['similarity_column']]), placeholder="Kopieren Sie das aktuell bearbeitete Ticket in dieses Feld.\n\nAnschließend können Sie mit Klick auf 'Ähnliche Tickets finden' (oben rechts) die Suche starten.\n\nAlternativ können Sie diesen Prozess auch mit einem Klick außerhalb dieses Feldes starten.", height=600, key='current_ticket_description')

    with col2:

        st.subheader('Ähnliche Tickets')

        col2_1, col2_2 = col2.columns([1,1], vertical_alignment='bottom')
        
        with col2_1:

            st.slider(label='Anzahl ähnliche Tickets', min_value=1, max_value=20, key='number_of_similar_tickets')
        
        with col2_2:

            st.button('Ähnliche Tickets finden', on_click=get_similar_tickets, args=(model, df, st.session_state['number_of_similar_tickets'], colum_name_map[st.session_state['similarity_column']]))


        similar_tickets = st.session_state['similar_tickets']

        for t_num in range(len(similar_tickets)):

            st.divider()
            col2_1, col2_2 = col2.columns([1,1])

            with col2_1:

                similarity = round(similar_tickets.iloc[t_num]['sim'], 3)
                st.write('Ticket Nr. ' + similar_tickets.iloc[t_num]['TicketNo_ref'] + ' | Ähnlichkeit: ' + str(similarity))
                st.write(get_ticket_text(df=similar_tickets, ticket_number=t_num, suffix='_ref'))
        
            with col2_2:

                st.write('*Lösung*')
                st.write(get_solution_text(df=similar_tickets, ticket_number=t_num, suffix='_ref'))


### Authentication
with open('_config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

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
