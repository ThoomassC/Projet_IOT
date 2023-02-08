#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>


#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme;

Adafruit_SSD1306 display = Adafruit_SSD1306(128, 64, &Wire);
unsigned long delayTime;

const char *ssid = "WIFI_Pi4";
const char *password = "123456789";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 3600, 60000);

String arr_days[]={"Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"};
String date_time;

void setup() {
  Serial.begin(9600);
  Serial.println(F("BME280 test"));
  Wire.pins(2, 0);
  Wire.begin();

  WiFi.begin(ssid, password);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

  while ( WiFi.status() != WL_CONNECTED )
  {
    delay ( 500 );
    Serial.print ( "." );
  }

  display.clearDisplay();

  display.setTextSize(1, 2); 

  display.setTextColor(WHITE);

  display.setCursor(5, 2);

  display.println("Bienvenue dans");

  display.println(" notre Projet");

  display.println("      :)");

  display.display();

  delay(3000);

  timeClient.begin();
  
  bool status;
  status = bme.begin(0x76);  
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

  Serial.println("-- Default Test --");
  delayTime = 1000;

  Serial.println();
}


void loop() { 
  
  display.setCursor(0,0);
  display.clearDisplay();

  timeClient.update();
  Serial.println(" "+timeClient.getFormattedTime());

  int hh = timeClient.getHours();

  int mm = timeClient.getMinutes();

  int ss = timeClient.getSeconds();

  display.print(hh);

  display.print(":");

  display.print(mm);

  display.print(":");

  display.print(ss);

  int day = timeClient.getDay();

  display.println(" "+arr_days[day]);

  date_time = timeClient.getFormattedTime();

  int index_date = date_time.indexOf("T");

  String date = date_time.substring(0, index_date);

  
  Serial.print("Temperature = "); Serial.print(bme.readTemperature()); Serial.println(" *C");
  display.print("Temperature: "); display.print(bme.readTemperature()); display.println(" *C");

  Serial.print("Pression = "); Serial.print(bme.readPressure() / 100.0F); Serial.println(" hPa");
  display.print("Pression: "); display.print(bme.readPressure() / 100.0F); display.println(" hPa");

  Serial.print("Humidite = "); Serial.print(bme.readHumidity()); Serial.println(" %");
  display.print("Humidite: "); display.print(bme.readHumidity()); display.println(" %");

  Serial.println();
  display.display();
  delay(1000);
}