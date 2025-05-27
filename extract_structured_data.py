import pandas as pd
import os
import sys
import numpy as np
from tqdm import tqdm


data_path_source = '/Users/mariebexte/Datasets/Ticket_Similarity/txpe_ki_2.txt'
data_path_target = '/Users/mariebexte/Datasets/Ticket_Similarity/structured_data.csv'


def clean_line(line):

    if 'ZLI | Gebäude 8 | Raum 0B523' in line:
        line = line.replace('ZLI | Gebäude 8 | Raum 0B523', 'ZLI > Gebäude 8 > Raum 0B523')
    
    if 'Hamburger Allee 2-4 | 30161 Hannover' in line:
        line = line.replace('Hamburger Allee 2-4 | 30161 Hannover', 'Hamburger Allee 2-4 > 30161 Hannover')

    if 'huef-nrw.de<http://huef-nrw.de/> | fernuni-hagen.de<https://www.fernuni-hagen.de/>' in line:
        line = line.replace('huef-nrw.de<http://huef-nrw.de/> | fernuni-hagen.de<https://www.fernuni-hagen.de/>', 'huef-nrw.de<http://huef-nrw.de/> > fernuni-hagen.de<https://www.fernuni-hagen.de/>')
    
    if 'Mail: kroll@huef-nrw,de | markus.kroll@fernuni-hagen.de<mailto:markus.kroll@fernuni-hagen.de%0d>' in line:
        line = line.replace('Mail: kroll@huef-nrw,de | markus.kroll@fernuni-hagen.de<mailto:markus.kroll@fernuni-hagen.de%0d>', 'Mail: kroll@huef-nrw,de > markus.kroll@fernuni-hagen.de<mailto:markus.kroll@fernuni-hagen.de%0d>')

    if 'Mediendidaktik | DIGI-V.nrw' in line:
        line = line.replace('Mediendidaktik | DIGI-V.nrw', 'Mediendidaktik > DIGI-V.nrw')
    
    if 'fuer_nicht_Studierende<br>|2023-11-23 06:36:02' in line:
        line = line.replace('fuer_nicht_Studierende<br>|2023-11-23 06:36:02', 'fuer_nicht_Studierende<br>>2023-11-23 06:36:02')

    if 'Universitätsplatz 1 | 31141 Hildesheim' in line:
        line = line.replace('Universitätsplatz 1 | 31141 Hildesheim', 'Universitätsplatz 1 > 31141 Hildesheim')
    
    if 'Weblinks: https://www.fernuni-hagen.de/zli/ (https://www.fernuni-hagen.de/zli/)   |   https://www.fernuni-hagen.de/zli/ueber-uns/team.shtml (https://www.fernuni-hagen.de/zli/ueber-uns/team.shtml)' in line:
        line = line.replace('Weblinks: https://www.fernuni-hagen.de/zli/ (https://www.fernuni-hagen.de/zli/)   |   https://www.fernuni-hagen.de/zli/ueber-uns/team.shtml (https://www.fernuni-hagen.de/zli/ueber-uns/team.shtml)', 'Weblinks: https://www.fernuni-hagen.de/zli/ (https://www.fernuni-hagen.de/zli/)   >   https://www.fernuni-hagen.de/zli/ueber-uns/team.shtml (https://www.fernuni-hagen.de/zli/ueber-uns/team.shtml)')
    
    if '|<div style="margin: 0;' in line:
        line = line.replace('|<div style="margin: 0;', '><div style="margin: 0;')

    if '&nbsp;&nbsp; |&nbsp;&nbsp;' in line:
        line = line.replace('&nbsp;&nbsp; |&nbsp;&nbsp;', '&nbsp;&nbsp; >&nbsp;&nbsp;')
    
    if 'Umfrage | FernUniversität in Hagen' in line:
        line = line.replace('Umfrage | FernUniversität in Hagen', 'Umfrage > FernUniversität in Hagen')

    if ' | MOD;andreas.almatester;Andreas' in line:
        line = line.replace(' | MOD;andreas.almatester;Andreas', ' > MOD;andreas.almatester;Andreas')
    
    if ' Microsoft 365 admin | Microsoft Learn' in line:
        line = line.replace('|', '>')

    if 'FernUniversität in Hagen – Institut für wissenschaftliche Weiterbildung GmbH | Sitz: Feithstraße 152, 58097 Hagen |  Amtsgericht Hagen HRB 11392 | Geschäftsführerin Constanze Schick' in line:
        line = line.replace('|','>')
    
    if 'FernUniversität in Hagen—Institut für wissenschaftliche Weiterbildung GmbH | Sitz: Feithstraße 152, Amtsgericht Hagen HRB 11392 | Geschäftsführerin Constanze Schick' in line:
        line = line.replace('|', '>')
    
    if 'Kostenloses Microsoft Office 365 für Schulen und Schüler | Microsoft Bildung' in line:
        line = line.replace('|', '>')
    
    if 'Universitätsstraße 27 | Gebäude 5 | 58097 Hagen' in line:
        line = line.replace('|', '>')

    if 'The German Bakery | Die deutsche Bäckerei' in line:
        line = line.replace('|', '>')

    return line



elements = {}
element_num = 0
previous_lines = ''

dropped = 0

with open(data_path_source, 'r', encoding='utf-16') as file:

    for line in tqdm(file):

        # line = clean_line(line)

        if True:
        # if element_num < 5:

            # Have to break into a new entry
            if line.startswith(str(element_num+1)+'|') or line.startswith('DataID'):
                
                element_entries = previous_lines.split('|')

                # If we have more than the 9 columns, drop the line
                if len(element_entries) != 9:

                    print(element_num, element_entries[0], len(element_entries))
                    # print(previous_lines)
                    # print()
                    # for en in element_entries:
                    #     print('+++', en)
                    # sys.exit(0)

                    dropped += 1

                else:
                    elements[element_num] = element_entries
                    
                previous_lines = line
                element_num += 1

            else:
                previous_lines += line
        

print(elements[0])
df_elements = pd.DataFrame.from_dict(elements, orient='index')
df_elements.columns = df_elements.iloc[0]
df_elements = df_elements.iloc[1:]
df_elements.to_csv(data_path_target, index=None)

print('--- --- ---')
print(len(df_elements), 'READ')
print(dropped, 'DROPPED')
