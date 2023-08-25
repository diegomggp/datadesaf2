import pandas as pd

class ArtistBuilder:

    def __init__(self):
        pass

    def fx__read_artist_info(self, json):
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
                columns=['track_id', 
                         'href',
                        'artist_id',
                        'artist_name'])
            
            # iterate over json items for parsing data
            for item in json:        
                # build the row for dataframe
                row = {                    
                    'track_id':item['track_id'],
                    'href':item['href'],
                    'artist_id':item['artist_id'],
                    'artist_name':item['artist_name']                    
                    }       
                
                # insert into dataframe
                df.loc[len(df)] = row
                       
            
        except Exception as ex:
            print(ex)                     
            df= pd.DataFrame()
        finally:
                return df