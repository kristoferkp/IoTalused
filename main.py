import json
import urequests
import _thread
import time

start = time.ticks_ms()

apiKey = 'o.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' 

url = "https://api.pushbullet.com/v2/pushes"
headers = {'Access-Token': apiKey, 'Content-Type': 'application/json'}

dataHum = {'type':'note','body':'Humidity is above 50% !!!\nCome help!','title':'The Weather Channel'}
dataJSONHum = json.dumps(dataHum)

dataTemp = {'type':'note','body':'It is really hot in here!','title':'The Weather Channel'}
dataJSONTemp = json.dumps(dataTemp)


def otherThread():
    
  n = 0
  while True:
    if n % 5 == 0:
        read_sensor()
    if hum >= 50 and n == 0:
        t = time.localtime()

        r = urequests.post(url, headers=headers,data=dataJSONHum)
        print('Push Notification Sent - Hum ' + str(t))
    if temp > 27 and n == 0:
        t = time.localtime()

        r = urequests.post(url, headers=headers,data=dataJSONTemp)
        print('Push Notification Sent - Temp ' + str(t))
    if n == 60:
        n = -1
    n += 1
    time.sleep(1)

_thread.start_new_thread(otherThread, ())


def read_sensor():
  global temp, hum, pressure
  try:
    dht22.measure()
    temp = dht22.temperature()
    hum = dht22.humidity()
    temp2= bmp.temperature
    pressure = round(bmp.pressure, 1)
    temp = round((temp + temp2) / 2, 1)
    
    display.fill_rect(0, 25, 128, 45, 0)
    display.text("Hum: " + str(hum) + "%", 0, 25, 1)
    display.text("Temp: " + str(temp) + "C", 0, 35, 1)
    display.text("P: " + str(pressure) + "Pa", 0, 45, 1)
    display.show()
    
  except OSError as e:
    return('Failed to read sensor.')

def web_page():
  html = """<!DOCTYPE HTML><html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
      <style>
        html {
         font-family: Arial;
         display: inline-block;
         margin: 0px auto;
         text-align: center;
        }
        h2 { font-size: 3.0rem; }
        p { font-size: 3.0rem; }
        .units { font-size: 1.2rem; }
        .dht-labels{
          font-size: 1.5rem;
          vertical-align:middle;
          padding-bottom: 15px;
        }
        button {
            background-color: #008CBA; /* Blue */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
      </style>
    </head>
    <body>
      <h2>The Weather Channel</h2>
      <p>
        <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
        <span class="dht-labels">Temperature</span> 
        <span>"""+str(temp)+"""</span>
        <sup class="units">&deg;C</sup>
      </p>
      <p>
        <i class="fas fa-tint" style="color:#00add6;"></i> 
        <span class="dht-labels">Humidity</span>
        <span>"""+str(hum)+"""</span>
        <sup class="units">%</sup>
      </p>
      <p>
        <i class="fas fa-wind" style="color:#00add6;"></i> 
        <span class="dht-labels">Pressure</span>
        <span>"""+str(pressure)+"""</span>
        <sup class="units">Pa</sup>
      </p>
      <button onclick="location.reload();">Refresh Info</button>
    </body>
    </html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
      
    led.off()
    print('Got a connection from ' + str(addr))
    time.sleep(1)
    led.on()
      
    request = conn.recv(1024)
    response = web_page()
      
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
