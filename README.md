# iot-pandemic-stack

This repo consists of code for  
- QR Scanner  
- Temperature Sensing  
- LCD display module    
- Upload to cloud  

The environment executing this scripts are Raspberry Pi 400.  

# Step guide for QR Scanner  
Generating QR Scanner:  
pip3 install qrcode[pil]  
import qrcode  
code = qrcode.make('Hello world!')  
code.save(<filename>.png)  

Setting up openCV  
sudo apt-get update  
sudo apt-get install python3-opencv  
sudo apt-get install libqt4-test python3-sip python3-pyqt5 libqtgui4 libjasper-dev libatlas-base-dev -y  
pip3 install opencv-contrib-python==4.1.0.25  
sudo modprobe bcm2835-v4l2  

Executing the script  
python3 qr-scanner\qr-scanner.py  

Example output  
![Example output](https://github.com/joshloo/iot-pandemic-stack/blob/main/qr-scanner/example-snapshot.png)  

# Step guide for Temperature Sensor  
This demo uses MLX 90614 temperature sensing module  
It communicates with Raspberry Pi through i2c1  

Setting up i2c in Raspberry pi  
run "sudo raspi-config"  
go to "Interfacing options"  
go to "P5 I2C" or equivalent  
select "yes" for enable  
select "finish"  
run "ls /dev/*i2c*"  
you should be able to see connected i2c appearing  
cd temp-sensor  
python3 temp-sensor.py  

![Example output](https://github.com/joshloo/iot-pandemic-stack/blob/main/temp-sensor/example-snapshot.png)  

# Step guide for LCD display module  
This demo uses I2C to communicate with 4x20 LCD display module  
It communicates with Raspberry Pi through i2c0  
I2C0 is actually disabled by default in Rasp Pi  
You will need to go change /boot/config.txt and add "dtparam=i2c_vc=on"  
sudo reboot, then i2c0 will appear in /dev/    
Reference: https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all  

python3 lcd_i2c.py  

![Example output](https://github.com/joshloo/iot-pandemic-stack/blob/main/i2c-lcd-display/example-snapshot.png)  

# Step guide for web server setup  
This demo uses Python Flask module, coupled with SQLAlchemy and Marshmallow framework.  

pre requisite: pip3 install flash-sqlalchemy flash-marshmallow flask-restful requests marshmallow-sqlalchemy  
Reference: https://towardsdatascience.com/develop-database-driven-rest-api-with-python-in-10-minutes-9b8cbb7ce5b2  
Reference: https://www.hackster.io/mjrobot/from-data-to-graph-a-web-journey-with-flask-and-sqlite-4dba35  

python3 flask-sql3.py  

In another terminal, run  
python3 create_db.py  

to inspect sqlite3 data base, run the following  
sqlite3 covid.db  
select * from user;  

On web browser, run http://127.0.0.1:5000

![Example output](https://github.com/joshloo/iot-pandemic-stack/blob/main/web-database/example_snapshot.png)


# [Staging] Guides for GPS from Google Geo API  
go to https://console.cloud.google.com/apis/library?filter=category:maps  
select Geocoding API  
Click enable  
Follow the steps here at https://developers.google.com/maps/documentation/geocoding/get-api-key to get an API key  
Copy the API key and add it to the HTTP RESTful request

pre-requisite: pip install geolocation-python  
