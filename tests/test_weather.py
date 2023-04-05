from src import wetter
from unittest.mock import patch, ANY, mock_open

@patch("builtins.open")
@patch("os.path.exists")
@patch("requests.get")
def test_current_weather(mock_requests, mock_exists, mock_open):
    obj = wetter.OpenWeatherMapAPI()
    
    obj.get_current_weather_with_gps(3.0, 4.0)
    mock_requests.assert_called_with(f"https://api.openweathermap.org/data/2.5/weather?lat=3.0&lon=4.0&appid={mock_open().__enter__().readline().strip()}&units=metric")


@patch("builtins.open")
@patch("os.path.exists")
@patch("requests.get")
def test_get_weather_by_date_with_gps(mock_requests, mock_exists, mock_open):
    obj = wetter.OpenWeatherMapAPI()
    
    obj.get_weather_by_date_with_gps(3.0, 4.0, "2022-04-01 14:30:00")
    mock_requests.assert_called_with(f"https://api.openweathermap.org/data/2.5/forecast?lat=3.0&lon=4.0&appid={mock_open().__enter__().readline().strip()}&units=metric")


@patch('builtins.open', new_callable=mock_open, read_data='test')
@patch("os.path.exists")
def test_loadAPIKey(mock_exists,mock_open):
    obj = wetter.OpenWeatherMapAPI()

    string_read = obj.api_key
    assert string_read == "test"