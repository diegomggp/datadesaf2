import json
import os
from flask import jsonify
import pandas as pd
import numpy as np
from collections import Counter

# cross validation libraries
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV

#Libraries to create the Multi-class Neural Network
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils

from TrainDataSetPreparer import TrainDataSetPreparer as train_dataset_preparer
from TrainDataSetBuilder import TrainDataSetBuilder as train_dataset_builder

class NeuralNetwork:

    def __init__(self):
        self.number_of_moods = 0
        self.columns_in_df = 0
        self.m_c_train_dataset_preparer = train_dataset_preparer()
        self.m_c_train_dataset_builder = train_dataset_builder()
        


    def fx__train(self, json):
        '''
        It trains the Neural Network with new dataset
        and saves it into a file ready to be consumed
        Args:
            JSON: songs' metrics with mood labelled
        Returns:
            Model Accuracy (str): an string that shows the accuracy and standard deviation of the trained model
        '''
        isOk =True
        try:

            # parse the json into dataframe
            df = self.__fx__prepare_data(json)       
            df = self.m_c_train_dataset_preparer.fx__prepare_target_encoding(df)
            isOk = isOk & self.__fx__save_categories(df)

            if df.empty | isOk ==False:
                return "JSON issue. Can't train..."

            # predictors and variables
            y = df['tag']
            X = df.drop(columns='tag').apply(pd.to_numeric)

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

            self.number_of_moods = len(self.m_c_train_dataset_preparer.fx__get_available_moods(df))
            self.columns_in_df = len(X.columns)
            
            # Configure the estimator with 300 epochs and 200 batchs. the build_fn takes the function defined above.
            estimator = KerasClassifier(
                build_fn=self.__fx__create_base_model,
                input_dim =self.columns_in_df,
                units = self.number_of_moods,
                epochs=300,
                batch_size=200)
            
            # Debugging? -->
            # #Evaluate the model using KFold cross validation
            #kfold = KFold(n_splits=5, shuffle=True)
            # # Get the score
            #results = cross_val_score(estimator, X, y, cv=kfold)
            # <-- Debugging?

            # materialize the model            
            estimator.fit(X_train, y_train)
            accuracy = estimator.score(X_test, y_test) * 100

            keras.models.save_model(estimator.model,'./neural_model.keras', overwrite=True)
            # pickle.dump(model, open('neural_model.pkl','wb'))

            if os.path.exists('./neural_model.keras') == True:
                message = 'Model saved => '
            else:
                message = '/!\ Model NOT saved /!\ => '


        except Exception as ex:
            print(ex)
            return ex
        finally:
            # Debugging? -->
            # return (message + " Model Accuraccy: %.2f%% (Std. Dev. %.2f%%)" % (results.mean()*100,results.std()*100))
            # <-- Debugging?
            return (message + f"Accuracy: %.2f%% " % (accuracy))


    def __fx__create_base_model(self, input_dim, units):
        '''
        It creates the neural network model
        Args:
            input_dimension (int): number of available columns in trainning dataset
            num_moods (int): number of moods available in trainning dataset
        Returns:
            Model: Neural Network Base Model ready for trainning
        '''
        try:
            #Create the model
            model = Sequential()
            #Add 1 layer with 8 nodes,input of 4 dim with relu function
            model.add(Dense(units=units,input_dim=input_dim,activation='relu'))
            #Add another layer with 8 nodes,input of 4 dim with relu function
            model.add(Dense(units=units*2,input_dim=input_dim,activation='relu'))
            #Add 1 layer with output 3 and softmax function
            model.add(Dense(units,activation='softmax'))
            #Compile the model using logistic loss function and adam     optimizer, accuracy correspond to the metric displayed
            model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
        except Exception as ex:
            print(ex)
            return ex
        finally:
            return model


    def __fx__prepare_data(self, json):
        isOk = True
        try:
            # parse the json into dataframe
            df = self.m_c_train_dataset_builder.fx__read_train_info(json)

            # dataset preparation
            df = self.m_c_train_dataset_preparer.fx__trainer_data_preparer(df)
            
        except Exception as ex:
            print(ex)
            df = pd.DataFrame()
        finally:
            return df

    def __fx__save_categories(self, df):
        isOk = True
        try:
            categories = self.m_c_train_dataset_preparer.m_dic_categories
            with open('./neural_model_labels.json', "w") as json_file:
                json.dump(categories, json_file)

            isOk = os.path.exists('./neural_model_labels.json')
        except Exception as ex:
            print(ex)
            isOk=False
        finally:
            return isOk
        
            


    def __fx__get_categories(self):
        categories ={}
        try:
            if os.path.exists('./neural_model_labels.json'):
                with open('./neural_model_labels.json', "r") as json_file:
                    categories = json.load(json_file)
                
        except Exception as ex:
            print(ex)
        finally:
            return categories





    def fx__predict(self, json):
        '''
        It creates the neural network model
        Args:
            input_dimension (int): number of available columns in trainning dataset
            num_moods (int): number of moods available in trainning dataset
        Returns:
            Model: Neural Network Base Model ready for trainning
        '''

        try:

            # create the model if not created
            if os.path.exists('./neural_model.keras') == True:
                # get the model
                # model_advertising= pickle.load(open('neural_model.pkl', 'rb'))
                model = keras.models.load_model('./neural_model.keras')
                
                categories = self.__fx__get_categories()

                # parse the json into dataframe
                df = self.__fx__prepare_data(json)

                if df.empty:
                    return "JSON issue. Can't predict..."

                # predictors and variables
                X = df.drop(columns='tag').apply(pd.to_numeric)

                # predict
                prediction = model.predict(X)
                lst_moods=[]
                for single_prediction in prediction:
                    predicted_mood_number = np.argmax(single_prediction)
                    predicted_mood = categories[str(predicted_mood_number)]
                    lst_moods.append(predicted_mood)
                counter = Counter(lst_moods)
                probable_mood = counter.most_common(1)[0][0]

            else:
                probable_mood = "Error when training..."

        except Exception as ex:
            probable_mood = "Bad parameters given. " + str(ex)
            print(ex)
            return ex
        finally:
            return probable_mood

