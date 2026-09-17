import httpx

weather_code_map = {
    0: "clear",
    1: "partly_cloudy",
    2: "partly_cloudy",
    3: "cloudy",
    45: "fog",
    48: "fog",
    51: "drizzle",
    53: "drizzle",
    55: "drizzle",
    56: "drizzle",
    57: "drizzle",
    61: "rain",
    63: "rain",
    65: "rain",
    66: "rain",
    67: "rain",
    80: "rain",
    81: "rain",
    82: "rain",
    71: "snow",
    73: "snow",
    75: "snow",
    77: "snow",
    85: "snow",
    86: "snow",
    95: "thunderstorm",
    96: "thunderstorm",
    99: "thunderstorm",
}

# tworzymy funkcje async, która jest wymagana, jeżeli w funkcji chociaż raz występuje await i trzeba czekać na jakąś odpowiedz
async def get_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"

    # Definiujemy szerkość i wysokośc geograficzną
    params = {"latitude": lat, "longitude": lon, "current": "temperature_2m,weather_code"}

    async with httpx.AsyncClient() as client:
        # Korzystamy z funkcji await, aby poczekać z resztą kodu, aż do uzyskania odpowiedzi
        response = await client.get(url, params=params)

    data = response.json()

    temperature = data["current"]["temperature_2m"]

    weather_code = data["current"]["weather_code"]

    condition = weather_code_map.get(weather_code, "unknown")

    return {"temperature": temperature, "condition": condition}