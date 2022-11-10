from bs4 import BeautifulSoup, NavigableString
from tqdm import tqdm
import requests, json, re, time


def fill_front_of_string(string, fillnum, fillchar):
    retstart = ''
    retlength = fillnum - len(string)
    if retlength > 0:
        retstart = ''.join([fillchar for i in range(retlength)])
    return retstart + string

serebii_base_url = 'https://www.serebii.net'
serebii_pokedex_url = 'https://www.serebii.net/pokedex/'

pokedex_page_html = requests.get(serebii_pokedex_url).content
soup = BeautifulSoup(pokedex_page_html, 'html.parser')
dex_table = soup.find('table', 'dextab')
dex_links = dex_table.find_all('a')

pokedex_link_dict = {}
for link in dex_links:
    pokedex_link_dict[link.get_text()[:-4]] = link['href']

pokedex_link_dict = {'Gen IV': '/pokedex-dp/'}
pokemon_by_gen_and_number_link_dict = {}
for gen, link in pokedex_link_dict.items():
    pokemon_by_gen_and_number_link_dict[gen] = []
    pokedex_page_html = requests.get(serebii_base_url + link).content
    soup = BeautifulSoup(pokedex_page_html, 'html5lib')

    pkmn_menu_items = soup.find_all('select', attrs={'name':'SelectURL'})

    for pkmn_menu in pkmn_menu_items:
        parent_option = pkmn_menu.find('option')
        if parent_option:
            if any([x.isdigit() for x in re.split('[ -]', parent_option.get_text().strip())]):
                options = pkmn_menu.find_all('option')[1:]
                # print(options)
                pokemon_by_gen_and_number_link_dict[gen] += [{'pkmn_link': o['value'], 'pkmn_index': o.get_text().strip().split(' ')[0], 'pkmn_name': o.get_text().strip().split(' ')[1]} for o in options]

# f = open('/root/linode_api/serebii_scraper/pokemon_info_by_gen.json', 'w')
# json.dump(pokemon_by_gen_and_number_link_dict, f)
# f.close()
# quit()

pokemon_by_gen_and_number_link_dict

pokemon_info_by_gen_dict = {}
for gen, link_info in pokemon_by_gen_and_number_link_dict.items():
    pokemon_info_by_gen_dict[gen] = {}
    for pkmn_info in tqdm(link_info):

        pokedex_page_link = serebii_base_url + pkmn_info['pkmn_link']
        # print(pokedex_page_link)
        pokemon_page_html = requests.get(pokedex_page_link).content
        soup = BeautifulSoup(pokemon_page_html, 'html5lib')

        name = pkmn_info['pkmn_name']
        pokemon_info_dict = {'dex_num': pkmn_info['pkmn_index']}
        
        # set basic info
        info_tables = soup.find('div', id='content').find_all('table', 'dextable')
        if gen != 'Gen III':
            for j, info_table in enumerate(info_tables):
                
                info_body = info_table.find('tbody')
                # print(info_table)
                table_rows = [tr for tr in info_body.contents if not isinstance(tr, NavigableString)]

                header_row = None
                for i, table_row in enumerate(table_rows):
                    # print(i)
                    # print(table_row)
                    # if i % 2 == 1: # change logic to strip out all empty
                    #     continue
                    if i % 2 == 0:
                        header_row = table_row
                    else:
                        # print(table_row)
                        try:
                            # header_names = [child.get_text() for child in header_row.children if child.get_text().strip() != '']
                            header_names = [child.get_text().strip() for child in header_row.children if not isinstance(child, NavigableString)]
                        except:
                            continue
                        # print(header_names)
                        if len(header_names) <= 0:
                            continue
                        if header_names[0] == 'Picture':
                            continue
                        # print(list(table_row.children))
                        for info_i, info_child in enumerate([child for child in table_row.children if not isinstance(child, NavigableString)]):
                            if len(header_names) < 1 or info_i >= len(header_names):
                                break
                            # custom for Ability, Experience Points (pts, category), effort values (split if multi), fix No. 
                            if header_names[info_i] == 'Type':
                                pokemon_info_dict[header_names[info_i]] = [type_info['href'][type_info['href'].rfind('/')+1:type_info['href'].rfind('.')] for type_info in info_child.find_all('a')]
                            elif header_names[info_i] == 'Gender Ratio':
                                pokemon_info_dict[header_names[info_i]] = [str(info_child.get_text().strip()[:info_child.get_text().strip().find('%')+1]), str(info_child.get_text().strip()[info_child.get_text().strip().find('%')+1:])]
                                pokemon_info_dict[header_names[info_i]] = dict(zip([x[:x.find(':')].strip() for x in pokemon_info_dict[header_names[info_i]]], [x[x.find(':')+1:].strip() for x in pokemon_info_dict[header_names[info_i]]]))
                            else:
                                pokemon_info_dict[header_names[info_i]] = [x for x in re.split(r'[\n\t]', info_child.get_text().strip()) if len(x) > 0]
                                if all([x.find(':') >= 0 for x in pokemon_info_dict[header_names[info_i]]]):
                                    pokemon_info_dict[header_names[info_i]] = dict(zip([x[:x.find(':')].strip() for x in pokemon_info_dict[header_names[info_i]]], [x[x.find(':')+1:].strip() for x in pokemon_info_dict[header_names[info_i]]]))

                if j == 1:
                    break
        pokemon_info_by_gen_dict[gen][name] = pokemon_info_dict
        # break
            

f = open('/root/linode_api/serebii_scraper/pokemon_info_by_gen.json', 'w')
json.dump(pokemon_info_by_gen_dict,f)
f.close()