import requests
import sys
from tkinter import Tk, Label, Entry, Button, Text, END

def get_weather(zip_code, api_key): # retrieves the weather data from the api
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
# CLI Interface - taken from chatgpt, i dont really know how to use this i couldnt get it to work and im a tad confused
def cli_interface():
    if len(sys.argv) != 2:
        print("Usage: weather <ZIP_CODE>")
        return
    
    zip_code = sys.argv[1]
    if len(zip_code) != 5 or not zip_code.isdigit():
        print("Bad ZIP code, please use a 5-digit ZIP code.")
        return
    
    api_key = "2090c15f968c595e2f8cffc690ad3865" # the keys take a couple hours to start working sometimes(in my experience). this is the key i used idk if itll still be active when you check this
    weather_data = get_weather(zip_code, api_key)
    if weather_data:
        forecast = display_forecast(weather_data)
        if forecast:
            for line in forecast:
                print(line)

# GUI Interface - also chatgpt i dont know how gui works with python ! i have another file that just does it in terminal if thats better because thats what i did before i actually read the assignment
def gui_interface():
    def fetch_forecast():
        zip_code = zip_input.get()
        if len(zip_code) != 5 or not zip_code.isdigit():
            result_box.delete("1.0", END)
            result_box.insert(END, "Invalid ZIP code. Please enter a 5-digit ZIP code.\n")
            return
        
        api_key = "2090c15f968c595e2f8cffc690ad3865" # the keys take a couple hours to start working sometimes(in my experience). this is the key i used idk if itll still be active when you check this
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
    if len(sys.argv) > 1:
        cli_interface()  # Use CLI if arguments are provided
    else:
        gui_interface()  # Default to GUI if no arguments are provided

if __name__ == "__main__":
    main()
