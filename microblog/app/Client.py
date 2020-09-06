import requests
import os
import json
import base64
import socket
import random



name = os.path.basename(r'static/kartinki/15735034537980.jpg')
print(name)
f = open('static/kartinki/15735034537980.jpg', 'rb')
data_img = f.read()




response = requests.post('http://127.0.0.1:5000/upload_pic', data=json.dumps({'img_bytes': base64.b64encode(data_img).decode(), 'img_name':  socket.gethostname(),'type':'screenshot','name_process':'pycharm','window_title':'microblog/ba/ba', 'id_computer': '3'}))
#data_img - сначала оригинальные байты картинки,
#потом base64.b64encode(data_img) преобразует в base64 байты,
#а .decode преобразует base64 байты в строку, чтобы json.dumps мог преобразовать словарь питона в json строку
#От клиента ожидаю json строку в которйо есть поле img_bytes и имя картинки img_name.
print(response)

#response = requests.post('http://127.0.0.1:5000/upload_process', data=json.dumps({'type': 'process', 'name_process': 'pycharm.exe', 'token': '1234567890qwerty', 'window_title': 'microblog/bla/bla', 'id_computer': '2'}))
#print(response)


#response = requests.post('http://127.0.0.1:5000/upload_url', data=json.dumps({'type': 'url', 'name_process': 'chrome', 'url': 'vk.com', 'token': '1234567890qwerty', 'window_title': 'chrome', 'id_computer': '2'}))
#print(response)

#response = requests.post('http://127.0.0.1:5000/start_connection', data=json.dumps({'name_computer': 'SQUILLPX'}))
#print(response.json()['token'], response.json()['id_computer'])
