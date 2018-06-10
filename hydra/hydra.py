import flask
import sqlite3
import hashlib
import random

app = flask.Flask(__name__)
app.secret_key = ".ohmygoodnessthiscoughisdrivingmecrazy.Takingabreathwithoutdyingwouldreallybehice!"

DATABASE = 'hydra.db'

iptables_path = "/sbin/iptables"
route_path = "/sbin.route"
ip_path = "/sbin/ip"
iptables_teamplate="""
#!/bin/sh
/usr/sbin/netplan apply
/sbin/iptables -F
/sbin/ip rule flush
/sbin/ip rule add from all lookup main pref 32766

cursor.execute("select room,interface,addresses from rooms")


for classes_enabled in cursor.execute("select enabled from enabled;"):
     room,class = enabled.split("_")
     roomaddresses = getroom_addresses(room)
     for eachaddress in roomaddresses:
         #add that ip to the table
         "/sbin/ip rule add from {0} table {1}".format(eachaddress, classname) 

"/sbin/ip route add default via 10.20.1.254 dev ens33 table {0}".format(classname)

"/sbin/ip rule add from {0} table {1}".format(room subnet, classname)
"""
   

def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET", "POST"])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        print(username,password)        
        if username.lower() == "hydra" and password == "QwerTy!@34":
            flask.session['loggedin'] = True
            return flask.redirect(flask.url_for('matrix'))
        else:
            return flask.abort(401)
    else:
        return flask.Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

@app.route('/matrix',methods=['GET'])
def matrix():
    if not "loggedin" in flask.session:
          flash.redirect(flask.url_for("login"))
    datab = get_db()
    cursor = datab.cursor()
    classes = sum(cursor.execute("select class from classes;").fetchall(), () )
    rooms  = sum( cursor.execute("select room from rooms;").fetchall(), () )
    enabled = sum( cursor.execute("select roomclass from enabled;").fetchall(), () )
    print(classes, rooms,enabled)
    response = flask.render_template('index.html', classes=classes, rooms=rooms, enabled=list(enabled))
    return response


@app.route('/matrix',methods=['POST'])
def matrix_post():
    if not "loggedin" in flask.session:
          flash.redirect(flask.url_for("login"))
    print("The JSON DATA",flask.request.json)
    for eachdict in flask.request.json:
        print(eachdict)
    datab = get_db()
    cursor = datab.cursor()
    cursor.execute("delete from enabled;")
    for eachdict in flask.request.json:
        cursor.execute("INSERT into enabled (roomclass) values (?)", (eachdict,) )
    datab.commit()   
    return "updated"


@app.route('/setting/class/list',methods=['GET'])
def class_list():
    if not "loggedin" in flask.session:
          flash.redirect(flask.url_for("login"))
    datab = get_db()
    cursor = datab.cursor()
    classes = cursor.execute("select * from classes;").fetchall()
    #print(classes)
    response = flask.render_template('classes.html', classes=classes)
    return response

@app.route('/setting/class/update',methods=['POST'])
def class_edit():
    if not "loggedin" in flask.session:
        flash.redirect(flask.url_for("login"))
    print("receiving new class")
    postdata = dict( [ (eachjson['name'], eachjson['value'].upper()) for eachjson in flask.request.json])
    datab = get_db()
    cursor = datab.cursor()
    cursor.execute("insert or replace into classes (class,interface,addresses) values (?,?,?)", (postdata['classname'].upper(),postdata['interface'],postdata['addresses']) )
    datab.commit()
    for eachdict in flask.request.json:
        print(eachdict)
    return ""
          
@app.route('/setting/class/delete',methods=['POST'])
def class_delete():
    if not "loggedin" in flask.session:
          flash.redirect(flask.url_for("login"))
    tgt_class = flask.request.json
    datab = get_db()
    cursor = datab.cursor()
    cursor.execute("delete from classes where class =  ?", (tgt_class,) )
    datab.commit()
    return "Success"


@app.route('/setting/room/update',methods=['POST'])
def room_edit():
    if not "loggedin" in flask.session:
        flash.redirect(flask.url_for("login"))
    print("receiving new class")
    postdata = dict( [ (eachjson['name'], eachjson['value'].upper()) for eachjson in flask.request.json])
    datab = get_db()
    cursor = datab.cursor()
    cursor.execute("insert or replace into rooms (room,subnet) values (?,?)", (postdata['roomname'].upper(),postdata['subnet']) )
    datab.commit()
    for eachdict in flask.request.json:
        print(eachdict)
    return ""
          
@app.route('/setting/room/delete',methods=['POST'])
def rooom_delete():
    if not "loggedin" in flask.session:
          flash.redirect(flask.url_for("login"))
    tgt_room = flask.request.json
    datab = get_db()
    cursor = datab.cursor()
    cursor.execute("delete from rooms where room =  ?", (tgt_room,) )
    datab.commit()
    return "Success"

@app.route('/setting/room/list',methods=['GET'])
def room_list():
    if not "loggedin" in flask.session:
          flash.redirect(flask.url_for("login"))
    datab = get_db()
    cursor = datab.cursor()
    rooms = cursor.execute("select * from rooms;").fetchall()
    print(rooms)
    response = flask.render_template('rooms.html', rooms=rooms)
    return response


if __name__ == "__main__":
    app.run(port=8000, debug=True)
