from src import main
from unittest.mock import patch, ANY, MagicMock
import json

@patch("wetter.OpenWeatherMapAPI")
def test_onMQTTconnect(mock_wetter):

    mock_client = MagicMock()

    main.on_connect(mock_client,None,None,None)

    mock_client.subscribe.assert_called_with([('req/weather/now', 0), ('req/weather/<Datum>/<Uhrzeit>', 0), ('location/current', 0)])
    
    
@patch("wetter.OpenWeatherMapAPI")
def test_on_message(mock_wetter):

    main.on_message(MagicMock(),None,message_for_testing())
    assert True

class message_for_testing:
    topic = "topic"
    payload = "payload"
    

@patch("wetter.OpenWeatherMapAPI")
def test_specific_callback_location(mock_wetter):
    
    mock_client = MagicMock()
    msg = message_for_testing()
    msg.topic = "location/current"

    main.specific_callback(mock_client, None, msg)
    assert main.location == msg.payload
    #mock_client.subscribe.assert_called_with("weather/now", mock_wetter)

@patch("wetter.OpenWeatherMapAPI")
def test_specific_callback_weather_now(mock_wetter):
    
    mock_client = MagicMock()
    msg = message_for_testing()
    msg.topic = "req/weather/now"
    
    main.weather_api = MagicMock()
    main.location = MagicMock()

    main.specific_callback(mock_client, None, msg)
    #assert main.location == msg.payload
    main.weather_api.get_current_weather_with_gps.assert_called_with(main.location.lat, main.location.lon)

@patch("wetter.OpenWeatherMapAPI")
def test_specific_callback_weather_date(mock_wetter):
    
    mock_client = MagicMock()
    msg = message_for_testing()
    msg.topic = "req/weather/<Datum>/<Uhrzeit>"
    msg.payload = MagicMock()
    
    main.weather_api = MagicMock()
    main.location = MagicMock()

    main.specific_callback(mock_client, None, msg)
    #assert main.location == msg.payload
    main.weather_api.get_weather_by_date_with_gps.assert_called_with(main.location.lat, main.location.lon, msg.payload.date + " " + msg.payload.time)
