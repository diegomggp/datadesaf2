import pandas as pd
import numpy as np

class TrainDataSetPreparer:

    def __init__(self):
        self.m_dic_categories={}

        
    def fx__trainer_data_preparer(self, df):

        '''
        It prepares the trainning dataset for deep learning model
        Args:
            Pandas DataFrame: metrics and mood tag for each song for trainning model
        Returns:
            Pandas DataFrame: prepared dataframe with proper parameters for deep learning algorithm
        '''
        
        #remove null values
        df.dropna(inplace=True)

        df =  self.__fx__prepare_tempo(df)
        df =  self.__fx__prepare_duration(df)
        df =  self.__fx__prepare_for_neural_network(df)
        
        return df

    def fx__get_available_moods(self, df):
        '''
        It retrieves the distinct available moods in the dataframe
        Args:
            Pandas DataFrame: metrics and mood tag for each song for trainning model
        Returns:
            List: list with the available moods
        '''
        return df['tag'].unique().tolist()


    def __fx__prepare_tempo(self, df):
        '''
        It handles tempo data and categorizes them
        Args:
            Pandas DataFrame: metrics and mood tag for each song for trainning model
        Returns:
            Pandas DataFrame: dataframe with tempo categorized
        '''
        try:
            #tempo
            df['tempo'] = pd.to_numeric(df['tempo'], errors='coerce')            
            df.loc[(df['tempo'] >= 0) & (df['tempo'] <= 60), 'speed'] = 1
            df.loc[(df['tempo'] > 60) & (df['tempo'] <= 90), 'speed'] = 2
            df.loc[(df['tempo'] > 90) & (df['tempo'] <= 120), 'speed'] = 3
            df.loc[(df['tempo'] > 120) & (df['tempo'] <= 150), 'speed'] = 4
            df.loc[(df['tempo'] > 150), 'speed'] = 5
            df['tempo'].astype('str')
        except Exception as ex:
            print(ex)
            df=pd.DataFrame()
        finally:
            return df


    def __fx__prepare_duration(self, df):
        '''
        It handles duration data and categorizes them
        Args:
            Pandas DataFrame: metrics and mood tag for each song for trainning model
        Returns:
            Pandas DataFrame: dataframe with duration categorized
        '''
        #duracion
        
        df['duration_ms'] = pd.to_numeric(df['duration_ms'], errors='coerce')        
        df['duration_minutes'] = round(df['duration_ms']/(1000 * 60),1)
        df.loc[(df['duration_minutes'] >= 0) & (df['duration_minutes'] <= 2), 'duration'] = 1
        df.loc[(df['duration_minutes'] > 2) & (df['duration_minutes'] <= 4), 'duration'] = 2
        df.loc[(df['duration_minutes'] > 4) & (df['duration_minutes'] <= 6), 'duration'] = 3
        df.loc[(df['duration_minutes'] > 6) , 'duration'] = 4
        df['duration_minutes'].astype('str')
        return df


    def __fx__prepare_for_neural_network(self, df):
        '''
        It prepares the Pandas Dataframe for Deep Learning algorithm
        Args:
            Pandas DataFrame: metrics and mood tag for each song for trainning model
        Returns:
            Pandas DataFrame: format dataframe for trainning model
        '''
        try:
            # remove some columns
            df.drop(columns=[
                'type',
                'analysis_url',
                'track_href',
                'error.status', 
                'error.message', 
                'ts', 
                'uri',
                'tick', 
                'playlist', 
                'id',
                'key', 
                'time_signature', 
                'duration_ms', 
                'duration_minutes',
                'tempo',
                'speechiness',
                'mode']
            , inplace=True)
            
            df = df.dropna()
            
        except Exception as ex:
            print(ex)
            return ex
        finally:            
            return df
        
    def fx__target_encoding(self, df):
        '''
        It prepares the Pandas Dataframe for Deep Learning algorithm
        Args:
            Pandas DataFrame: metrics and mood tag for each song for trainning model
        Returns:
            Pandas DataFrame: format dataframe for trainning model
        '''
        try:
            if len(self.m_dic_categories) != len(df['tag'].unique().tolist()):
                self.m_dic_categories = {}
                labels = df['tag'].unique().tolist()
                i = 0
                for label in labels:
                    self.m_dic_categories[label]= i
                    self.m_dic_categories[i]= label
                    i = i + 1
            
        except Exception as ex:
            print(ex)
            return ex
        finally:            
            return self.m_dic_categories
        
    def fx__prepare_target_encoding(self, df):
        '''
        It prepares the target labels of Pandas Dataframe for Deep Learning algorithm
        Args:
            Pandas DataFrame: metrics and mood tag for each song for trainning model
        Returns:
            Pandas DataFrame: tag encoded dataframe
        '''
        try:
            df['tag_label'] = df['tag'].map(self.fx__target_encoding(df))
            df['tag'] = df['tag_label']
            df = df.drop(columns='tag_label')
        except Exception as ex:
            print(ex)
            return ex
        finally:            
            return df