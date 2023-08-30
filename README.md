# SpotifyRecommender
The goal of this API is to be able to recommend Spotify songs to the user that are related to the last songs they are listening to or according to their mood. To do this, based on a series of information formatted appropriately as input data, metrics are calculated with which requests can be made to the Spotify API to obtain the list of songs that best fit.

## Spotify Metrics:
- `Acousticness`: A confidence measure from 0 to 1 of whether the track is acoustic. 1 represents high confidence the track is acoustic.
- `Danceability`: Danceability describes how suitable a track is for dancing based on a combination of musical elements. A value of 0 is least danceable and 1 is most danceable.
- `Duration`: The duration of the track in milliseconds.
- `Energy`: Energy is a measure from 0 to 1 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.
- `Instrumentalness`: Predicts whether a track contains no vocals. The closer the instrumentalness value is to 1, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.
- `Key`: The estimated overall key of the track. (-1 if no key is detected)
- `Liveness`: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
- `Loudness`: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Values typical range between -60 and 0 db.
- `Mode`: Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
- `Speechiness`: Speechiness detects the presence of spoken words in a track. Talk shows and audio books are closer to 1, songs made entirely of spoken words are above 0.66, songs that contain both music and speech are typically around 0.33 - 0.66 and values below 0.33 represent music and other non-speech-like tracks.
- `Tempo`: The overall estimated tempo of a track in beats per minute (BPM).
- `Time Signature`: An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).
- `Valence`: A measure from 0 to 1 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive, while tracks with low valence sound more negative.
    
## API Calls

- `[POST]` `/api/v1/metrics`
- `[POST]` `/api/v1/similarity`
- `[POST]` `/api/v1/favourite_artists`
- `[POST]` `/api/v1/predict_mood`
- `[POST]` `/api/v1/retrain_mood`
- `[GET]` `/api/v1/default_train_mood`

### Trendy Metrics
From the metrics of a series of songs as input data, the trend is calculated for each one of them and a JSON is returned with the ones that fit best using `Facebook Prophet` predictions.
![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/3a25d289-776b-4d68-9f4a-f5201a00e396)

- `[POST]` `/api/v1/metrics`
- Input example (available file: `trendy_metrics_json`): JSON with songs' metrics

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/4798910c-2b81-4c0e-9d0a-a9618cd67da8)

- Output: JSON with calculated metrics

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/29d73acb-28c0-4854-be39-330bc26c577a)


### Similarity
Recommends songs from the same playlist based on the songs previously listened to from the same playlist. Uses a Nearest Neighbors algorithm to find the most similar songs to the ones that have been listened to from the playlist. 
- `[POST]` `/api/v1/similarity`
- Input example ( available file: `playlist_example_json.json`): JSON with playlist songs' metrics
 
![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/cc0d19e4-9f51-476c-9b71-224a18afb916)

- Output: JSON with selected songs' metrics and IDs

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/618f0df1-fb85-494b-97ff-b8427311b534)

  
### User's favourite artists
Gets the user's favorite artists.
- `[POST]` `/api/v1/favourite_artists`
- Input example ( available file: `playlist_artists.txt`): JSON with user's songs and artists. This file must be prepared gathering information from Spotify API.
 
![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/d65bb8a9-eca2-4c87-9855-216dbe7da0e1)


- Output: JSON with most common artists and song counter

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/e8418264-c161-47b8-9103-7d4bcdcbc423)


### Mood prediction
It will predict the user's mood based on a set of song metrics passed as input data (songs he/she has recently listened to, for example) using a TensowFlow Keras Neural Network trained with a dataset (`playlist_metrics.json`) containing the mood tags for each song. These labels are automatically saved in a file (`neural_model_labels.json`) so that they are available to both the user and the model. With each training of the model its information is also saved (`neural_model.keras`) so that it can be loaded and preconditioned. **Importan: accuracy in this model is quite low, so next steps will be to optimize the Neural Network**
- `[POST]` `/api/v1/predict_mood`
- Input example ( available file: `playlist_metrics.json`): JSON with songs' metrics and associated mood tag. Notice in the image that input JSON contains `tag`, but we won't use that for predicting.

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/04af4ea5-1c1c-45fd-95ca-d04fa6ace090)

- Output: String with the predicted mood

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/fe357bca-e989-4ca8-bcde-a1cee7fc126a)



### Neural Network Trainning
With a dataset in the same format as the default (`playlist_metrics.json`), it is possible to retrain the neural network to save the model and the new categories in order to make new predictions.
- `[POST]` `/api/v1/retrain_mood`
- Input example ( like available file: `playlist_metrics.json`): JSON with songs' metrics and associated mood tag.

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/04af4ea5-1c1c-45fd-95ca-d04fa6ace090)

- Output: String with accuracy and model status

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/febf085e-4199-4dc8-a030-2f8389e92465)


### Neural Network Default Trainning
In any case, we can retrain the neural network with the original data (`playlist_metrics.json`).
- `[GET]` `/api/v1/default_train_mood`
- Input example ( like available file: `playlist_metrics.json`): JSON with songs' metrics and associated mood tag.

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/04af4ea5-1c1c-45fd-95ca-d04fa6ace090)

- Output: String with accuracy and model status

![imagen](https://github.com/marcosmarinalopez/SpotifyRecommender/assets/12278720/febf085e-4199-4dc8-a030-2f8389e92465)

