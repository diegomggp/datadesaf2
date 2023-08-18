from flask import Flask, request, jsonify
from MetricAnalyzer import MetricAnalyzer as metric_analyzer
from SimilarityAnalyzer import SimilarityAnalyzer as similarity_analyzer

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug = True, port=5000)