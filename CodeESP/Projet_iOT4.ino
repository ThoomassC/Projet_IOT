#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <Time.h>
#include <ESP8266HTTPClient.h>

#define SEALEVELPRESSURE_HPA (1013.25)
#define NUM_VALUES 10

Adafruit_BME280 bme;
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 64, &Wire);

const char *ssid = "WIFI_Pi4";
const char *password = "123456789";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 3600, 60000);

String arr_days[]={"Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"};

float pressure_values[NUM_VALUES];
float temperature_values[NUM_VALUES];
float humidity_values[NUM_VALUES];
int i = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("BME280 test");
  Wire.pins(2, 0);
  Wire.begin();

  WiFi.begin(ssid, password);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  display.clearDisplay();

  display.setTextSize(1, 2);
  display.setTextColor(WHITE);
  display.setCursor(5, 2);
  display.println("Bienvenue dans");
  display.println("  notre Projet");
  display.println("       :)");
  display.display();

  delay(3000);

  timeClient.begin();
  
  bool status;
  status = bme.begin(0x76);  
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }
  Serial.println();
}

void loop() { 
  display.setCursor(0,0);
  display.clearDisplay();

  timeClient.update();
  Serial.println(" "+timeClient.getFormattedTime());
  String time = timeClient.getFormattedTime();
  display.print(time);

  int day = timeClient.getDay();
  display.println(" "+arr_days[day]);

  float pressure = bme.readPressure() / 100.0F;
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();

  pressure_values[i] = pressure;
  temperature_values[i] = temperature;
  humidity_values[i] = humidity;

  i = (i + 1) % NUM_VALUES;

  // Calculer la moyenne
  float pressure_average = 0.0;
  float temperature_average = 0.0;
  float humidity_average = 0.0;
  for (int j = 0; j < NUM_VALUES; j++) {
    pressure_average += pressure_values[j];
    temperature_average += temperature_values[j];
    humidity_average += humidity_values[j];
  }
  pressure_average /= NUM_VALUES;
  temperature_average /= NUM_VALUES;
  humidity_average /= NUM_VALUES;
  
  Serial.print("Temperature = "); Serial.print(temperature_average); Serial.println(" *C");
  display.print("Temperature: "); display.print(temperature_average); display.println(" *C");

  Serial.print("Pression = "); Serial.print(pressure_average); Serial.println(" hPa");
  display.print("Pression: "); display.print(pressure_average); display.println(" hPa");

  Serial.print("Humidite = "); Serial.print(humidity_average); Serial.println(" %");
  display.print("Humidite: "); display.print(humidity_average); display.println(" %");

  Serial.println();
  display.display();
  delay(5000);

  HTTPClient http;
  WiFiClient client;
  http.begin(client, "http://192.168.137.5:80/api/data");
  http.addHeader("Content-Type", "application/json");
  String payload = "{\"temperature\": " + String(temperature_average) +
                  ",\"humidity\": " + String(humidity_average) +
                  ",\"pressure\": " + String(pressure_average) + 
                  ",\"day\": " + String(day) +
                  ",\"hour\": \"" + time + "\"}";
  int httpResponseCode = http.POST(payload);
  if (httpResponseCode > 0) {
    Serial.println("Data sent");
    Serial.println(payload);
  } else {
    Serial.println("Error sending data");
    Serial.println(payload);
  }
  http.end();

  delay(5000);
}