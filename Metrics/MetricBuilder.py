import pandas as pd
import datetime as dt

class MetricBuilder:

    def __init__(self):
        pass

    def fx__read_metrics(self, json):
        '''
        It read the data from JSON and it parses into a Pandas DataFrame

        Args:
            json (JSON): JSON data with the songs metrics

        Returns:
            DataFrame: A Pandas DataFrame of the parsed JSON
        '''

        try:
            # create a new DataFrame with the fields we expected
            df = pd.DataFrame(
                columns=['ts', 
                         'id',
                        'danceability',
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
                        'duration_ms',
                        'time_signature'])
            
            # iterate over json items for parsing data
            for item in json:        
                # build the row for dataframe
                row = {                    
                    'ts':dt.datetime.strptime(item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                    'id':item['id'],
                    'danceability':item['danceability'],
                    'energy':item['energy'],
                    'key':item['key'],
                    'loudness':item['loudness'],
                    'mode':item['mode'],
                    'speechiness':item['speechiness'],
                    'acousticness':item['acousticness'],
                    'instrumentalness':item['instrumentalness'],
                    'liveness':item['liveness'],
                    'valence':item['valence'],
                    'tempo':item['tempo'],
                    'duration_ms':item['duration_ms'],
                    'time_signature':item['time_signature']
                    }       
                
                # insert into dataframe
                df.loc[len(df)] = row
            
            # set timestamp properly at the end
            df['ts'] = pd.to_datetime(df['ts'], format='%Y-%m-%d &H:%M:%S')            
            df= df.sort_values('ts', ascending=False)
            
        except Exception as ex:
            print(ex)                     
            df= pd.DataFrame()
        finally:
                return df