import pandas as pd
import re
import sys
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

    if '<http' in str(row):

        row = re.sub('<http.*>', '', row)

    if '<mailto:' in str(row):

        row = re.sub('<mailto:.*>', '', row)

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

    if '</p>' in str(row):
        
        row = row.replace('</p>', '\n')

    if '</span>' in str(row):

        row = row.replace('</span>', '')

    if '<span>' in str(row):

        row = row.replace('<span> ', '')

    if '</div>' in str(row):

        row = row.replace('</div>', '')

    if '<div>' in str(row):

        row = row.replace('<div>', '')

    if '<p style' in str(row):

        row = re.sub('<p style.*>', '', row)

    if '<a rel' in str(row):

        row = re.sub('<a rel.*>', '', row)

    if '</a>' in str(row):

        row = row.replace('</a>', '')

    if '<span style' in str(row):

        row = re.sub('<span style.*>', '', row)

    if '<pre style' in str(row):

        row = re.sub('<pre style.*>', '', row)

    if '<pre>' in str(row):

        row = row.replace('<pre>', '')

    if '</pre>' in str(row):

        row = row.replace('</pre>', '')

    if '[Sie erhalten' in str(row):

        row = re.sub('\[Sie erhalten.*\]', "", row)

    if "You don't often get email from" in str(row):

        row = re.sub("You don't often get email from.*why this is important", '', row)

    if "Sie erhalten nicht häufig E-Mails" in str(row):

        row = re.sub("Sie erhalten nicht häufig E-Mails.*warum dies wichtig ist", '', row)

    if "Einige Personen, die diese Nachricht erhalten haben, erhalten nicht oft" in str(row):

        row = re.sub("Einige Personen, die diese Nachricht erhalten haben, erhalten nicht oft.*warum dies wichtig ist", '', row)

    if 'Von meinem iPhone gesendet' in str(row):

        row = row.replace('Von meinem iPhone gesendet', '')
    
    if '[Extern]' in str(row):

        row = row.replace('[Extern]', '')
    

    row = re.sub('<.*@.*>', "", str(row))
    row = re.sub('\[[0-9]*\]', "", str(row))

    row = row.strip('\n')
    row = row.strip()

    # if '[' in str(row):
    #     print(row)

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

for col in ['Title', 'Description', 'Solution', 'Comments\n']:

    df[col] = df[col].apply(drop_safelinks)
    # df[col] = df[col].apply(strip_greeting)

model = SentenceTransformer('all-mpnet-base-v2')
for col in ['Title', 'Description', 'Solution', 'Comments\n']:

    print('Processing colunn', col)

    df[col] = df[col].astype(str)
    df[col+'embedded'] = df[col].apply(model.encode)


df.to_pickle('embedded_tickets.pkl')
