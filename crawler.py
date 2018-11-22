import os
import sys
import time
import codecs
from random import randint

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

prefix = 'https://xn--cckza4aydug8bd3l.gamerch.com'
rare_url = 'https://xn--cckza4aydug8bd3l.gamerch.com/%E2%98%85{}'
id_fmt = '{}{}{}'

# init folders
img_dir = os.path.abspath('data/images')
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

icon_dir = os.path.abspath('data/icons')
if not os.path.exists(icon_dir):
    os.makedirs(icon_dir)



csv_header = 'ID,名字,稱號,稀有度,屬性,武器種類,國別,性別,年齡,HP(Max),攻撃力(Max),攻擊體數,攻撃段數,攻擊距離,攻撃間隔,移動速度,韌性,成長,DPS,DPS(Total),火補正,水補正,風補正,光補正,暗補正'
csv_file = 'data/characters.csv'

my_headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

if not os.path.isfile(csv_file):
    with codecs.open(csv_file, 'wb', 'utf-8') as f:
        f.write(csv_header)

df = pd.read_csv(csv_file)


def get_next_id(dataframe, prefix='^51'):
    dataframe = dataframe[dataframe['ID'].astype(str).str.contains(prefix)]
    last_id = dataframe['ID'].max()
    if pd.isnull(last_id):
        return 1
    else:
        return int(str(last_id)[2:]) + 1


rares = [5, 4, 3, 2]
for _rare in rares:
    top_rare_url = rare_url.format(_rare)
    print('Fetching Rare {} ...'.format(_rare))
    print('URL = {}'.format(top_rare_url))

    html = requests.get(top_rare_url, headers=my_headers).content
    soup = BeautifulSoup(html, 'lxml')
    tables = soup.select('table')[:5]

    for idx, table in enumerate(tables):
        trs = table.select('tbody > tr')
        for i, tr in enumerate(trs):
            uri = tr.select('td > a')[0]['href']
            fname_arr = uri[1:].split('」')
            _name = fname_arr[1].strip()
            _title = fname_arr[0][1:].strip()
            if df['稱號'].isin([_title]).any() and df['名字'].isin([_name]).any():
                print('already exists. [{}] {}'.format(_title, _name))
                continue

            detail_url = prefix + uri
            icon_url = tr.select('td > a > img')[0]['data-original']

            print('detail_url = {}'.format(detail_url))

            html = requests.get(detail_url, headers=my_headers).content
            soup2 = BeautifulSoup(html, 'lxml')

            fullname_arr = soup2.select('#js_wikidb_main_name')[0].text.strip().split('」')
            name = fullname_arr[1].strip()
            title = fullname_arr[0][1:].strip()

            next_id = get_next_id(df, '^{}{}'.format(_rare, idx+1))
            _id = id_fmt.format(_rare, idx+1, str(next_id).zfill(3))
            data_sets = {
                'ID': _id,
                '名字': name,
                '稱號': title,
                '稀有度': _rare,
            }

            div_ps = soup2.select('.ui_wikidb_top_pc > p')
            try:
                data_sets['國別'] = div_ps[0].select('a')[0].text.strip()
            except:
                # special case in https://xn--cckza4aydug8bd3l.gamerch.com/「盤上の騎士王」レオ
                data_sets['國別'] = div_ps[0].select('span')[0].next_sibling.strip()

            data_sets['年齡'] = div_ps[1].select('span')[0].next_sibling.strip().replace('歳', '')
            data_sets['性別'] = div_ps[2].select('span')[0].next_sibling.strip()
            data_sets['稀有度'] = int(div_ps[3].select('a')[0].text.strip()[-1])
            data_sets['屬性'] = div_ps[4].select('span')[0].next_sibling.strip()

            ps = soup2.select('.ui_wikidb_top_area > p')
            data_sets['成長'] = ps[0].select('span')[0].next_sibling.strip()
            data_sets['武器種類'] = ps[2].select('a')[0].text.strip()

            atk_multi = ps[3].select('span')[0].next_sibling.strip().replace('体', '')
            data_sets['攻擊體數'] = 1 if atk_multi == '' else int(atk_multi)

            atk_counts = ps[4].select('span')[0].next_sibling.strip().replace('段', '')
            data_sets['攻撃段數'] = 1 if atk_counts == '' else int(atk_counts)

            div_ps = soup2.select('.ui_wikidb_middle_pc > p')
            data_sets['HP(Max)'] = int(div_ps[2].select('span')[0].next_sibling.strip().replace(',', ''))
            data_sets['移動速度'] = div_ps[3].select('span')[0].next_sibling.strip()
            data_sets['攻擊距離'] = div_ps[4].select('span')[0].next_sibling.strip()
            data_sets['DPS'] = int(div_ps[6].select('span')[0].next_sibling.strip().replace(',', ''))

            ps = soup2.select('.ui_wikidb_middle_area > p')
            data_sets['攻撃力(Max)'] = int(ps[2].select('span')[0].next_sibling.strip().replace(',', ''))
            data_sets['攻撃間隔'] = ps[3].select('span')[0].next_sibling.strip()
            data_sets['韌性'] = ps[4].select('span')[0].next_sibling.strip()
            data_sets['DPS(Total)'] = int(ps[6].select('span')[0].next_sibling.strip().replace(',', ''))

            elems = {
                '火補正': '.zokusei_hono',
                '水補正': '.zokusei_mizu',
                '風補正': '.zokusei_kaze',
                '光補正': '.zokusei_hikari',
                '暗補正': '.zokusei_yami',
            }
            for k in elems:
                data_sets[k] = soup2.select(elems[k])[0].next_sibling.strip().replace('%', '')

            df = df.append(data_sets, ignore_index=True)

            icon_to_save = '{}/{}.jpg'.format(icon_dir, _id)
            if not os.path.isfile(icon_to_save):
                response = requests.get(icon_url, headers=my_headers)
                if response.status_code == 200:
                    with open(icon_to_save, 'wb') as f:
                        f.write(response.content)

            print('Done. id={}'.format(_id))
            time.sleep(5)

df.to_csv(csv_file, index=False)
