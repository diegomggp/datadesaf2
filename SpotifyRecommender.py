from flask import Flask, request, jsonify
from MetricAnalyzer import MetricAnalyzer

app = Flask(__name__)

# Default entrypoint
@app.route('/', methods=['GET'])
def home():
    return """
    <h1>APP for recommending songs</h1>    
    """


@app.route('/api/v1/metrics', methods=['POST'])
def metrics():
    '''
    API call  to predict the metrics for next Spotify songs with the provided JSON about other songs metrics

    Args:
        json (JSON): JSON data with the songs metrics

    Returns:
        Dictionary: A dictionary with the metrics to use for retrieving information from Spotify
    '''
    try:
        
        if request.is_json:
            data = request.get_json()      
            analyzer = MetricAnalyzer('metric_analyzer')
            metrics = analyzer.fx__get_metrics(data)
            # print(metrics)
            json_result =  jsonify(metrics)
        else:
            json_result = jsonify({"message": "El contenido de la petición no es un JSON"}), 400
    except Exception as ex:
        json_result = jsonify({"message": str(ex)}), 400
    finally:
        return json_result
    




if __name__ == '__main__':
    app.run(debug = True, port=5000)