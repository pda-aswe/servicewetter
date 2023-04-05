from src import main
from unittest.mock import patch, ANY, MagicMock
import json

@patch("wetter.OpenWeatherMapAPI")
def test_onMQTTconnect(mock_wetter):

    mock_client = MagicMock()

    main.on_connect(mock_client,None,None,None)

    mock_client.subscribe.assert_called_with([('req/weather/now', 0), ('req/weather/<Datum>/<Uhrzeit>', 0), ('location/current', 0)])
    
    
@patch("wetter.OpenWeatherMapAPI")
def test_onMQTTMessage(mock_wetter):

    main.on_message(MagicMock(),None,message_for_testing())
    assert True

class message_for_testing:
    topic = "topic"
    payload = "payload"
    

@patch("wetter.OpenWeatherMapAPI")
def test_specific_callback(mock_wetter):
    assert True
    # mock_client = MagicMock()
    # msg = message_for_testing()
    # msg.topic = "req/weather/now"

    # main.specific_callback(mock_client, None, msg)
    # mock_client.subscribe.assert_called_with("weather/now", mock_wetter)
