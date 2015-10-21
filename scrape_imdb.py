import requests
from bs4 import BeautifulSoup
import re
import dateutil.parser
from pprint import pprint
import pickle

url_list = ['http://www.imdb.com/title/tt0073972/',
'http://www.imdb.com/title/tt0092312/',
'http://www.imdb.com/title/tt0057729/?ref_=nv_sr_4',
'http://www.imdb.com/title/tt0086759/?ref_=fn_al_tt_1',
'http://www.imdb.com/title/tt0159206/?ref_=fn_al_tt_1',
'http://www.imdb.com/title/tt0060009/?ref_=fn_al_tt_2',
'http://www.imdb.com/title/tt0060028/?ref_=fn_al_tt_2',
'http://www.imdb.com/title/tt0081933/?ref_=nv_sr_3',
'http://www.imdb.com/title/tt0083466/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0052522/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0086817/?ref_=fn_al_tt_3',
'http://www.imdb.com/title/tt0412253/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0094517/?ref_=fn_al_tt_1',
'http://www.imdb.com/title/tt0264263/?ref_=nv_sr_6',
'http://www.imdb.com/title/tt0096697/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0052520/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0121955/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0084967/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0056757/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0303461/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0106179/?ref_=fn_al_tt_1',
'http://www.imdb.com/title/tt0111875/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0367274/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0084972/?ref_=nv_sr_6',
'http://www.imdb.com/title/tt0105950/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0055662/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0057733/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0063878/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0101084/?ref_=fn_al_tt_1',
'http://www.imdb.com/title/tt0078607/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0387199/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0088513/?ref_=nv_sr_3',
'http://www.imdb.com/title/tt0053502/?ref_=fn_al_tt_2',
'http://www.imdb.com/title/tt0094469/?ref_=nv_sr_6',
'http://www.imdb.com/title/tt0061256/?ref_=fn_al_tt_3',
'http://www.imdb.com/title/tt0058805/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0086719/?ref_=fn_al_tt_2',
'http://www.imdb.com/title/tt0493093/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0126158/?ref_=fn_al_tt_6',
'http://www.imdb.com/title/tt0064603/?ref_=nm_knf_t1',
'http://www.imdb.com/title/tt0042114/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0085033/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0058816/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0050032/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0071005/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0273366/?ref_=fn_al_tt_1',
'http://www.imdb.com/title/tt0058824/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0050037/?ref_=nv_sr_3',
'http://www.imdb.com/title/tt0096657/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0074028/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0056775/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0175058/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0106064/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0370194/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0101188/?ref_=fn_al_tt_1',
'http://www.imdb.com/title/tt0072562/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0206512/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0072567/?ref_=nv_sr_2',
'http://www.imdb.com/title/tt0072560/?ref_=nv_sr_5',
'http://www.imdb.com/title/tt0098936/?ref_=nv_sr_1',
'http://www.imdb.com/title/tt0060037/?ref_=fn_al_tt_7',
'http://www.imdb.com/title/tt0058855/?ref_=nv_sr_2']
imdb_data = []

def get_imdb_value(soup, tag, fieldname):
    '''Grab a value from imdb HTML
    Takes a tag and class_ or itemprop
    '''
    obj = soup.find(tag, class_ = fieldname)
    if not obj:
        obj = soup.find(tag, itemprop = fieldname)
    if obj:
        return obj.text
    else:
        return None

def getimdbdata(url):

    # request html data and creat soup
    response = requests.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.text)

    # scrape imdb 'easy' fields

    title = get_imdb_value(soup, 'span', 'itemprop')

    raw_release = get_imdb_value(soup, 'span', 'nobr')
    start_year = int(raw_release[1:5])
    try:
        end_year = int(release[6:10])
    except:
        end_year = None

    raw_length = get_imdb_value(soup, 'time', 'duration')
    try:
        length = int(raw_length.strip()[:2])
    except:
        length = None

    raw_rating = get_imdb_value(soup, 'div', 'titlePageSprite star-box-giga-star')
    rating = float(raw_rating)

    # get genres

    genre1 = soup.find_all('span', itemprop= 'genre')[0].text
    try:
        genre2 = soup.find_all('span', itemprop= 'genre')[1].text
    except IndexError:
        genre2 = None
    try:
        genre3 = soup.find_all('span', itemprop= 'genre')[2].text
    except IndexError:
        genre3 = None

    # get awards

    try:
        award_s1 = soup.find_all('span', itemprop= 'awards')[0].text
    except IndexError:
        award_s1 = '0'
    try:
        award_s2 = soup.find_all('span', itemprop= 'awards')[1].text
    except IndexError:
        award_s2 = '0'
    award_list = [int(s) for s in (award_s1.split() + award_s2.split()) if s.isdigit()]
    awards = sum(award_list)

    headers = ['showtitle', 'startyear' ,'endyear', 
               'episodelength', 'rating', 'genre1', 
               'genre2', 'genre3', 'awards']

    show_dict = dict(zip(headers, [title,
                                   start_year,
                                   end_year,
                                   length,
                                   rating,
                                   genre1,
                                   genre2,
                                   genre3,
                                   awards]))

    imdb_data.append(show_dict)

def scrape_imdb(url_list):
    for url in url_list:
        getimdbdata(url)

scrape_imdb(url_list)
pprint(imdb_data)

with open('imdb.pkl', 'w') as picklefile:
    pickle.dump(imdb_data, picklefile)