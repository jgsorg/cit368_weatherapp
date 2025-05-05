import requests
import os
from tkinter import Tk, Label, Entry, Button, Text, END, Frame
import json
import re
import logging
from cryptography.fernet import Fernet
import hashlib

logging.basicConfig(
    filename='weatherapp.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
if os.path.exists('weatherapp.log'):
    os.chmod('weatherapp.log', 0o600)

with open('secrets.json', 'r') as file:
    api_key = json.load(file)["key"]

# GUI Interface - also chatgpt i dont know how gui works with python ! i have another file that just does it in terminal if thats better because thats what i did before i actually read the assignment
def valid_zip(zip_code):
    url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},us&units=imperial&appid={api_key}'
    response = requests.get(url)
    zip_code = zip_code.strip() # removes whitespace
    if len(zip_code) != 5:
        return False
    if not zip_code.isdigit():
        return False
    if re.search(r"^\d{5}$", zip_code) is None:
        return False
    return True

def get_weather(zip_code, api_key): 
    try:
        url = f'http://api.openweathermap.org/data/2.5/forecast?zip={zip_code},us&units=imperial&appid={api_key}'
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return None
def hash_zip(zip_code):
    return hashlib.sha256(zip_code.encode()).hexdigest()

def display_forecast(weather_data):
    if weather_data:
        forecast = []
        try:
            for i in range(3):  # 3-day intervals
                day = weather_data['list'][i * 8]  # 8 entries per day
                date = day['dt_txt']
                temp = day['main']['temp']
                description = day['weather'][0]['description']
                forecast.append(f"{date}: {description} with a temperature of {temp}°F")
            return forecast
        except KeyError as e:
            logging.error(f"Error parsing weather data: {e}")
            return None
    return None

def gui_interface():
    def fetch_forecast():
        zip_code = zip_input.get()
        if not valid_zip(zip_code):
            result_box.delete("1.0", END)
            result_box.insert(END, "Please enter a valid 5-digit ZIP code.\nExample: 12345\n")
            logging.info(f"Invalid ZIP code entered: {zip_code}")
            return

        weather_data = get_weather(zip_code, api_key)
        result_box.delete("1.0", END)
        if weather_data:
            forecast = display_forecast(weather_data)
            if forecast:
                result_box.insert(END, "3-day weather forecast:\n")
                for line in forecast:
                    result_box.insert(END, line + "\n")
                # log the successful forecast request
                hashed_zip = hash_zip(zip_code)
                logging.info(f"Weather requested for hashed ZIP: {hashed_zip} — Forecast: {forecast}")

            else:
                result_box.insert(END, "Error fetching weather data. Check logs for details.\n")
                logging.error(f"Error parsing weather data for ZIP code {zip_code}.")
        else:
            result_box.insert(END, "Failed to fetch weather data. Check logs for details.\n")
            logging.error(f"Failed to fetch weather data for ZIP code {zip_code}.")

    # setting up the GUI window
    root = Tk()
    root.title("Weather!!")
    root.geometry("500x300") 
    root.configure(bg="#f0f0f0")

  
    title_label = Label(root, text="Weather Forecast App", font=("Times New Roman", 16, "bold"), bg="#f0f0f0", fg="#333")
    title_label.pack(pady=10)


    input_frame = Frame(root, bg="#f0f0f0")
    input_frame.pack(pady=10)

    Label(input_frame, text="Enter ZIP Code:", font=("Times New Roman", 12), bg="#f0f0f0", fg="#333").grid(row=0, column=0, padx=10, pady=5)
    zip_input = Entry(input_frame, font=("Times New Roman", 12), width=20)
    zip_input.grid(row=0, column=1, padx=10, pady=5)

    get_forecast_btn = Button(input_frame, text="Get Forecast", font=("Times New Roman", 12), bg="#4CAF50", fg="white", command=fetch_forecast)
    get_forecast_btn.grid(row=1, column=0, columnspan=2, pady=10)


    result_box = Text(root, font=("Times New Roman", 10), width=60, height=10, wrap="word", bg="#ffffff", fg="#333", borderwidth=2, relief="groove")
    result_box.pack(pady=10, padx=10)

    root.mainloop()

def main():
    logging.info("Application started")
    gui_interface()

if __name__ == "__main__":
    main()