import os
import json
from flask import Flask, request, jsonify
from Metrics.MetricAnalyzer import MetricAnalyzer as metric_analyzer
from Metrics.SimilarityAnalyzer import SimilarityAnalyzer as similarity_analyzer
from Artist.ArtistAnalyzer import ArtistAnalyzer as artist_analyzer
from NeuralNetwork.NeuralNetwork import NeuralNetwork as neural_network

from keras.models import Sequential
from keras.layers import Dense
# from keras.wrappers.scikit_learn import KerasClassifier
from scikeras.wrappers import KerasClassifier
from sklearn.datasets import make_classification



# New Flask Instance
app = Flask(__name__, static_folder='static')

# Define a folder for uploading files
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Default entrypoint
@app.route('/', methods=['GET'])
def home():
    return """
    <h1>APP for recommending songs</h1>    
    """


@app.route('/api/v1/metrics', methods=['POST'])
def fx__api_metrics():
    '''
    API call  to predict the metrics for next Spotify songs with the provided JSON about other songs metrics

    Args:
        json (JSON): JSON data with the songs metrics

    Returns:
        JSON: A JSON with the metrics to use for retrieving information from Spotify
    '''
    try:
        
        if request.is_json:
            data = request.get_json()      
            analyzer = metric_analyzer('metric_analyzer')
            metrics = analyzer.fx__get_metrics(data)
            # print(metrics)
            json_result =  jsonify(metrics)
        else:
            json_result = jsonify({"message": "El contenido de la petición no es un JSON"}), 400
    except Exception as ex:
        json_result = jsonify({"message": str(ex)}), 500
    finally:
        return json_result, 200
    


@app.route('/api/v1/similarity', methods=['POST'])
def fx__api_similarity():
    '''
    API call to select the 5 similariest songs in your own playlist using a JSON as input

    Args:
        json (JSON): JSON data with the songs metrics

    Returns:
        JSON: JSON with metrics and IDs of your 5 similariest songs in your own playlist
    '''
    try:
        
        if request.is_json:
            data = request.get_json()      
            analyzer = similarity_analyzer('similarity_analyzer')
            json_result = analyzer.fx__get_next_song_metrics(data)
        else:
            json_result = jsonify({"message": "El contenido de la petición no es un JSON"}), 400
    except Exception as ex:
        json_result = jsonify({"message": str(ex)}), 500
    finally:
        return json_result, 200



@app.route('/api/v1/favourite_artists', methods=['POST'])
def fx__api_favourite_artists():
    '''
    API call to select the top 20 artists from users playlist

    Args:
        json (JSON): JSON data with the songs in a playlist

    Returns:
        JSON: JSON with the information about top 20 artists
    '''
    try:
        
        if request.is_json:
            data = request.get_json()      
            analyzer = artist_analyzer('artist_analyzer')
            json_result = analyzer.fx__get_favourite_artists(data)
        else:
            json_result = jsonify({"message": "El contenido de la petición no es un JSON"}), 400
    except Exception as ex:
        json_result = jsonify({"message": str(ex)}), 500
    finally:
        return json_result, 200




# It predicts the sales based in 3 parameters. If model is not created yet it will.
@app.route('/api/v1/predict_mood', methods=['POST'])
def predict():
    '''
    API call to retrain the neural network model with new data
    Args:
        json (JSON): JSON data with the songs metrics and mood labelled
    Returns:
        JSON: Model accuracy result
    '''
    try:
        
        if request.is_json:
            data = request.get_json()      
            nn = neural_network()
            json_result = nn.fx__predict(data)
        else:
            json_result = jsonify({"message": "El contenido de la petición no es un JSON"}), 400

    except Exception as ex:
        json_result = jsonify({"message": str(ex)}), 500
    finally:
        return json_result, 200
    

    



@app.route('/api/v1/retrain_mood', methods=['POST'])
def fx__api__retrain():    
    '''
    API call to retrain the neural network model with new data
    Args:
        json (JSON): JSON data with the songs metrics and mood labelled
    Returns:
        JSON: Model accuracy result
    '''
    try:
        
        if request.is_json:
            data = request.get_json()      
            nn = neural_network()
            json_result = nn.fx__train(data)
        else:
            json_result = jsonify({"message": "El contenido de la petición no es un JSON"}), 400

    except Exception as ex:
        json_result = jsonify({"message": str(ex)}), 500
    finally:
        return json_result, 200
    

@app.route('/api/v1/default_train_mood', methods=['GET'])
def fx__api__default_train():
    '''
    API call to retrain the neural network model with the default data
    Args:
        json (JSON): JSON data with the songs metrics and mood labelled
    Returns:
        JSON: Model accuracy result
    '''
    
    try:
        
        # estimator = KerasClassifier(model=model, epochs=100, batch_size=5, verbose=0)
        # X, y = make_classification()
        # estimator.fit(X, y)

        # # This is what you need
        # # estimator.model.summary()
        # estimator.model_.summary()

        # default trainning JSON path
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'playlist_metrics.json')
        # load JSON file
        data = json.load(open(filename))
        
        # train neural network
        nn = neural_network()
        json_result = nn.fx__train(data)

    except Exception as ex:
        print(ex)
        json_result = jsonify({"message": str(ex)}), 500
    finally:        
        return json_result, 200
    


if __name__ == '__main__':
    app.run(debug = False, port=5000)