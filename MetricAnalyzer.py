from prophet import Prophet
import pandas as pd
import datetime as dt

class MetricAnalyzer:
    '''
    ## Spotify Metrics:
    - Acousticness: A confidence measure from 0 to 1 of whether the track is acoustic. 1 represents high confidence the track is acoustic.
    - Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements. A value of 0 is least danceable and 1 is most danceable.
    - Duration: The duration of the track in milliseconds.
    - Energy: Energy is a measure from 0 to 1 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.
    - Instrumentalness: Predicts whether a track contains no vocals. The closer the instrumentalness value is to 1, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.
    - Key: The estimated overall key of the track. (-1 if no key is detected)
    - Liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
    - Loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Values typical range between -60 and 0 db.
    - Mode: Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
    - Speechiness: Speechiness detects the presence of spoken words in a track. Talk shows and audio books are closer to 1, songs made entirely of spoken words are above 0.66, songs that contain both music and speech are typically around 0.33 - 0.66 and values below 0.33 represent music and other non-speech-like tracks.
    - Tempo: The overall estimated tempo of a track in beats per minute (BPM).
    - Time Signature: An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).
    - Valence: A measure from 0 to 1 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive, while tracks with low valence sound more negative.
    '''

    def __init__(self, id):
        self.id = id
        
    
    def fx__get_metrics(self,json):
        '''
        The main function to predict the metrics for next Spotify songs

        Args:
            json (JSON): JSON data with the songs metrics

        Returns:
            Dictionary: A dictionary with the metrics to use for retrieving information from Spotify
        '''

        try:
            df = self.fx__read_metrics(json)
            if not df.empty:
                predictions = self.fx__predict(df)
                predictions = self.fx__handle_predictions(predictions)            

        except Exception as ex:
            return {'Error':str(ex)}
        finally:
            return predictions
    

    
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
                columns=['song', 
                        'ts', 
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
                    'song':item['item'], 
                    'ts':dt.datetime.strptime(item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                    'danceability':item['metrics']['danceability'],
                    'energy':item['metrics']['energy'],
                    'key':item['metrics']['key'],
                    'loudness':item['metrics']['loudness'],
                    'mode':item['metrics']['mode'],
                    'speechiness':item['metrics']['speechiness'],
                    'acousticness':item['metrics']['acousticness'],
                    'instrumentalness':item['metrics']['instrumentalness'],
                    'liveness':item['metrics']['liveness'],
                    'valence':item['metrics']['valence'],
                    'tempo':item['metrics']['tempo'],
                    'duration_ms':item['metrics']['duration_ms'],
                    'time_signature':item['metrics']['time_signature']
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
        
    
    def fx__predict(self, df):
        '''
        It predicts the next metrics based on inmediate previous metrics with Facebook Prophet

        Args:
            df (Pandas DataFrame): Songs metrics data

        Returns:
            Dictionary: Predicted metrics
        '''

        try:
            prediction = {}
            for col in ['danceability','energy','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']:
                # set data for prediction
                data = df[['ts',col]]
                data = data.rename(columns={'ts':'ds',col:'y' })

                # setup the model
                model = Prophet()
                model.fit(data)
                
                # do predictions
                future = model.make_future_dataframe(periods=10, freq='1min')
                # predictions
                forecast = model.predict(future)
                # trend data
                trend = forecast['trend']

                # predictions to return
                prediction[col] = forecast.loc[forecast.index[-1], 'trend']

        except Exception as ex:
            prediction = {}
        finally:
            return prediction
        

    def fx__manage_limits(self, key, value, min_value, max_value):        
        '''
        It handle values if exceeds or lacks the maximum or minimun value           
        Args:
            df (Pandas DataFrame): Songs metrics data
            key (string): original dictionary key
            value (float): original dictionary value
            min_value (float): allowed minimum value for original dictionary value
            max_value (float): allowed maximum value for original dictionary value
        Returns:
            Dictionary: Predicted metrics
        '''

        if value < min_value:
            value = min_value
        elif value > max_value:
            value = max_value
        
        return {key:value}
    
    def fx__handle_predictions(self, prediction):
        '''
        It handle the limits for the predictions
        Args:
            prediction (dictionary): predicted song metrics
        Returns:
            Dictionary: Adjusted predicted metrics
        '''
        managed_prediction ={}

        for key, value in prediction.items():
            
            if key in ['acousticness','danceability','energy','instrumentalness', 'valence','liveness','mode', 'speechiness']:
                managed_key_value = self.fx__manage_limits(key, value, 0, 1)
            
            if key in ['loudness']:
                managed_key_value = self.fx__manage_limits(key, value, -60, 0)
            
            if key in ['tempo']:
                managed_key_value = self.fx__manage_limits(key, value, 0, 200)       

            if key in ['duration_ms']:
                managed_key_value = self.fx__manage_limits(key, value, 0, 1000 * 60 * 60 * 3) # 3 horas

            managed_prediction = {**managed_prediction, **managed_key_value}

        return managed_prediction

