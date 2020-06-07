import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "00dxkm"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()
# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
while True:
        hum=random.randint(10, 50)
        #print(hum)
        temp =random.randint(30, 90)
        vib=random.randint(10, 100)
        curr=random.randint(10, 50)
        
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Humidity': hum, 'Vibration': vib, 'Current':curr}
         #notification alerts-----------------------------------------------------------
        if temp>60 and hum>20:
                url = "https://www.fast2sms.com/dev/bulk"
                querystring = {"authorization":"oa1O3XmWyhSg7RY9A0JuqPTdc8wiBZHNxCKkelL5fbIGDvU2M49zwPxtsy5V6NMekh3jUpuXLFQCof0a","sender_id":"FSTSMS","message":"Temperature abnormal","language":"english","route":"p","numbers":"8096632863"}
                headers = {
                        'cache-control': "no-cache"
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)
        elif vib>60:
                url = "https://www.fast2sms.com/dev/bulk"
                querystring = {"authorization":"oa1O3XmWyhSg7RY9A0JuqPTdc8wiBZHNxCKkelL5fbIGDvU2M49zwPxtsy5V6NMekh3jUpuXLFQCof0a","sender_id":"FSTSMS","message":"Motor condition is abnormal","language":"english","route":"p","numbers":"8096632863"}
                headers = {
                        'cache-control': "no-cache"
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)
        elif curr>40:
                url = "https://www.fast2sms.com/dev/bulk"
                querystring = {"authorization":"oa1O3XmWyhSg7RY9A0JuqPTdc8wiBZHNxCKkelL5fbIGDvU2M49zwPxtsy5V6NMekh3jUpuXLFQCof0a","sender_id":"FSTSMS","message":"Motor components may short circuit","language":"english","route":"p","numbers":"8096632863"}
                headers = {
                        'cache-control': "no-cache"
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "Vibration = %s hz" % vib, "Current = %s amp" % curr,  "to IBM Watson")
        success = deviceCli.publishEvent("motor", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        deviceCli.commandCallback = myCommandCallback
# Disconnect the device and application from the cloud
deviceCli.disconnect()
