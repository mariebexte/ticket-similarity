import streamlit as st
import pandas as pd
from random import randint


in_file = 'embedded_tickets.pkl'

st.set_page_config(layout="wide")


colum_name_map = {'Titel': 'Title', 'Beschreibung': 'Description'}

def get_data(filename):

    return pd.read_pickle(filename)


def get_ticket_title(df, ticket_number, suffix=''):

    return df.iloc[ticket_number]['Title'+suffix]


def get_ticket_text(df, ticket_number, suffix='', include_title=True):

    text = ''
    if include_title:
        text = '**' + df.iloc[ticket_number]['Title'+suffix] + '**\n\n'
    text = text + df.iloc[ticket_number]['Description'+suffix]

    return text


def get_solution_text(df, ticket_number, suffix=''):

    text =  df.iloc[ticket_number]['Solution'+suffix] 

    return text


def get_similar_tickets(df, ticket_number, number_of_similar_tickets, sim_col='Title'):

    # Use Title to determine similar tickets
    df_ticket = pd.DataFrame(df.iloc[ticket_number]).T
    print(df_ticket)
    df_rest = df.drop(ticket_number)

    df_cross = pd.merge(left=df_ticket, right=df_rest, how='cross', suffixes=['_ticket', '_ref'])
    print(df_cross.columns)
    df_cross['sim'] = df_cross.apply(lambda row: row[sim_col+'embedded_ticket'] @ row[sim_col+'embedded_ref'], axis=1)


    # Get n most similar
    st.session_state['similar_tickets'] = df_cross.nlargest(n=number_of_similar_tickets, columns='sim')


def pick_random_ticket(df):

    st.session_state['current_ticket_number'] = randint(0, len(df))
    reset_similar_tickets()


def reset_similar_tickets():

    st.session_state['similar_tickets'] = pd.DataFrame()


df = get_data(filename=in_file)

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

    st.text_input(label='Titel', value=get_ticket_title(df=df, ticket_number=st.session_state['current_ticket_number']))
    st.text_area(label='Beschreibung', value=get_ticket_text(df=df, ticket_number=st.session_state['current_ticket_number'], include_title=False), height=600)

with col2:

    st.subheader('Ähnliche Tickets')
    st.divider()

    col2_1, col2_2, col2_3 = col2.columns([1,1,1], vertical_alignment='bottom')
    with col2_1:
        st.slider(label='Anzahl ähnliche Tickets', min_value=1, max_value=20, key='number_of_similar_tickets')
    
    with col2_2:
        st.selectbox('Ähnlichkeit', ['Titel', 'Beschreibung'], key='similarity_column')

    with col2_3:
        st.button('Ähnliche Tickets finden', on_click=get_similar_tickets, args=(df, st.session_state['current_ticket_number'], st.session_state['number_of_similar_tickets'], colum_name_map[st.session_state['similarity_column']]))
    # st.write('Similar Tickets:')

    similar_tickets = st.session_state['similar_tickets']
    for t_num in range(len(similar_tickets)):
        st.divider()
        col2_1, col2_2 = col2.columns([1,1])

        with col2_1:

            st.markdown('*Anfrage (Ähnlichkeit: ' + str(round(similar_tickets.iloc[t_num]['sim'], 3))+')*')
            st.write(get_ticket_text(df=similar_tickets, ticket_number=t_num, suffix='_ref'))
    
        with col2_2:

            st.write('*Lösung*')
            st.write(get_solution_text(df=similar_tickets, ticket_number=t_num, suffix='_ref'))
    
