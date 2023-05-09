from faker import Faker
import requests

def get_Weather_data():
    fake = Faker()
    country = fake.country()
    API_ENDPOINT = f"https://api.openweathermap.org/data/2.5/weather?appid=35308e05b1df356376df6be58ce9bb9e&units=metric&q={country}"

    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        # Get weather data from response
        data = response.json()

        # Extract relevant information from data
        city = data['name']
        temp = data['main']['temp']
        weather_desc = data['weather'][0]['description']

        # Print weather information
        return data
    else:
        return {}

if __name__ == "__main__":
    print(get_Weather_data())

