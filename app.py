import os

import pyodbc as pyodbc
from flask import Flask, render_template, request

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT','5000'))

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

@app.route('/')
def home():
    cur = cnxn.cursor()
    cur.execute("select PicturePas from minnow WHERE Fname = 'Janice'")
    get = cur.fetchone();
    return render_template('home.html', imgname=get[0])

@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/records1')
def records1():
    return render_template('records1.html')


@app.route('/options', methods=['POST', 'GET'])
def options():
    lat1 = float(request.form['lat1'])
    lat2 = float(request.form['lat2'])
    lon1 = float(request.form['lon1'])
    lon2 = float(request.form['lon2'])
    rows = []
    get = []
    c = []
    points = []
    points.append(['Lat Long Range','Count'])
    cur = cnxn.cursor()
    i = lat1
    j = lon1
    print ("charan")
    while(i < lat2 or j < lon2):
        cur.execute("select count(*) from all_month WHERE latitude between ? and ? and longitude between ? and ?",(i,i+1,j,j+1))
        get = cur.fetchone();
        key = str(i)+"-"+str(i + 1)+" & "+str(j)+"-"+str(j+1)
        points.append([key, get[0]])
        if(i < lat2):
            i =i+1
        if(j < lon2):
            j =j+1
    print(points)
    return render_template("list.html", p=points)

@app.route('/fare', methods=['POST', 'GET'])
def fare():
    rows = []
    get = []
    c = []
    points = []
    annotation = {'role':'annotation'}
    points.append(['Fare','Survived','Non-survived',annotation])
    cur = cnxn.cursor()
    cur.execute("select fare,count(survived) from [dbo].[minnow(3)] where survived = 1 group by fare")
    get1 = cur.fetchall();
    cur.execute("select fare,count(survived) from [dbo].[minnow(3)] where survived = 0 group by fare")
    get2 = cur.fetchall();
    print (get1)
    print (get2)
    for i in range(min(len(get1),len(get2))):
        points.append([get1[i][0],get1[i][1],get2[i][1],get1[i][1]])
    print (points)
    return render_template("list1.html", p=points)


@app.route('/quesseven', methods=['POST', 'GET'])
def quesseven():
    con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
   # r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    #start_time = time.time()
    age1=int(request.form['a1'])
    age2=int(request.form['a2'])
    fare1 = int(request.form['f1'])
    fare2 = int(request.form['f2'])
    rows = []
    #get = []
    c = []
    points = []
    points.append(['age', 'fare'])
        #val = round(random.uniform(2,5),1)
    cur = con.cursor()
    cur.execute("select age,fare from minnow WHERE Age between ? and ? and Fare between ? and ?",age1,age2,fare1,fare2)
    #, (age1, age2, fare1, fare2)
    get = cur.fetchall()
    for row in get:
      points.append([row[0],row[1]])
    print (points)

    return render_template("chart_pie.html",p=points)




# @app.route('/options', methods=['POST', 'GET'])
# def options():
#     con = pyodbc.connect(
#         'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
#     mc = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
#     age1 = int(request.form['age1'])
#     age2 = int(request.form['age2'])
#     cab1 = int(request.form['cab1'])
#     cab2 = int(request.form['cab2'])
#     rows = []
#     # get = []
#     c = []
#     points = []
#     c.append(['age', 'Lat'])
#     # val = round(random.uniform(2,5),1)
#     cur = con.cursor()
#     cur.execute("select age,fare from minnow WHERE Age between ? and ? and CabinNum between ? and ?",(age1,age2,cab1,cab2))
#     get = cur.fetchall()
#     for row in get:
#         c.append([row[0],row[1]])
#         print(c)
#         # points.append([row[0], row[1]])
#     return render_template("list1.html", rows=c)

if __name__ == '__main__':
    app.run()
