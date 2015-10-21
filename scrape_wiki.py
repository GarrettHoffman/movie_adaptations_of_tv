import requests
from bs4 import BeautifulSoup
import re
import dateutil.parser
from pprint import pprint
import pickle

url_list = ['https://en.wikipedia.org/wiki/Charlie%27s_Angels',
'https://en.wikipedia.org/wiki/21_Jump_Street',
'https://en.wikipedia.org/wiki/The_Addams_Family_(1964_TV_series)',
'https://en.wikipedia.org/wiki/Miami_Vice',
'https://en.wikipedia.org/wiki/Sex_and_the_City',
'https://en.wikipedia.org/wiki/Mission:_Impossible',
'https://en.wikipedia.org/wiki/Star_Trek:_The_Original_Series',
'https://en.wikipedia.org/wiki/The_Smurfs_(TV_series)',
'https://en.wikipedia.org/wiki/Police_Squad!',
'https://en.wikipedia.org/wiki/The_Untouchables_(1959_TV_series)',
'https://en.wikipedia.org/wiki/The_Transformers_(TV_series)',
'https://en.wikipedia.org/wiki/Veronica_Mars',
'https://en.wikipedia.org/wiki/Mystery_Science_Theater_3000',
'https://en.wikipedia.org/wiki/Jackass_(TV_series)',
'https://en.wikipedia.org/wiki/The_Simpsons',
'https://en.wikipedia.org/wiki/The_Twilight_Zone_(1959_TV_series)',
'https://en.wikipedia.org/wiki/South_Park',
'https://en.wikipedia.org/wiki/The_A-Team',
'https://en.wikipedia.org/wiki/The_Fugitive_(TV_series)',
'https://en.wikipedia.org/wiki/Firefly_(TV_series)',
'https://en.wikipedia.org/wiki/The_X-Files',
'https://en.wikipedia.org/wiki/All_That',
'https://en.wikipedia.org/wiki/Da_Ali_G_Show',
'https://en.wikipedia.org/wiki/Alvin_and_the_Chipmunks_(1983_TV_series)',
'https://en.wikipedia.org/wiki/Beavis_and_Butt-head',
'https://en.wikipedia.org/wiki/The_Beverly_Hillbillies',
'https://en.wikipedia.org/wiki/Bewitched',
'https://en.wikipedia.org/wiki/The_Brady_Bunch',
'https://en.wikipedia.org/wiki/Doug',
'https://en.wikipedia.org/wiki/The_Dukes_of_Hazzard',
'https://en.wikipedia.org/wiki/Entourage_(TV_series)',
'https://en.wikipedia.org/wiki/The_Equalizer',
'https://en.wikipedia.org/wiki/The_Flintstones',
'https://en.wikipedia.org/wiki/Garfield_and_Friends',
'https://en.wikipedia.org/wiki/George_of_the_Jungle',
'https://en.wikipedia.org/wiki/Get_Smart',
'https://en.wikipedia.org/wiki/G.I._Joe:_A_Real_American_Hero_(1985_TV_series)',
'https://en.wikipedia.org/wiki/Hannah_Montana',
'https://en.wikipedia.org/wiki/He-Man_and_the_Masters_of_the_Universe',
'https://en.wikipedia.org/wiki/Herbie,_the_Love_Bug',
'https://en.wikipedia.org/wiki/The_Honeymooners',
'https://en.wikipedia.org/wiki/Inspector_Gadget',
'https://en.wikipedia.org/wiki/I_Spy_(1965_TV_series)',
'https://en.wikipedia.org/wiki/Leave_It_to_Beaver',
'https://en.wikipedia.org/wiki/Land_of_the_Lost_(1974_TV_series)',
'https://en.wikipedia.org/wiki/Lizzie_McGuire',
'https://en.wikipedia.org/wiki/Lost_in_Space',
'https://en.wikipedia.org/wiki/Maverick_(TV_series)',
'https://en.wikipedia.org/wiki/Mr._Bean',
'https://en.wikipedia.org/wiki/The_Muppet_Show',
'https://en.wikipedia.org/wiki/My_Favorite_Martian',
'https://en.wikipedia.org/wiki/The_Powerpuff_Girls',
'https://en.wikipedia.org/wiki/Mighty_Morphin_Power_Rangers',
'https://en.wikipedia.org/wiki/Reno_911!',
'https://en.wikipedia.org/wiki/Rugrats',
'https://en.wikipedia.org/wiki/Saturday_Night_Live',
'https://en.wikipedia.org/wiki/SpongeBob_SquarePants',
'https://en.wikipedia.org/wiki/Starsky_%26_Hutch',
'https://en.wikipedia.org/wiki/S.W.A.T._(TV_series)',
'https://en.wikipedia.org/wiki/Twin_Peaks',
'https://en.wikipedia.org/wiki/Underdog_(TV_series)',
'https://en.wikipedia.org/wiki/The_Wild_Wild_West']
wiki_data = []

def get_wiki_value(soup, fieldname):
    '''Grab a value from wikipedia and finds
    next element.
    '''
    obj = soup.find(text=re.compile(fieldname))
    if not obj:
        return None
    next_next_element = obj.next_element.next_element
    if next_next_element:
        return next_next_element.text
    else:
        return None

def getwikidata(url):

    # request html data and creat soup
    response = requests.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.text)

    #get title
    title = soup.find('h1', class_='firstHeading').text

    #get next_next_element data
    raw_seasons = get_wiki_value(soup, 'of seasons')
    try:
        seasons = int(raw_seasons)
    except:
        seasons = None

    raw_episodes = get_wiki_value(soup, 'of episodes')
    try:
        episodes = int(raw_episodes[0:raw_episodes.find(' ')])
    except:
        episodes = None

    raw_length = get_wiki_value(soup, 'Running time')
    try:
        length = int(raw_length[0:2])
    except:
        length = None

    raw_network = get_wiki_value(soup, 'Original channel')
    if raw_network.find(' ') > 0:
        try:
            network = raw_network[0:raw_network.find(' ')]
        except:
            network = None
    else:
        network = raw_network

    headers = ['title', 'seasons' ,'episodes', 
               'showlength', 'network']

    wiki_dict = dict(zip(headers, [title,
                                    seasons,
                                    episodes,
                                    length,
                                    network]))

    wiki_data.append(wiki_dict)

def scrape_wiki(url_list):
    for url in url_list:
        getwikidata(url)

scrape_wiki(url_list)
pprint(wiki_data)

with open('wiki.pkl', 'w') as picklefile:
    pickle.dump(wiki_data, picklefile)