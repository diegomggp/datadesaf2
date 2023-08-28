# SpotifyRecommender
The goal of this API is to be able to recommend Spotify songs to the user that are related to the last songs they are listening to or according to their mood. To do this, based on a series of information formatted appropriately as input data, metrics are calculated with which requests can be made to the Spotify API to obtain the list of songs that best fit.

## API Calls

- `/api/v1/metrics` [POST]
- `/api/v1/similarity` [POST]
- `/api/v1/favourite_artists` [POST]
- `/api/v1/predict_mood` [POST]
- `/api/v1/retrain_mood` [POST]
- `/api/v1/default_train_mood` [GET]

### Trendy Metrics
A partir de las métricas de una serie de canciones como datos de entrada se calcula la tendencia para cada una de ellas y se devuelve un JSON con las que más se ajustan.
- `/api/v1/metrics` [POST]
- Input example:
![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/4798910c-2b81-4c0e-9d0a-a9618cd67da8)
