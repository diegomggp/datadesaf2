import json
import pandas as pd
from Artist.ArtistBuilder import ArtistBuilder as artist_builder

class ArtistAnalyzer:

    def __init__(self, id):
        self.id = id

    def fx__get_favourite_artists(self, json):
        '''
        It gets the most favourite artists based on how many songs have in the playlist

        Args:
            json (JSON): JSON data with the playlist song

        Returns:
            JSON: contains the 20 most favourite artists
        '''
        
        c_artist_builder = artist_builder()
        df = c_artist_builder.fx__read_artist_info(json)

        # which artists are the favourite ones
        # pay attention to .head(20) because this should be a parameter instead a number
        df_group = df.groupby(['artist_id','artist_name','href'])   \
            .count()                                                \
            .sort_values('track_id', ascending=False)               \
            .reset_index()                                          \
            .rename(columns={'track_id':'counter'})
       
        result = df_group.head(20).to_json(orient='records', indent=4)

        return result

