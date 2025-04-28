import pandas as pd
import re
from sentence_transformers import SentenceTransformer


def drop_safelinks(row):

    if '<https://eur05.safelinks.protection' in str(row):

        row = re.sub('<https://eur05.safelinks.protection.*>', '', row)


    if '[cid:' in str(row):

        row = re.sub('\[cid:.*\]', '', row)
    
    if '[signature' in str(row):

        row = re.sub('\[signature.*\]', '', row)
    
    if '<https://www' in str(row):

        row = re.sub('<https://www.*>', '', row)

    if '<br>' in str(row):

        row = row.replace('<br>', '\n')

    if '&amp;' in str(row):

        row = row.replace('&amp;', '&')
    
    if '&nbsp;' in str(row):

        row = row.replace('&nbsp;', ' ')

    if '<p>' in str(row):

        row = row.replace('<p>', '')

    if '</p>' in str(row):

        row = row.replace('<p>', '\n')

    return row


def strip_greeting(row):

    if str(row).lower().startswith('lieb'):

        print(row)
        row = re.sub('[Ll]ieb.*,', '', row)
        print(row)
    
    return row



in_file = '/Users/mariebexte/Datasets/Ticket_Similarity/structured_data.csv'

df = pd.read_csv(in_file)
print(df.columns)

# states = df.TicketState.value_counts().to_dict()
# for key, value in states.items():
#     print(key+','+str(value))

for col in ['Description', 'Solution', 'Comments\n']:

    df[col] = df[col].apply(drop_safelinks)
    # df[col] = df[col].apply(strip_greeting)

model = SentenceTransformer('all-mpnet-base-v2')


for col in ['Title', 'Description', 'Solution', 'Comments\n']:

    print('Processing colunn', col)

    df[col] = df[col].astype(str)
    df[col+'embedded'] = df[col].apply(model.encode)


df.to_pickle('embedded_tickets.pkl')
