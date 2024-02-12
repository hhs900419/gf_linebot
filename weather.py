import requests

# Replace with your API key
API_KEY = "68IVLcGtC0DdWKbaaUQiT69lkI4YJHiF"

# # Base URL for the API
# base_url = "https://dataservice.accuweather.com/currentconditions/v1/"

# # Location key for San Francisco
# location_key = "349722"

# # API endpoint for current conditions
# endpoint = f"{location_key}?apikey={API_KEY}"

# # Make the API call
# response = requests.get(base_url + endpoint)

# # Check for successful response
# if response.status_code == 200:
#   # Parse JSON data
#   eather_data = response.json()[0]

#   # Extract relevant information
#   # city = weather_data["City"]["EnglishName"]
#   temperature = weather_data["Temperature"]["Imperial"]["Value"]
#   weather_text = weather_data["WeatherText"]

#   # Print or use the data in your reminder message
#   print(f"City: , Temperature: {temperature}°F, Weather: {weather_text}")
# else:
#   print("Error fetching weather data")


class WeatherAPI:
  def __init__(self):
      self.api_key
      self.location_key = None
        
  def get_location_by_geo(self, latitude, longitude):
    api_base_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
    api_endpoint = f"?apikey={self.api_key}"