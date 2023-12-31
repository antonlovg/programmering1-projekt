import requests
import datetime
import json
import os
import pytz
import ui

def main():

    def weather_getcity():
        with open ("city.json", "r") as myFile:
            main_input = myFile.read()
            main_input = json.loads(main_input)
            return main_input.title()
    
    def weather_cloud():
        if weather['cloud_pct'] > 30 and weather['cloud_pct'] < 60:
            coverage = "partially cloudy"

        elif weather['cloud_pct'] >= 60:
            coverage = "cloudy"
            
        else:
            coverage = "sunny"
        print (f"It's {coverage} in {city} with a cloud coverage of {weather['cloud_pct']}%")

    def weather_temp():
        # Om temperaturen "Känns som" den aktuella temperaturen så behöver det inte nämnas
        if weather['temp'] != weather["feels_like"]:
            print (f"the temperature is currently at {weather['temp']}°C but feels like {weather['feels_like']} °C")

        else: 
            print (f"the temperature is currently at {weather['temp']}°C")

        print (f"The temperature range today will be between {weather['min_temp']}°C and {weather['max_temp']}°C")

    def weather_humid():
        print (f"Humidity level is at {weather['humidity']}%")

    def weather_wind():
        # Vindstyrka och riktning i grader (0-360) blir mer lättläst i kardinaler
        degrees = weather["wind_degrees"]
        cardinals = ["Northern", "Northeastern", "Eastern", "Southeastern", "Southern", "Southwestern", "Western", "Northwestern", "Northern"]
        cardinal = cardinals[round(degrees / 45)]
        print (F"There's a {cardinal} wind at {weather['wind_speed']} meters per second")

    def weather_sun():
        # Originell API hämtar soltimmar från angivna staden men utefter UTC tid. Denna URL är Worldtimes API för att kunna omvandla det till lokal tid
        urlzone = f'https://api.api-ninjas.com/v1/worldtime?city={city}'
        response = requests.get(urlzone, headers={'X-Api-Key': 'P56lgPDrmRuinArO1ubksg==A0OfMd46O71uIjAv'})
        response_dict = json.loads(response.text)

        try:
            timezone_str = response_dict['timezone']
            timezone = pytz.timezone(timezone_str)
        
            sunrise_utc = datetime.datetime.utcfromtimestamp(weather['sunrise'])
            sunset_utc = datetime.datetime.utcfromtimestamp(weather['sunset'])

            local_sunrise = sunrise_utc.replace(tzinfo=pytz.utc).astimezone(timezone)
            local_sunset = sunset_utc.replace(tzinfo=pytz.utc).astimezone(timezone)
            
            print(f"Today the sun rises in {city} at {local_sunrise.strftime('%H:%M')} and sets at {local_sunset.strftime('%H:%M')}")
        
        except KeyError:
            print ("Could not find the sun in", city)
            input ("Press Enter to continue")
    
    def weather_getdata():
        api_url = f'https://api.api-ninjas.com/v1/weather?city={city}'
        response = requests.get(api_url, headers={'X-Api-Key': 'dYoSBiEQ2LdY439GrifdSw==7OgS2qGCvv1GiXs8'})

        if response.status_code != requests.codes.ok:
            print("Could not fetch the weather from", city)
            input("Press Enter to continue")

        if response.status_code == requests.codes.ok:
            return response.json()

    # Hämtar användarens val av stad från huvudprogrammet och sedan data om den staden
    city = weather_getcity()
    weather = weather_getdata()

    # Hämtar favoritlistan eller skapar en tom om den inte finns
    favorites = []
    
    if os.path.exists ("favorites.json"):
        with open ("favorites.json", "r") as myFile:
            favorites = myFile.read()
            favorites = json.loads(favorites)
    else:
        with open ("favorites.json", "a+") as myFile:
            myFile.write(json.dumps(favorites))
    
    while True:  
        os.system("cls") if os.name == "nt" else os.system("clear")

        # Här börjar UI
        ui.line()
        ui.header(".:   Weather Analyzer   :.")
        ui.line()
        print(f"|{city.center(28)}|")
        ui.line()
        print("| 1 | Cloud" + "|".rjust(19))
        print("| 2 | Temperature" + "|".rjust(13))
        print("| 3 | Wind" + "|".rjust(20))
        print("| 4 | Humidity" + "|".rjust(16))
        print("| 5 | Sun forecast" + "|".rjust(12))
        print("| 6 | All of the above" + "|".rjust(8))
        print("| 7 | View / Edit favorites" + "|".rjust(3))
        print("| 8 | Exit Weather Analyzer" + "|".rjust(3))
        ui.line()
        print("Type the number for the alternative")
        user_input = input("you wish to know more about: ")

        # Användaren får välja alternativ de vill utföra
        os.system("cls") if os.name == "nt" else os.system("clear")
        print(".:     Weather Analyzer     :.")
        print("-" * 30)

        if user_input == "1":
            weather_cloud()
            input ("Press Enter to continue")
            continue

        elif user_input == "2":
            weather_temp()
            input ("Press Enter to continue")
            continue

        elif user_input == "3":
            weather_wind()
            input ("Press Enter to continue")
            continue

        elif user_input == "4":
            weather_humid()
            input ("Press Enter to continue")
            continue

        elif user_input == "5":
            weather_sun()
            input ("Press Enter to continue")
            continue

        # Detta alternativ skriver ut samtliga funktioner
        elif user_input == "6":
            weather_cloud()
            ui.line()
            weather_temp()
            ui.line()
            weather_wind()
            ui.line()
            weather_humid()
            ui.line()
            weather_sun()
            ui.line()
            input ("Press Enter to continue")
            continue

            # Lista av favoritstäder
        elif user_input == "7":
            if len(favorites) > 0:
                ui.header("Favorites")
                ui.line()

                i = 1
                for items in favorites:
                    item = f"| {i} | {items:<22} |"
                    print (item)
                    i += 1

                ui.line()
                print(f"Enter 'add' to add {city} to your favorite list")
                print(f"Enter 'use' to analyze a city from your favorite list")
                print(f"Enter 'del' to delete a city from your favorite list")
                fav_input = input("Or press Enter to return > ")
                ui.line()

                # Lägg till stad som du valde från main programmet
                if fav_input == "add":
                    favorites.append(city)

                    with open ("favorites.json", "w") as myFile:
                        myFile.write(json.dumps(favorites))
                        print (city, "Added to favorites")
                        input("Press Enter to continue")
                        ui.line()

                # Byt till en stad från din favoritlista
                elif fav_input == "use":
                    try:
                        fav_input = int(input("Enter the number representing the city you wish to analyze > "))
                        city = favorites[(fav_input - 1)]

                        with open ("city.json", "w") as myFile:
                            myFile.write(json.dumps(city))

                        weather = weather_getdata()
                        print("Now analyzing", city)

                    except (ValueError, IndexError):
                        print("Could not find the item you entered")
                        input("Press Enter to continue")
                        
                # Ta bort en stad från din favoritlista
                elif fav_input == "del":
                    try:
                        fav_input = int(input("Enter the number representing the city you wish to remove > "))
                        
                        removed_item = favorites[(fav_input - 1)]
                        favorites.pop(fav_input - 1)
                        print(removed_item, "has been deleted from your list")

                        with open ("favorites.json", "w") as myFile:
                            myFile.write(json.dumps(favorites))

                        input ("Press Enter to continue")

                    except (ValueError, IndexError):
                        print("Could not find the item you entered")
                        input("Press Enter to continue")
                
                # Om favoritlistan är tom så erbjuds användaren endast att lägga till den stad som valdes i main
            else:
                print("You have no favorites yet.")
                print (f"Enter 'y' if you would like to add {city} to your favorites")
                fav_input = input("or press Enter to return > ")
                ui.line()

                if fav_input == "y":
                    favorites.append(city)
                    with open ("favorites.json", "w") as myFile:
                        myFile.write(json.dumps(favorites))
                        print (city, "Added to favorites")
                        input("Press Enter to continue")
            
            continue

        # Avsluta programmet
        elif user_input == "8":
            break

        else:
            print("Invalid input")
            input("Press Enter to continue")
            continue


# Nedan är exempel på datan man får från API
# {"cloud_pct": 75, "temp": 17, "feels_like": 16, "humidity": 70, "min_temp": 14, "max_temp": 18, "wind_speed": 2.06, "wind_degrees": 0, "sunrise": 1695275057, "sunset": 1695319397}
