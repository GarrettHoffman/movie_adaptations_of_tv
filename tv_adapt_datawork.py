import pickle
from pprint import pprint

## import data and check for reasonability
with open("bomojo.pkl", 'r') as picklefile: 
    bomojo_data = pickle.load(picklefile)
pprint(bomojo_data)

with open("imdb.pkl", 'r') as picklefile: 
    imdb_data = pickle.load(picklefile)
pprint(imdb_data)

with open("wiki.pkl", 'r') as picklefile:
    wiki_data = pickle.load(picklefile)
pprint(wiki_data)

print len(bomojo_data), len(imdb_data), len(wiki_data)

bomojo_df = pd.DataFrame.from_dict(bomojo_data)
imdb_df = pd.DataFrame.from_dict(imdb_data)
wiki_df = pd.DataFrame.from_dict(wiki_data)

## define animated indicator based on TV show genre
imdb_df['animated'] = 0
imdb_df['animated'][(imdb_df['genre1'] == 'Animation')] = 1
imdb_df['animated'][(imdb_df['genre2'] == 'Animation')] = 1
imdb_df['animated'][(imdb_df['genre3'] == 'Animation')] = 1

## reduce network feature to major networks and other
wiki_df['tvnetwork'] = 'temp'
wiki_df['tvnetwork'][wiki_df['network'].str.contains('NBC')] = 'NBC'
wiki_df['tvnetwork'][wiki_df['network'].str.contains('ABC')] = 'ABC'
wiki_df['tvnetwork'][wiki_df['network'].str.contains('CBS')] = 'CBS'
wiki_df['tvnetwork'][wiki_df['network'].str.contains('FOX')] = 'FOX'
wiki_df['tvnetwork'][wiki_df['network'].str.contains('Fox')] = 'FOX'
wiki_df['tvnetwork'][wiki_df['network'].str.contains('HBO')] = 'HBO'
wiki_df['tvnetwork'][wiki_df['tvnetwork'].str.contains('temp')] = 'Other'

## add key to merge on and merge into on data frame
bomojo_df['key'] = range(62)
imdb_df['key'] = range(62)
wiki_df['key'] = range(62)
df = pd.merge(bomojo_df, imdb_df, on = 'key')
df = pd.merge(df, wiki_df, on = 'key')

## define "distance", length of time between tv show premier and movie release
df['distance'] = df['releaseyear'] - df['startyear']

## create data frame containing model data only
modeldf = pd.concat([df['title'], 
                     df['domesticgross'], 
                     df['rating'], 
                     df['distance'], 
                     df['tvnetwork'], 
                     df['animated'],
                     df['awards']], axis = 1)

## pickle data 
with open('modeldata.pkl', 'w') as picklefile:
    pickle.dump(modeldf, picklefile)