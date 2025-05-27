import pandas as pd
import streamlit as st
import datetime

from sentence_transformers import SentenceTransformer
from random import randint


@st.cache_resource
def get_model(model_name='all-mpnet-base-v2'):
    
    return SentenceTransformer(model_name)


@st.cache_data
def get_data(filename):

    df = pd.read_pickle(filename)
    df = df.fillna('-')
    df['Solution'] = df['Solution'].replace({'nan': '/'})
    df['CreatedDateTime'] = df['CreatedDateTime'].apply(pd.to_datetime)

    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(days=364)

    df_dropped = df[df['CreatedDateTime'] < cutoff]
    df = df[df['CreatedDateTime'] >= cutoff]

    print('Dropped', len(df_dropped), 'tickets because they were older than a year!')

    return df


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


# def get_similar_tickets(model, df, ticket_number, number_of_similar_tickets, sim_col='Title'):

#     # Use Title to determine similar tickets
#     df_ticket = pd.DataFrame(df.iloc[ticket_number]).T
#     df_ref = df.drop(ticket_number)

#     # Check if ticket text/title was altered
#     current_title = st.session_state['current_ticket_title']
#     current_description = st.session_state['current_ticket_description']

#     if not df_ticket.iloc[0]['Title'] == current_title:

#         df_ticket.loc[:, 'Title'] = current_title
#         df_ticket['Titleembedded'] = df_ticket['Title'].apply(model.encode)
#         print('Modified title')

#     if not df_ticket.iloc[0]['Description'] == current_description:

#         df_ticket.loc[:, 'Description'] = current_description
#         df_ticket['Descriptionembedded'] = df_ticket['Description'].apply(model.encode)
#         print('Modified description')

#     set_similar_tickets(df_ticket=df_ticket, df_ref=df_ref, number_of_similar_tickets=number_of_similar_tickets, sim_col=sim_col)


def get_similar_tickets(model, df, number_of_similar_tickets, sim_col='Title'):

    # Use Title to determine similar tickets
    df_ticket = pd.DataFrame(columns=df.columns)
    df_ticket.loc[0, 'Description'] = st.session_state['current_ticket_description']
    df_ticket['Descriptionembedded'] = df_ticket['Description'].apply(model.encode)
    df_ref = df

    set_similar_tickets(df_ticket=df_ticket, df_ref=df_ref, number_of_similar_tickets=number_of_similar_tickets, sim_col=sim_col)


def pick_random_ticket(df):

    st.session_state['current_ticket_number'] = randint(0, len(df))
    reset_similar_tickets()


def reset_similar_tickets():

    st.session_state['similar_tickets'] = pd.DataFrame()

def get_html_confidence(value):

    r,g,b = rgb_from_prob(value=value)
    # r,g,b = probability_to_rgb(value)
    underline = f"3px solid rgb({r}, {g}, {b})"
    html = f"<span style='border-bottom: {underline}'>{value:.3f}</span>"
    # html = f"<span style='border-bottom: {underline}'>{round(value, 3)}</span>"
    return html

def rgb_from_prob(value, minimum=0.4, maximum=1):
    
    '''
    Based on: https://stackoverflow.com/a/20792531/3450793
    ''' 
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    r = int(max(0, 255*(1 - ratio)))
    g = int(max(0, 255*(ratio - 1)))
    b = 0
    # b = 255 - g - r
	
    return (r, g, b)


def probability_to_rgb(probability):
    """
    Convert a probability value (0-1) to an RGB color.
    
    Args:
        probability (float): A value between 0 and 1 representing probability
        
    Returns:
        tuple: RGB color values as a tuple of integers (0-255)
    """
    # Ensure probability is within valid range
    probability = max(0, min(1, probability))
    
    # Basic implementation: use a color gradient from red (low probability) to green (high probability)
    # Red component decreases as probability increases
    red = int(255 * (1 - probability))
    # Green component increases as probability increases
    green = int(255 * probability)
    # Blue remains 0
    blue = 0
    
    return (red, green, blue)