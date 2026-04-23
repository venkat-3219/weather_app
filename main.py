# Weather App
import sys
import requests

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QFrame)

from PyQt5.QtCore import Qt

class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        import os

        self.setWindowTitle("Weather App")
        self.resize(500, 700)
        self.setObjectName("WeatherApp")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.glass_frame = QFrame(self)
        self.glass_frame.setObjectName("glass_frame")

        vbox = QVBoxLayout(self.glass_frame)
        vbox.setContentsMargins(40, 40, 40, 40)
        vbox.setSpacing(20)
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.addWidget(self.glass_frame)
        self.setLayout(main_layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weather_bg.png").replace("\\", "/")

        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Calibri, sans-serif;
            }
            #WeatherApp {
                border-image: url('%s') 0 0 0 0 stretch stretch;
            }
            QFrame#glass_frame {
                background-color: rgba(255, 255, 255, 130);
                border: 2px solid rgba(255, 255, 255, 200);
                border-radius: 30px;
            }
            QLabel {
                background: transparent;
            }
            QLabel#city_label {
                font-size: 38px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            QLineEdit#city_input {
                font-size: 30px;
                font-weight: bold;
                padding: 12px 20px;
                border: 2px solid rgba(255, 255, 255, 180);
                border-radius: 25px;
                background-color: rgba(255, 255, 255, 220);
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: #ffffff;
            }
            QLineEdit#city_input:focus {
                border: 3px solid #3498db;
                background-color: rgba(255, 255, 255, 255);
            }
            QPushButton#get_weather_button {
                font-size: 28px;
                font-weight: bold;
                background-color: rgba(52, 152, 219, 210);
                color: white;
                border: 2px solid rgba(255, 255, 255, 150);
                border-radius: 20px;
                padding: 12px 24px;
                margin-top: 15px;
            }
            QPushButton#get_weather_button:hover {
                background-color: rgba(41, 128, 185, 230);
            }
            QPushButton#get_weather_button:pressed {
                background-color: rgba(28, 89, 128, 255);
            }
            QLabel#temperature_label {
                font-size: 75px;
                color: #2c3e50;
                margin-top: 20px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: 'Segoe UI Emoji', 'Apple Color Emoji';
            }
            QLabel#description_label {
                font-size: 45px;
                font-weight: bold;
                color: #2c3e50;
            }    
        """ % bg_path)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = "b659affd6c4346cab05aa82224dc2dbf"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if str(data.get("cod")) == "200":
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "Unknown API error"))

        except requests.exceptions.HTTPError as http_error:
            status_code = response.status_code
            match status_code:
                case 400:
                    self.display_error("Bad request. Please check your input.")
                case 401:
                    self.display_error("Unauthorized. Invalid API key.")
                case 403:
                    self.display_error("Forbidden. Access is denied.")
                case 404:
                    self.display_error("City not found.")
                case 500:
                    self.display_error("Internal server error. Please try again later.")
                case 502:
                    self.display_error("Bad gateway. Invalid response from server.")
                case 503:
                    self.display_error("Service unavailable.")
                case 504:
                    self.display_error("Gateway timeout. No response from server.")
                case _:
                    self.display_error(f"HTTP error occurred: {http_error}")
        except requests.exceptions.RequestException as request_error:
            self.display_error(f"Network error: {request_error}")

    def display_error(self, message):
        self.temperature_label.setText("")
        self.emoji_label.setText("⚠")
        self.description_label.setText(message)

    def display_weather(self, data):
        temp_kelvin = data["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        description = data["weather"][0]["description"].title()

        self.temperature_label.setText(f"{temp_celsius:.1f}°C")
        self.emoji_label.setText("🌤")
        self.description_label.setText(description)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_App = WeatherApp()
    weather_App.show()
    sys.exit(app.exec_())
