import pandas as pd

class TrainDataSetBuilder:

    def __init__(self):
        pass

    def fx__read_train_info(self, json):
        '''
        It read the data from JSON and it parses into a Pandas DataFrame

        Args:
            json (JSON): JSON data with the songs metrics and labels

        Returns:
            DataFrame: A Pandas DataFrame of the parsed JSON
        '''

        try:
            # create a new DataFrame with the fields we expected
            df = pd.DataFrame(
                columns=['danceability', 
                         'energy', 
                         'key', 
                         'loudness', 
                         'mode', 
                         'speechiness',
                         'acousticness', 
                         'instrumentalness', 
                         'liveness', 
                         'valence', 
                         'tempo',
                         'type', 
                         'id', 
                         'uri', 
                         'track_href', 
                         'analysis_url', 
                         'duration_ms',
                         'time_signature', 
                         'ts', 
                         'tick', 
                         'tag', 
                         'playlist', 
                         'error.status',
                         'error.message'
                         ])
            
            # iterate over json items for parsing data
            for item in json:        
                # build the row for dataframe
                row = {                    
                        'danceability' :(item['danceability']), 
                        'energy':(item['energy']), 
                        'key':(item['key']), 
                        'loudness': (item['loudness']), 
                        'mode':(item['mode']), 
                        'speechiness':( item['speechiness']), 
                        'acousticness': (item['acousticness']), 
                        'instrumentalness': (item['instrumentalness']), 
                        'liveness':( item['liveness']), 
                        'valence': (item['valence']), 
                        'tempo': (item['tempo']), 
                        'type': item['type'], 
                        'id': item['id'], 
                        'uri': item['uri'], 
                        'track_href': item['track_href'], 
                        'analysis_url': item['analysis_url'], 
                        'duration_ms': (item['duration_ms']), 
                        'time_signature': (item['time_signature']), 
                        'ts':item['ts'], 
                        'tick': item['tick'], 
                        'tag': item['tag'], 
                        'playlist': item['playlist'], 
                        'error.status': item['error.status'], 
                        'error.message': item['error.message']
                    }       
                
                # insert into dataframe
                df.loc[len(df)] = row
                df.dropna(inplace=True)
            
        except Exception as ex:
            print(ex)                     
            df= pd.DataFrame()
        finally:
                return df