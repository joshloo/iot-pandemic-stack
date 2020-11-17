# iot-pandemic-stack

This repo consists of code for
QR Scanner
Temperature Sensing
Upload to cloud

The environment executing this scripts are Raspberry Pi 400.

# Step pre-requisite for QR Scanner
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
qr-scanner\example-snapshot.png