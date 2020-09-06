# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app
import json
import base64
import os.path
import time
import mysql.connector
import requests
import random


cnx = mysql.connector.connect(user='root', password='130560',
                                  host='127.0.0.1',
                                  database='worktime_new')
cursor = cnx.cursor()
quary = ('SELECT * FROM `computers`')
cursor.execute(quary)
print(cursor.fetchall())
cursor.close()

#Агент обращается при старте---------------------
@app.route('/start_connection', methods=['post', 'get'])
def start_connection():

#Создание токена---------------------------------
    znacheniya = 'qwertyuiopasdfghjklzxcvbnm0123456789QWERTYUIOPASDFGHJKLZXCVBNM'
    spisok = list(znacheniya)
    random.shuffle(spisok)
    half1 = ''.join([random.choice(spisok) for x in range(6)])
    half2 = ''.join([random.choice(spisok) for x in range(6)])
    token = half1 + half2


#Получение реквеста и запись токена

    data_f_client = json.loads(request.data)

    cursor = cnx.cursor()
    quary = ('update computers set token = "' + token + '" where name_computer = "' + data_f_client['name_computer'] + '"')
    cursor.execute(quary)
    cnx.commit()
    cursor.close()

    cursor = cnx.cursor()
    quary = ('select id_computer from computers where name_computer = "' + data_f_client['name_computer'] + '"')
    cursor.execute(quary)
    id_computer = []
    rows = cursor.fetchall()
    for row in rows:
        id_computer.append(row[0])
    cursor.close()

    id_comp = id_computer[0]

    return json.dumps({'token': token, 'id_computer': id_comp})


@app.route('/img')
def img():
    pict_mas = []
    count_pic = 0
    for picture in os.listdir(path='app/static/uploads'):
        pict_mas.append('uploads/' + picture)
    print(pict_mas)


    return render_template('img.html', title='Img', pictures=pict_mas)


@app.route('/dash', methods=['post', 'get'])

def dash():
#Вывод пользователей слево------------------
    cursor = cnx.cursor()
    quary = ('SELECT owner FROM `computers`')
    cursor.execute(quary)

    owners = []
    rows=cursor.fetchall()
    for row in rows:
        owners.append(row[0])
        print(row)
    cursor.close()
#--------------------------------------------
# Вывод картинок пользователя------------------
    name = request.args.get('user')
#массив id компьютеров-------------------------

    cursor = cnx.cursor()
    quary = ('SELECT id_computer FROM `computers` WHERE owner="' + name + '"')
    cursor.execute(quary)
    print(quary)

    comp_id_mass = []
    rows = cursor.fetchall()
    for row in rows:
        comp_id_mass.append(row[0])
    cursor.close()

    id_comp = comp_id_mass[0]
    id_comp = str(id_comp)
    
# --------------------------------------------


# Процесс И Сайты---------------
    process_mass=[]
    sites_mass=[]
    pict_mas = []

    if request.method == 'POST':
        datestart = request.form.get('datestart') 
        dateend = request.form.get('dateend')
        typex = request.form.get('type') 
        login = request.form.get('login')
        name_user = request.form.get('name_user')
        computer = request.form.get('computer')
        owner = request.form.get('owner')

        if typex == "user":
            cursor = cnx.cursor()
            quary = ('INSERT INTO users (login, name_user) VALUES ("' + login + '", "' + name_user + '")')
            cursor.execute(quary)
            cnx.commit()
            cursor.close()

            cursor = cnx.cursor()
            quary = ('SELECT name_user FROM `users`')
            cursor.execute(quary)
            owners = []
            rows=cursor.fetchall()
            for row in rows:
                owners.append(row[0])
                print(row)
            cursor.close()

            cursor = cnx.cursor()
            quary = ('select name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="process" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_proc = cursor.fetchall()
            for proc in vivod_proc:
                process_mass.append(proc)
            cursor.close()

            cursor = cnx.cursor()
            quary = ('select url, name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="url" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_sites = cursor.fetchall()
            for site in vivod_sites:
                sites_mass.append(site)
            cursor.close()


            cursor = cnx.cursor()
            quary = ('select screenshot, date_time from processandscreen where id_computer ="'+id_comp+'" and type="screenshot" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_pict=cursor.fetchall()
            for pict in vivod_pict:
                pict_mas.append(pict)
            cursor.close()

            pc_mass=[]
            cursor = cnx.cursor()
            quary = ('select * from computers')
            cursor.execute(quary)
            vivod_pc = cursor.fetchall()
            for pc in vivod_pc:
                pc_mass.append(pc)
            cursor.close()

        elif typex == "machine":
            cursor = cnx.cursor()
            quary = ('INSERT INTO computers (name_computer, owner) VALUES ("' + computer + '", "' + owner + '")')
            cursor.execute(quary)
            cnx.commit()
            cursor.close()

            cursor = cnx.cursor()
            quary = ('SELECT name_user FROM `users`')
            cursor.execute(quary)

            user_mass = []
            rows=cursor.fetchall()
            for row in rows:
                user_mass.append(row[0])
                print(row)
            cursor.close()

            cursor = cnx.cursor()
            quary = ('select name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="process" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_proc = cursor.fetchall()
            for proc in vivod_proc:
                process_mass.append(proc)
            cursor.close()

            cursor = cnx.cursor()
            quary = ('select url, name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="url" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_sites = cursor.fetchall()
            for site in vivod_sites:
                sites_mass.append(site)
            cursor.close()

            cursor = cnx.cursor()
            quary = ('select screenshot, date_time from processandscreen where id_computer ="'+id_comp+'" and type="screenshot" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_pict=cursor.fetchall()
            for pict in vivod_pict:
                pict_mas.append(pict)
            cursor.close()

            pc_mass=[]
            cursor = cnx.cursor()
            quary = ('select * from computers')
            cursor.execute(quary)
            vivod_pc = cursor.fetchall()
            for pc in vivod_pc:
                pc_mass.append(pc)
            cursor.close()

        else:
            cursor = cnx.cursor()
            quary = ('select name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="process" AND date_time >="' + datestart + '" AND date_time <="' + dateend + '" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_proc = cursor.fetchall()
            for proc in vivod_proc:
                process_mass.append(proc)
            cursor.close()

            cursor = cnx.cursor()
            quary = ('select url, name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="url" AND date_time >="' + datestart + '" AND date_time <="' + dateend + '" ORDER BY date_time DESC')
            cursor.execute(quary)
            vivod_sites = cursor.fetchall()
            for site in vivod_sites:
                sites_mass.append(site)
            cursor.close()


    else:
        cursor = cnx.cursor()
        quary = ('select name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="process" ORDER BY date_time DESC')
        cursor.execute(quary)
        vivod_proc = cursor.fetchall()
        for proc in vivod_proc:
            process_mass.append(proc)
        cursor.close()

        cursor = cnx.cursor()
        quary = ('select url, name_process, date_time, window_title from processandscreen where id_computer ="' + id_comp + '" and type="url" ORDER BY date_time DESC')
        cursor.execute(quary)
        vivod_sites = cursor.fetchall()
        for site in vivod_sites:
            sites_mass.append(site)
        cursor.close()

#-СКРИНШОТЫ НОРМАЛЬНЫЕ-------------------------

        pict_mass = []
        cursor = cnx.cursor()
        quary = ('select screenshot from processandscreen where id_computer ="'+id_comp+'" and type="screenshot"')
        cursor.execute(quary)
        vivod_pict = cursor.fetchall()
        for pict in vivod_pict:
            pict_mass.append(pict[0])
        cursor.close()
        print(pict_mass)

#----------------------------------------------

# Вывод Компов пользователей-------------------
    pc_mass=[]

    cursor = cnx.cursor()
    quary = ('select * from computers')
    cursor.execute(quary)
    vivod_pc = cursor.fetchall()
    for pc in vivod_pc:
        pc_mass.append(pc)
    cursor.close()
#------------------------------------------------




    return render_template('dash.html',title='Img', pictures=pict_mass, user_mass_dash=owners, process_mass_dash=process_mass, sites_mass_dash=sites_mass, pc_mass_dash=pc_mass)


@app.route('/auth', methods=['post', 'get'])
def auth():
    if request.method == 'POST':
        login = request.form.get('login')
        user_name = request.form.get('user_name')

        user=[]

        cursor = cnx.cursor()
        quary = ('select * from users WHERE login = "'+login+'" AND name_user = "'+user_name+'"')
        cursor.execute(quary)
        users = cursor.fetchall()
        for u in users:
            user.append(u)
        cursor.close()

        if user:
            nameMass = user_name.split()
            return redirect('/dash?user='+nameMass[0]+'%20'+nameMass[1]+'')

    return render_template('auth.html')



#Поулчение картинок---------------------------------------------
@app.route('/upload_pic', methods=['GET', 'POST'])
def upload_pic():
    if request.method == 'POST':
        data_f_client = json.loads(request.data)

#вывод нужного токена
        token = []

        cursor = cnx.cursor()
        quary = ('select token from computers where id_computer = "' + data_f_client['id_computer'] + '"')
        cursor.execute(quary)
        tokens = cursor.fetchall()
        for t in tokens:
            token.append(t)
        cursor.close()


        absolut_vremya = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        date_vremya = time.strftime("%Y-%m-%d", time.localtime())

   #     filecheck_date = f"app/static/{date_vremya}"

    #    if not os.path.exists(filecheck_date):
      #      os.mkdir(f"app/static/{date_vremya}")

        filecheck_name = f"app/static/{data_f_client['img_name']}"

        papka = data_f_client['img_name']

        if not os.path.exists(filecheck_name):
            os.mkdir(f"app/static/{data_f_client['img_name']}")

        f = open(f"app/static/{papka}/{data_f_client['name_process']+ ' ' + absolut_vremya + '.jpg'}", 'wb')
        decode64 = base64.b64decode(data_f_client['img_bytes'])
        f.write(decode64)
        f.close()

        the_way= f"{papka}/{data_f_client['name_process']+ ' ' + absolut_vremya + '.jpg'}"
        print(the_way)

        cursor = cnx.cursor()
        quary = ('INSERT INTO processandscreen (date_time, type ,name_process, window_title, screenshot, id_computer) VALUES ("' + absolut_vremya + '" , "' + data_f_client['type'] + '" , "' + data_f_client['name_process'] + '", "' + data_f_client['window_title'] + '", "' + the_way + '" ,"' + data_f_client['id_computer'] + '")')
        cursor.execute(quary)
        cnx.commit()
        cursor.close()


    return 'upload_finish'
#---------------------------------------------

#Поулчение прцоессов---------------------------------------------
@app.route('/upload_process', methods=['GET', 'POST'])
def upload_process():
    print(request)
    if request.method == 'POST':
        data_f_client = json.loads(request.data)
        print(data_f_client)

        absolut_vremya = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

        cursor = cnx.cursor()
        quary = ('INSERT INTO processandscreen (date_time, type ,name_process, window_title, id_computer) VALUES ("' + absolut_vremya + '" , "' + data_f_client['type'] + '" , "' + data_f_client['name_process'] + '", "' + data_f_client['window_title'] + '", "' + data_f_client['id_computer'] + '")')
        cursor.execute(quary)
        cnx.commit()
        cursor.close()

    return 'upload_finish'
#---------------------------------------------


#Получение вкладок---------------------------------------------
@app.route('/upload_url', methods=['GET', 'POST'])
def upload_url():
    print(request)
    if request.method == 'POST':
        data_f_client = json.loads(request.data)
        print(data_f_client)

        absolut_vremya = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())

        cursor = cnx.cursor()
        quary = ('INSERT INTO processandscreen (date_time, type ,name_process, url, window_title, id_computer) VALUES ("' + absolut_vremya + '" , "' + data_f_client['type'] + '" , "' + data_f_client['name_process'] + '", "' + data_f_client['url'] + '", "' + data_f_client['window_title'] + '", "' + data_f_client['id_computer'] + '")')
        cursor.execute(quary)
        cnx.commit()
        cursor.close()


    return 'upload_finish'
#---------------------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

