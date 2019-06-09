import socketio
import os
import io

sio = socketio.Client()

@sio.on('connect')
def connect():
    print('connection established')
    sio.emit('transcribe', {
      'fn': 'big-shaq.mp4',
      'accent': 'en-GB'
    }) 
    print('sent message')
      

@sio.on('transcribe')
def my_message(data):
  print('Transribe')
  print(data, '/n')

@sio.on('status')
def status(data):
  print('Status')
  print(data, '/n')

sio.connect('http://localhost:3000')
sio.wait()
