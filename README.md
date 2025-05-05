# Weather Forcast App

## Overview

This is a secure Python weather forecast app that lets users input a ZIP code and then view a 3day forecast.

It accomplishes this using the OpenWeatherMap API.

The application has a graphical interface, made using Tkinter, proper error handling, logging, and implements security priciples throughout the code.

---

## Dependencies

To run this, you have to have Python installed. You must also install requests and cryptography with pip.

## Threat Modeling Process

Some common threats are things like exposure of the API key, malicious input (ZIP in this case), and logging user info.

To mitigate these I stored the API key in 'secrets.json' while excluding it from the commit history. I also made sure that the zip code input was validated and sanitized by using regex and digit checking. To mitigate the threat of logging user info, I hashed the user's zip code whenever it gets put into the weatherapp.log file (which is also in .gitignore). I also restricted the file permissions of that file.

A threat that is not handled could be no user authentication / rate limiting. This could lead to a user or bot spamming requests, and since there is no protection like logins or captchas, a bot could easily spam it without running into authentication errors.

