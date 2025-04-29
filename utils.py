import pandas as pd
import streamlit as st

from sentence_transformers import SentenceTransformer
from random import randint


@st.cache_resource
def get_model(model_name='all-mpnet-base-v2'):
    
    return SentenceTransformer(model_name)


@st.cache_data
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


def set_similar_tickets(df_ticket, df_ref, number_of_similar_tickets, sim_col):

    df_cross = pd.merge(left=df_ticket, right=df_ref, how='cross', suffixes=['_ticket', '_ref'])
    df_cross['sim'] = df_cross.apply(lambda row: row[sim_col+'embedded_ticket'] @ row[sim_col+'embedded_ref'], axis=1)

    # Get n most similar
    st.session_state['similar_tickets'] = df_cross.nlargest(n=number_of_similar_tickets, columns='sim')


def get_similar_tickets(model, df, ticket_number, number_of_similar_tickets, sim_col='Title'):

    # Use Title to determine similar tickets
    df_ticket = pd.DataFrame(df.iloc[ticket_number]).T
    df_ref = df.drop(ticket_number)

    # Check if ticket text/title was altered
    current_title = st.session_state['current_ticket_title']
    current_description = st.session_state['current_ticket_description']

    if not df_ticket.iloc[0]['Title'] == current_title:

        df_ticket.loc[:, 'Title'] = current_title
        df_ticket['Titleembedded'] = df_ticket['Title'].apply(model.encode)
        print('Modified title')

    if not df_ticket.iloc[0]['Description'] == current_description:

        df_ticket.loc[:, 'Description'] = current_description
        df_ticket['Descriptionembedded'] = df_ticket['Description'].apply(model.encode)
        print('Modified description')

    set_similar_tickets(df_ticket=df_ticket, df_ref=df_ref, number_of_similar_tickets=number_of_similar_tickets, sim_col=sim_col)


def pick_random_ticket(df):

    st.session_state['current_ticket_number'] = randint(0, len(df))
    reset_similar_tickets()


def reset_similar_tickets():

    st.session_state['similar_tickets'] = pd.DataFrame()
