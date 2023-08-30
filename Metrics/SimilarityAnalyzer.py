import pandas as pd
import datetime as dt
from Metrics.MetricBuilder import MetricBuilder as mb
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import json

class SimilarityAnalyzer:
    
    def __init__(self, id):
        self.id = id

    def fx__get_next_song_metrics(self, json):
        
        try:
            metric_builder = mb()
            df = metric_builder.fx__read_metrics(json)
            result = self.__fx__get_nearest_neighbors__(df)
        except Exception as ex:
            return {'Error':str(ex)}     
        return result
    
    def __fx__get_nearest_neighbors__(self, df):

        '''
        It returns the 5 similariest songs in the same playlist

        Args:
            json (JSON): Playlist songs metrics data

        Returns:
            Dictionary: 5 Similariest songs within playlist
        '''
        
        try:
            
            # ML notation
            X = df.drop(columns=['id', 'ts'])        

            # Split data.         
            X_test = X.head(5) # last 5 songs to search other similar songs
            X_train = X.tail(len(df) - 5) # remaining songs where we will search in

            # Scale parameters
            scl = StandardScaler()
            scl.fit(X_train)
            X_train_scl = scl.transform(X_train)
            X_train_scl = pd.DataFrame(X_train_scl, columns=X_train.columns)
            X_test_scl = scl.transform(X_test)
            X_test_scl = pd.DataFrame(X_test_scl, columns=X_train.columns)


            
            k = 1  # Number of neighbors
            model = NearestNeighbors(n_neighbors=k)
            # Train model
            model.fit(X_train_scl)
            # Find closest neighbors
            distances, indices = model.kneighbors(X_test_scl)
                    
            # For each neighbor, add to JSON 
            lst_similariest_songs = []
            for indice in indices:
                neighbors = df.iloc[indice[0]]            
                lst_similariest_songs.append(neighbors.to_dict())
            result = json.dumps(lst_similariest_songs, indent=4,default=str)
        
        except Exception as ex:
            return {'Error':str(ex)}    
            print(df.info())   

        return result
    
    