import requests
from bs4 import BeautifulSoup
import re
import dateutil.parser
from pprint import pprint
import pickle

url_list = ['http://www.boxofficemojo.com/movies/?id=charliesangels.htm',
'http://www.boxofficemojo.com/movies/?id=21jumpstreet.htm',
'http://www.boxofficemojo.com/movies/?id=addamsfamily.htm',
'http://www.boxofficemojo.com/movies/?id=miamivice.htm',
'http://www.boxofficemojo.com/movies/?id=sexandthecity.htm',
'http://www.boxofficemojo.com/movies/?id=missionimpossible.htm',
'http://www.boxofficemojo.com/movies/?id=startrek11.htm',
'http://www.boxofficemojo.com/movies/?id=smurfs.htm',
'http://www.boxofficemojo.com/movies/?id=nakedgun.htm',
'http://www.boxofficemojo.com/movies/?id=untouchables.htm',
'http://www.boxofficemojo.com/movies/?id=transformers06.htm',
'http://www.boxofficemojo.com/movies/?id=veronicamars.htm',
'http://www.boxofficemojo.com/movies/?id=mysterysciencetheater3000.htm',
'http://www.boxofficemojo.com/movies/?id=jackass.htm',
'http://www.boxofficemojo.com/movies/?id=simpsons.htm',
'http://www.boxofficemojo.com/movies/?id=twilightzone.htm',
'http://www.boxofficemojo.com/movies/?id=southpark.htm',
'http://www.boxofficemojo.com/movies/?id=ateam.htm',
'http://www.boxofficemojo.com/movies/?id=fugitive.htm',
'http://www.boxofficemojo.com/movies/?id=serenity.htm',
'http://www.boxofficemojo.com/movies/?id=x-filesfightthefuture.htm',
'http://www.boxofficemojo.com/movies/?id=goodburger.htm',
'http://www.boxofficemojo.com/movies/?id=borat.htm',
'http://www.boxofficemojo.com/movies/?id=alvinandthechipmunks.htm',
'http://www.boxofficemojo.com/movies/?id=beavisandbuttheaddoamerica.htm',
'http://www.boxofficemojo.com/movies/?id=beverlyhillbillies.htm',
'http://www.boxofficemojo.com/movies/?id=bewitched.htm',
'http://www.boxofficemojo.com/movies/?id=bradybunchmovie.htm',
'http://www.boxofficemojo.com/movies/?id=dougsfirstmovie.htm',
'http://www.boxofficemojo.com/movies/?id=dukesofhazzard.htm',
'http://www.boxofficemojo.com/movies/?id=entourage.htm',
'http://www.boxofficemojo.com/movies/?id=equalizer.htm',
'http://www.boxofficemojo.com/movies/?id=flintstones.htm',
'http://www.boxofficemojo.com/movies/?id=garfield.htm',
'http://www.boxofficemojo.com/movies/?id=georgeofthejungle.htm',
'http://www.boxofficemojo.com/movies/?id=getsmart.htm',
'http://www.boxofficemojo.com/movies/?id=gijoe.htm',
'http://www.boxofficemojo.com/movies/?id=hannahmontanamovie.htm',
'http://www.boxofficemojo.com/movies/?id=mastersoftheuniverse.htm',
'http://www.boxofficemojo.com/movies/?id=herbie05.htm',
'http://www.boxofficemojo.com/movies/?id=honeymooners.htm',
'http://www.boxofficemojo.com/movies/?id=inspectorgadget.htm',
'http://www.boxofficemojo.com/movies/?id=ispy.htm',
'http://www.boxofficemojo.com/movies/?id=leaveittobeaver.htm',
'http://www.boxofficemojo.com/movies/?id=landofthelost.htm',
'http://www.boxofficemojo.com/movies/?id=lizziemcguiremovie.htm',
'http://www.boxofficemojo.com/movies/?id=lostinspace.htm',
'http://www.boxofficemojo.com/movies/?id=maverick.htm',
'http://www.boxofficemojo.com/movies/?id=bean2.htm',
'http://www.boxofficemojo.com/movies/?id=muppetmovie.htm',
'http://www.boxofficemojo.com/movies/?id=myfavoritemartian.htm',
'http://www.boxofficemojo.com/movies/?id=powerpuffgirls.htm',
'http://www.boxofficemojo.com/movies/?id=powerrangers.htm',
'http://www.boxofficemojo.com/movies/?id=reno911.htm',
'http://www.boxofficemojo.com/movies/?id=rugratsmovie.htm',
'http://www.boxofficemojo.com/movies/?id=bluesbrothers.htm',
'http://www.boxofficemojo.com/movies/?id=spongebob.htm',
'http://www.boxofficemojo.com/movies/?id=starskyandhutch.htm',
'http://www.boxofficemojo.com/movies/?id=swat.htm',
'http://www.boxofficemojo.com/movies/?id=twinpeaksfirewalkwithme.htm',
'http://www.boxofficemojo.com/movies/?id=underdog.htm',
'http://www.boxofficemojo.com/movies/?id=wildwildwest.htm']
movie_data = []

def get_movie_value(soup, fieldname):
    '''Grab a value from boxofficemojo HTML
    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    '''
    obj = soup.find(text=re.compile(fieldname))
    if not obj:
        return None
    next_sibling = obj.findNextSibling()
    if next_sibling:
        return next_sibling.text
    else:
        return None

def money_to_int(moneystring):
    moneystring = moneystring.replace('$', '').replace(',', '')
    return int(moneystring)

def to_date(datestring):
    date = dateutil.parser.parse(datestring)
    return date

def runtime_to_minutes(runtimestring):
    runtime = runtimestring.split()
    try:
        minutes = int(runtime[0])*60 + int(runtime[2])
        return minutes
    except:
        return None

def getmojodata(url):

    # request html data and create soup
    response = requests.get(url + '&adjust_yr=2015&p=.htm')
    assert response.status_code == 200
    soup = BeautifulSoup(response.text)

    # scrape movie title and clean
    title = soup.find('title').text.split(' (')[0]

    # scrape mojo "sibling" fields
    raw_domestic_total = get_movie_value(soup, 'Domestic')
    domestic_total = money_to_int(raw_domestic_total)

    distributor = get_movie_value(soup, 'Distributor')

    raw_release_date = get_movie_value(soup, 'Release Date')
    release_date = to_date(raw_release_date)
    release_year = release_date.year

    genre = get_movie_value(soup, 'Genre:')

    raw_run_time = get_movie_value(soup, 'Runtime')
    run_time = runtime_to_minutes(raw_run_time)

    rating = get_movie_value(soup, 'Rating')

    raw_budget = get_movie_value(soup, 'Budget')
    try:
        budget = int(raw_budget[1:raw_budget.find(' ')]) * 1000000
    except:
        budget = None

    #scrape worldwide total
    try:
        raw_worldwide_total = soup.find(class_='mp_box_content').find_all('td')[8].text
        worldwide_total = money_to_int(raw_worldwide_total)

    except IndexError:
        worldwide_total = None

    headers = ['movietitle', 'worldgross' ,'domesticgross', 
               'distributor', 'releaseyear', 'genre', 
               'runtime', 'movierating', 'budget']

    movie_dict = dict(zip(headers, [title,
                                    worldwide_total,
                                    domestic_total,
                                    distributor,
                                    release_year,
                                    genre,
                                    run_time,
                                    rating,
                                    budget]))

    movie_data.append(movie_dict)

def scrape_mojo(url_list):
    for url in url_list:
        getmojodata(url)

scrape_mojo(url_list)
pprint(movie_data)

with open('bomojo.pkl', 'w') as picklefile:
    pickle.dump(movie_data, picklefile)