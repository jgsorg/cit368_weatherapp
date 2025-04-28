import requests
import sys
from tkinter import Tk, Label, Entry, Button, Text, END
import json
import re

with open('secrets.json', 'r') as file:
    api_key = json.load(file)["key"]

# GUI Interface - also chatgpt i dont know how gui works with python ! i have another file that just does it in terminal if thats better because thats what i did before i actually read the assignment
def valid_zip(zip_code):
    url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},us&units=imperial&appid={api_key}'
    response = requests.get(url) # gets response lol
    if len(zip_code) != 5:
        return False
    if not zip_code.isdigit():
        return False
    if re.search(r"^\d{5}$", zip_code) is None:
        return False
    return True

def get_weather(zip_code, api_key): 
    url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},us&units=imperial&appid={api_key}' # using f to be able to pick api key and zip
    response = requests.get(url) # gets response lol
    if response.status_code == 200: # if its successful it returns json data
        return response.json()
    else:
        print(f"error fetching data: {response.status_code}") # if it fails it will return the error code (u can look it up on the website)
        return None

def display_forecast(weather_data):
    if weather_data:
        forecast = []
        for i in range(3): # 3 day intervals
            day = weather_data['list'][i * 8] # 8 entries per day
            date = day['dt_txt']
            temp = day['main']['temp']
            description = day['weather'][0]['description']
            forecast.append(f"{date}: {description} with a temperature of {temp}°F")
        return forecast
    return None

def gui_interface():
    def fetch_forecast():
        zip_code = zip_input.get()
        if not valid_zip(zip_code):
            result_box.delete("1.0", END)
            result_box.insert(END, "Please enter a valid 5-digit zip code.\nExample: 12345\n")
            return
        
        weather_data = get_weather(zip_code, api_key)
        if weather_data:
            forecast = display_forecast(weather_data)
            result_box.delete("1.0", END)
            if forecast:
                result_box.insert(END, "3-day weather forecast:\n")
                for line in forecast:
                    result_box.insert(END, line + "\n")
            else:
                result_box.insert(END, "Error fetching weather data.\n")

    # Setting up the GUI window
    root = Tk()
    root.title("Weather Forecast")

    Label(root, text="Enter ZIP Code:").grid(row=0, column=0, padx=10, pady=10)
    zip_input = Entry(root)
    zip_input.grid(row=0, column=1, padx=10, pady=10)

    get_forecast_btn = Button(root, text="Get Forecast", command=fetch_forecast)
    get_forecast_btn.grid(row=1, column=0, columnspan=2, pady=10)

    result_box = Text(root, width=50, height=10)
    result_box.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

def main():
    gui_interface()

if __name__ == "__main__":
    main()