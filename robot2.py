import socketio
import time
import wget
import numpy as np

sio = socketio.Client()

map_number = 'map_1'
localisation = 'Courbevoie'

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

def check_map():
    sio.emit('check_map', data = {sio.get_sid() : [map_number, localisation]})


@sio.on('good')
def good_map():
    print('I have the good map ! What would you expect ?')

@sio.on('download')
def download_map(data):
    print(data)
    wget.download(data, '/home/teddy/Documents/DEVO/API_DEVO/MAP/map')

def send_position():
    position = np.random.rand(1,3)
    sio.emit('sensors', data = position.tolist())


if __name__ == '__main__':
    sio.connect('http://localhost:5000', auth='MK2R2_2')
    print('sid: ', sio.get_sid())
    
    # check_map()

    i = 0
    while True:
        if i%5 == 0:
                check_map()
        if i%1 == 0:
            send_position()
        sio.emit('ping', {'ping': '2'})
        time.sleep(1) 
        i += 1