#!/usr/bin/env python3
#
# This script requires the following:
# 1. A Dylos DC1100 Pro with serial interface
# 2. a working InfluxDB server ready to receive measurement data
# 3. (Optional) a Grafana installation reading data from InfluxDB for nice graphs but Influx can do graphs too 
#
import sys
import serial
import time
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# We use Influx to log all data
def init_influx(config):
    client = InfluxDBClient(url=f"https://{config['influx_server']}:{config['influx_port']}", token=config['influx_token'], org=config['influx_org'], verify_ssl=config['verify_ssl'], ssl_ca_cert=config['ssl_ca_cert'] )
    # You may have to disable SSL verification if your InfluxDB server is not configured to use SSL/TLS.
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return write_api

def convert_to_pm(small,large):
    # Dylos air quality monitors measure in number of particles per square foot, but we are interested in PM 2.5
    # So we need to convert the raw number of particles to an estimation of PM 2.5.
    # Particle to µg/m3 conversion is based based on page 17 from this document (also in github repo of this project):
    # https://www.scapeler.com/wp-content/uploads/2019/12/Project%20Report%20VISIBILIS_Final%20Version%201.2-compact.pdf0
    
    l = int(large)
    s = int(small) - l # document states that PM10 should be substracted from PM2.5 count to get 'pure' PM2.5 figure.
        
    pm10 = round((float(l) / 3),2) # I have honestly no idea if this is accurate, I only look at PM 2.5
    pm25 = round((s/250),1)        # That division is based on the paper above, which in turn states that it's based
                                   # on official Dylos recommendation, but I was never able to verify this info. 
    
    # The Dylos DC 1100 Pro can measure particles from 0.5µg to 2.5µg which is reflected in the PM2.5 value.

    data = {
            "pm25": pm25, "pm10": pm10, "pm25particles": s 
    }
    return data

def get_dylos_data(config):
    line = config['interface'].readline().decode("UTF-8").strip()
    time.sleep(1)
    small,large = line.split(",") # PM2.5 vs PM10
    data = convert_to_pm(small,large)
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{date} | Raw data: {line} | PM2.5: " + str(data['pm25']) + " | PM10: " + str(data['pm10']) + " |")
    return data
    
def send_to_influx(config, data):
    points = []
    for key in data.keys():
        value = data[key]
        points.append(Point("Dylos").field(key, value))
    try:
        config['influx'].write(bucket=config['influx_bucket'], record=points)
    except Exception as e:
        print("Failed to send data to influx")
        print(e)
        config['influx'] = init_influx(config)

def get_config():
    config = {}
    # 1. Configure the serial port
    # 2. Configure InfluxDB settings
    config['interface'] = serial.Serial('/dev/ttyUSB0', 9600, timeout=70)  # Serial port for Dylos DC1100 Pro
    config['influx_server'] = "IP address or domain name of the influxdb server"
    config['influx_port'] = 8086 # default for InfluxDB
    config['verify_ssl'] = True # You may have to disable this option or rip out the code even if SSL is not used 
    config['ssl_ca_cert'] = "/usr/local/share/ca-certificates/YOUR_CA_CERTIFICATE (if required)" 
    config['influx_bucket'] = "Dylos" 
    config['influx_org'] = "your influx db org" 
    config['influx_token'] = "a token generated for the API account with write permissions on the appropriate bucket"
    config['influx'] = init_influx(config)
    return config

def main():
    config = get_config()
    try:
        while True:
            data = get_dylos_data(config)
            if config['influx']:
                try:
                    send_to_influx(config, data)
                except:
                    print("Failed to send pm2.5/pm10 data to Influx")
            else:
                print("Influx client not initialized, not submitting data")
    except KeyboardInterrupt:
        print("Aborting...")
        config['interface'].close()
        sys.exit(1)

if __name__ == "__main__":
    main()
