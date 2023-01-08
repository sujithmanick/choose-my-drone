from flask import Flask,make_response,redirect,url_for,flash
from flask import session
import math
from flask.globals import request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
import smtplib, ssl
from datetime import datetime
import calendar
from pytz import timezone
from tzlocal import get_localzone
import os
import time

os.environ["TZ"] = "Asia/Calcutta"
time.tzset()
format = "%Y-%m-%d %H:%M:%S"
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = "app_secret_key"

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="choosemydrone",
    password="SQL_Password",
    hostname="choosemydrone.mysql.pythonanywhere-services.com",
    databasename=" choosemydrone$team_cmd",
)

'''SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="password",
    hostname="localhost:3306",
    databasename="mk",
)'''
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class user97(db.Model):
    __tablename__ = 'login'
    id =db.Column(db.Integer,db.Sequence('mukesh',start=1),primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    pass1 = db.Column(db.String(80))
class user98(db.Model):
    __tablename__ = 'analysis'
    email = db.Column(db.String(120))
    id =db.Column(db.Integer,db.Sequence('mukesh',start=1),primary_key=True)
    Max_Output_Power=db.Column(db.String(80))
    Input_Power_In_watts=db.Column(db.String(80))
    Output_Power_In_watts = db.Column(db.String(80))
    Motor_Rpm=db.Column(db.String(80))
    Static_Efficiency=db.Column(db.String(80))
    Volts_to_Motor=db.Column(db.String(80))
    Maximum_efficiency=db.Column(db.String(80))
    Propeller_Static_RPM=db.Column(db.String(80))
    Static_Pitch_Speed=db.Column(db.String(80))
    time = db.Column(db.String(80))
    o_date=db.Column(db.String(80))
class user99(db.Model):
    __tablename__ = 'design'
    email = db.Column(db.String(120))
    id =db.Column(db.Integer,db.Sequence('cmd',start=1),primary_key=True)
    Input_Power_In_watts=db.Column(db.String(80))
    Output_Power_In_watts = db.Column(db.String(80))
    Motor_Rpm=db.Column(db.String(80))
    Static_Efficiency=db.Column(db.String(80))
    Volts_to_Motor=db.Column(db.String(80))
    Maximum_efficiency=db.Column(db.String(80))
    Propeller_Static_RPM=db.Column(db.String(80))
    Static_Pitch_Speed=db.Column(db.String(80))
    Static_Thrust_in_g=db.Column(db.String(80))
    Prop_Static_Tip_Speed=db.Column(db.String(80))
    time = db.Column(db.String(80))
    o_date=db.Column(db.String(80))
class user100(db.Model):
    __tablename__ = 'newwe'
    id =db.Column(db.Integer,db.Sequence('seq_book',start=1001),primary_key=True)
    ip = db.Column(db.String(80))
    info = db.Column(db.String(420))
    time=db.Column(db.String(80))
    date=db.Column(db.String(80))
    mon=db.Column(db.String(80))
    year=db.Column(db.String(80))
    count=db.Column(db.String(80))


@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.xml')


@app.route('/home')
@app.route('/')
def index():
    now_utc = datetime.now(timezone('UTC'))
    now_local = now_utc.astimezone(get_localzone())
    li=now_local.strftime(format)
    li=li.split(' ')
    cal=li[0].split('-')
    time=li[1]
    mon=calendar.month_name[int(cal[1])]
    year=cal[0]
    date=cal[2]
    i_p=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    i_p=str(i_p)
    in_fo=request.headers.get('User-Agent')
    try:
        data = user100.query.filter_by(info=in_fo).first()
        if data:
            c=int(data.count)+1
            data.count=c
            data.time=time
            data.year=year
            data.date=date
            data.ip=i_p
            db.session.commit()
        else:
            register= user100(ip =i_p,info=in_fo, time=time,date=date,mon=mon,year=year,count=0)
            db.session.add(register)
            db.session.commit()

    except:
        pass
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("index.html",a='LOGIN',b='/login')
    else:
        d= user97.query.filter_by(email=session['email']).first()
        if d is None:
            flash("Error Came cookies override")
            return redirect(url_for('login'))
        else:
            return render_template('index.html',a=d.username,b='/database')
@app.route('/load1')
def data1():
    dd= user99.query.filter_by(email=session['email']).all()
    ddd= user98.query.filter_by(email=session['email']).all()
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("design_data.html",a='Login/signup',b='/login',ls=dd)
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('design_data.html',a=d.username,b='/database',ls=dd,analysis=ddd)
    return render_template('design_data.html')

@app.route('/visitor')
def mukeshdata1():
    d=user100.query.all()
    return render_template("visitor_data.html",books=d)

@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method=='GET':
        return render_template('login.html')
    elif request.method=='POST':
        session['email']=request.form['email']
        session['pass']=request.form['pass']
        try:
            d= user97.query.filter_by(email=session['email']).first()
            if d.email==session['email'] and d.pass1==session['pass']:
                resp = make_response(render_template('index.html',a=d.username,b='/database'))
                resp.set_cookie('email',session['email'],max_age=60*60*24*360)
                resp.set_cookie('pass',session['pass'],max_age=60*60*24*360)
                return resp
            elif d.email==session['email'] and d.pass1!=session['pass']:
                flash("Password Wrong")
                return redirect(url_for('login'))
            else:
                flash("No Account Found Please Register")
                return redirect(url_for('signup'))
        except:
            flash("No Account Found Please Register")
            return redirect(url_for('signup'))

@app.route('/signup',methods = ["POST","GET"])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        session['u_name']=request.form['u_name']
        session['u_email']=request.form['u_email']
        session['u_pass']=request.form['u_pass']
        ab = user97.query.filter_by(email=session['u_email']).first()
        if ab is None:
            try:
                register= user97(username =session['u_name'], email = session['u_email'] ,pass1 =session['u_pass'])
                db.session.add(register)
                db.session.commit()
                flash("New Account Created")
                return redirect(url_for('login'))
            except:
                flash("Please Try again later!! some database server error came")
                return redirect(url_for('signup'))
        else:
            flash("Account Already Found In our Database")
            return redirect(url_for('signup'))

@app.route('/forget')
def forget():
    return render_template('forget.html')
@app.route('/ff',methods = ["POST"])
def ff():
    if request.method=='POST':
        session['f_email']=request.form['f_email']
        try:
                d= user97.query.filter_by(email=session['f_email']).first()
                if d.email==session['f_email']:
                    flash("Your Password is "+d.pass1)
                    return redirect(url_for('login'))
                else:
                    flash("No Account Found Please Register")
                    return redirect(url_for('signup'))
        except:
            flash("No Account Found Please Register")
            return redirect(url_for('signup'))
    else:
        return redirect(url_for('forget'))

@app.route('/database')
def database():
    try:
        d= user97.query.filter_by(email=session['email']).first()
        return render_template('d1.html',a=d.username)
    except:
        return render_template("index.html",a='LOGIN',b='/login')
@app.route('/logout')
def delete_cookie():
    res= make_response(redirect(url_for('index')))
    res.delete_cookie("email")
    res.delete_cookie("pass")
    return res


def battery_s(a,b,c,d):
    da = [
        ['A123 - 2300 LiNP 15/20C',        2300,   .009,     2.54,    3.3,     46],
        ['AnyRc Lipo 1700',                1700,   .06,      1.4,     3.7,	0],
        ['Apogee 830',                      850,   .012,     .61,     3.7,      0],
        ['Apogee 1050',                    1050,   .012,     .76,     3.7,	0],
        ['Apogee 1570',                    1570,   .012,     1.27,    3.7,	0],
        ['Apogee 2480',                    2480,   .012,     1.67,    3.7,	0],
        ['BlackLine 1700 35C',             1700,   .0089,     1.16,   3.7,     60],
        ['BlackLine 2200 35C',             2200,   .0071,     2.05,   3.7,     77],
        ['BlackLine 2600 35C',             2600,   .0058,     2.47,   3.7,     91],
        ['BlackLine 3200 35C',             3200,   .0048,     3.39,   3.7,    112],
        ['BlackLine 3800 35C',             3800,   .0038,     3.60,   3.7,    133],
        ['BlackLine 4400 35C',             4400,   .0033,     4.31,   3.7,    154],
        ['Dualsky XPower 1000 16C',        1000,   .035,      0.92,   3.7,     33],
        ['Dualsky XPower 1000 25C',        1000,   .030,      1.06,   3.7,     25],
        ['Dualsky XPower 2200 25C',        1000,   .009,      1.94,   3.7,     55],
        ['Dualsky XPower 2200 16C',        2200,   .013,      1.77,   3.7,     33],

        ['Dymond XS-1350 22C',             1350,   .017,      2.73,   3.7,     31],
        ['Dymond XS-1700 22C',             1700,   .015,      1.73,   3.7,     38],
        ['Dymond XC-2250 22C',             2250,   .0148,     2.26,   3.7,     38],
        ['Dymond ZC-2500 30C',             2500,   .0065,     2.4,    3.7,     60],
        ['Dymond XC-3200 30C',              3200,  .006,      3.32,   3.7,     80],
        ['ePower 450 15/20C',               450,   .0276,    .353,    3.7,	9],
        ['ePower 700 12/18C',               700,   .0336,    .493,    3.7,     12],
        ['ePower 1000HP 10/16C',           1000,   .044,     .847,    3.7,     16],
        ['ePower 1000HPT 12/18C',          1000,   .015,     .883,    3.7,     18],
        ['ePower 1200XP 15/25C',           1200,   .015,     1.01,    3.7,     30],
        ['ePower 1250HPT 12/15C',          1250,   .015,     .953,    3.7,     19],
        ['ePower 1500XP 15/25C',           1500,   .012,     1.34,    3.7,     38],
        ['ePower 1700HP 10/15C',           1700,   .025,     1.34,    3.7,     26],
        ['ePower 1800XP 15/25C',           1800,   .01,      1.586,   3.7,     45],
        ['ePower 2500XP 15/25C',           2500,   .0096,    2.256,   3.7,     63],
        ['ePower 3700XP 15/25C',           3700,   .0049,    3.35,    3.7,     93],
        ['ePower 5000XP 15/25C',           5000,   .0032,    4.234,   3.7,    125],
        ['E-Tec ET-0250',                   250,   .09,      .2,      3.7,	0],
        ['E-Tec ET-0700',                   700,   .042,     .53,     3.7,	0],
        ['E-Tec ET-1200',                  1200,   .033,     .85,     3.7,	0],
        ['E-Tec ET-1200HD',                1200,   .032,     .93,     3.7,	0],
        ['FlightPower 400 20C',	            400,   .0037,    .65,     3.7,	8],
        ['FlightPower 800 20C',	            800,   .0023,    .85,     3.7,     16],
        ['FlightPower 1200 20C',	   1200,   .0125,    1.27,    3.7,     24],
        ['FlightPower 1500 20C',	   1500,   .0098,    1.27,    3.7,     30],
        ['FlightPower 1800 20C',	   1800,   .0063,    1.71,    3.7,     36],
        ['FlightPower 2100 20C',	   2100,   .01,      2.24,    3.7,     42],
        ['FlightPower 2500 20C',	   2500,   .0065,    2.51,    3.7,     50],
        ['FlightPower 3300 20C',	   3300,   .0038,    3.34,    3.7,     66],
        ['FlightPower 3700 20C',	   3700,   .0037,    3.5,     3.7,     74],
        ['Gold Peak GP750 NiMH',	    750,   .06,       .5,    1.25,	0],
        ['Gold Peak GP3300 NiMH 12C',	   3300,   .005,     2.19,   1.25,     40],
        ['Gold Peak GP3700 NiMH 12C',	   3700,   .005,     2.4,    1.25,     45],
        ['G. Planes Electrifly 300 20C',    300,   .06,       .28,    3.7,	6],
        ['G. Planes Electrifly 640 20C',    640,   .022,      .6,     3.7,     13],
        ['G. Planes Electrifly 910 20C',    910,   .018,      .88,    3.7,     18],
        ['G. Planes Electrifly 1250 20C',  1250,   .0115,    1.02,    3.7,     25],
        ['G. Planes Electrifly 1500 20C',  1500,   .011,     1.23,    3.7,     30],
        ['G. Planes Electrifly 2100 20C',  2100,   .0075,    1.83,    3.7,     42],
        ['G. Planes Electrifly 3200 20C',  3200,   .0045,    2.75,    3.7,     64],
        ['G. Planes Electrifly 5000 20C',  5000,   .003,     4.3,     3.7,    100],
        ['Hecell HE23AF 1050 NiMH',        1050,   .025,      .71,   1.25,	0],
        ['Hecellusa 1100 NiMH',            1100,    .01,      .7,    1.25,	0],
        ['Hyperion HP-LVX 0300 20C',        300,   .056,      .32,    3.7,	6],
        ['Hyperion HP-LCL 0350 26C',        350,   .073,      .4,     3.7,	9],
        ['Hyperion HP-LVX 0400 20C',        400,   .042,      .46,    3.7,	8],
        ['Hyperion HP-LVX 0800 20C',        800,   .021,      .53,    3.7,     16],
        ['Hyperion HP-LCL 0950 25C',        950,   .027,      .98,    3.7,     24],
        ['Hyperion HP-LVX 1200 20C',       1200,   .014,      1.13,   3.7,     24],
        ['Hyperion HP-LVX 1500 20C',       1500,   .011,      1.34,   3.7,     30],
        ['Hyperion HP-LVX 1800 20C',       1800,   .0093,     1.5,    3.7,     36],
        ['Hyperion HP-LVX 2000 20C',       2000,   .0084,     1.64,   3.7,     40],
        ['Hyperion HP-LVX 2100 20C',       2100,   .008,      1.88,   3.7,     42],
        ['Hyperion HP-LCL 2100 16C',       2100,   .012,      1.43,   3.7,     34],
        ['Hyperion HP-LVX 2200 20C',       2200,   .0076,     1.98,   3.7,     44],
        ['Hyperion HP-LVX 2500 20C',       2500,   .0067,     2.17,   3.7,     50],
        ['Hyperion HP-LVX 3300 20C',       3300,   .0005,     2.89,   3.7,     66],
        ['Hyperion HP-LVX 3700 20C',       3700,   .0045,     3.16,   3.7,     74],
        ['Hyperion HP-LVX 4350 20C',       4350,   .0038,     3.69,   3.7,     87],
        ['Hyperion HP-LCL 4000 20C',       2100,   .0064,    3.65,    3.7,     80],
        ['Hyperion HP-LCL 4200 16C',       4200,   .0061,    3.2,     3.7,     67],
        ['Hyperion HP-LCL 4800 20C',       4800,   .0053,    4.32,    3.7,     96],
        ['Hyperion HP-LVX 5000 20C',       5000,   .0033,    4.3,     3.7,    100],
        ['Kokam 145 8C',		    145,   .019,     .12,     3.7,    1.2],
        ['Kokam 340',                       340,   .02,      .36,     3.7,	0],
        ['Kokam 360SHD 20C',                360,   .0688,    .39,     3.7,    7.2],
        ['Kokam 630',                       630,   .04,      .58,     3.7,	0],
        ['Kokam 640SHD 15C',                640,   .044,     .6,      3.7,    9.6],
        ['Kokam 730SHD 20C',                730,   .0257,    .74,     3.7,     15],
        ['Kokam 910SHD 15C',                920,   .0275,    .81,     3.7,     14],
        ['Kokam 1020',                     1020,   .06,      .72,     3.7,	0],
        ['Kokam 1100 5C',		   1100,   .02,      11.1,    3.7,    5.5],
        ['Kokam 1200 2C',		   1200,   .06,      .82,     3.7,    4.2],
        ['Kokam 1250 15C', 		   1250,   .012,     1.16,    3.7,     19],
        ['Kokam 1250 20C',		   1250,   .027,     1.26,    3.7,     25],
        ['Kokam 1500',		           1500,   .027,     1.15,    3.7,	0],
        ['Kokam 1500 10C',		   1500,   .017,     1.15,    3.7,     15],
        ['Kokam 1500 2S',                  1500,   .015,     1.24,    3.7,	0],
        ['Kokam 1500 8/16C',               1500,   .019,     1.15,    3.7,     24],
        ['Kokam 2000 10C',		   2000,   .017,     1.62,    3.7,     20],
        ['Kokam 2000 15/30C',              2000,   .012,     1.79,    3.7,     60],
        ['Kokam 2000SHD 15C',              2000,   .0178,    1.84,    3.7,     30],
        ['Kokam 2100 20/40C',		   2100,   .01,      2.41,    3.7,     84],
        ['Kokam 2100SHD 20C',              2100,   .0114,    2.37,    3.7,     42],
        ['Kokam 3100 5C',		   3100,   .02,      3.03,    3.7,     16],
        ['Kokam 3200 20C', 		   3200,   .01,      2.91,    3.7,     64],
        ['Kokam 3200SHD 20C',	           3200,   .008,     2.83,    3.7,     64],
        ['Kokam 3200H5 25C',	           3200,   .004,     3.14,    3.7,     80],
        ['Kokam 4000H 20C',	           4000,   .0025,    3.67,    3.7,     80],
        ['Kokam 4000H5 20/25C',	           4000,   .0025,    3.67,    3.7,    100],
        ['Kokam 4800H 15C',	           4000,   .0034,    4.06,    3.7,     75],
        ['Kokam 5000H 25C',	           5000,   .0025,    4.59,    3.7,    125],
        ['Lipoly.de 1800',                 1800,   .0183,    1.45,    3.7,	0],
        ['LiteStorm  350CL 20/30C',	    350,   .028,     .46,     3.7,   10.5],
        ['LiteStorm  950CL 20/30C',	    950,   .0145,    .917,    3.7,     29],
        ['LiteStorm 1200VX 20/25C',	   1200,   .015,     1.165,   3.7,     30],
        ['LiteStorm 1600CL 20/30C',	   1600,   .0113,    1.305,   3.7,     48],
        ['LiteStorm 2100CL 16/22C',	   2100,   .01,	     1.587,   3.7,     46],
        ['LiteStorm 2100VX 20/25C',	   2100,   .01,	     1.975,   3.7,     53],
        ['LiteStorm 2200VX 20/25C',	   2200,   .009,     2.045,   3.7,     55],
        ['LiteStorm 2500CL 20/30C',	   2500,   .008,     2.221,   3.7,     75],
        ['LiteStorm 2500VX 20/25C',	   2500,   .007,     2.224,   3.7,     63],
        ['LiteStorm 3200CL 20/30C',	   3200,   .0075,    2.892,   3.7,     96],
        ['LiteStorm 4000CL 20/30C',	   4000,   .0045,    3.705,   3.7,    120],
        ['LiteStorm 4350VX 20/25C',	   4350,   .0042,    3.88,    3.7,    109],
        ['LiteStorm 4800CL 20/30C',	   4800,   .0042,    4.41,    3.7,    144],
        ['LiteStorm 5000VX 20/25C',	   5000,   .0032,    4.445,   3.7,    125],
        ['Litronics 2200 25C',	           2200,   .0087,    1.98,     3.7,    44],
        ['Litronics 2500 25C',	           2200,   .007,     2.37,     3.7,    50],
        ['Litronics 3200 25C',	           3200,   .0055,    3.18,     3.7,    64],
        ['Litronics 5000 22C',	           5000,   .0038,    4.45,     3.7,   100],
        ['Panasonic 2000 NiMH',            1950,   .0055,    1.48,   1.25,	0],
        ['Panasonic 3000 NiMH',            2900,   .0055,    2.01,   1.25,	0],
        ['Panasonic 3000 Sq NiMH',         3300,   .0055,    2.43,   1.25,	0],
        ['Panasonic HHR150AA',             1500,   .02,      .92,    1.25,	0],
        ['Panasonic HHR300SCU',            3000,   .004,     1.94,   1.25,	0],

        ['Panasonic NCR18650GA 3500',      3500,   .025,     1.67,    3.7,     10],
        ['Panasonic NCR20700B  4250',      3500,   .020,     2.24,    3.7,     15],

        ['Poly-Quest 300',                  300,   .216,     .3,      3.7,	0],
        ['Poly-Quest 300XP 20C',            300,   .098,     .32,     3.7,	6],
        ['Poly-Quest 400XP 15C',            400,   .075,     .49,     3.7,	6],
        ['Poly-Quest 800XP 13C',            800,   .038,     .78,     3.7,     10],
        ['Poly-Quest 880',                  880,   .0813,    .64,     3.7,	0],
        ['Poly-Quest 1200XP 15C',          1200,   .018,     .99,     3.7,     18],
        ['Poly-Quest 1800',                1800,   .0287,    1.48,    3.7,	0],
        ['Poly-Quest 1800XP 15C',          1800,   .012,     1.45,    3.7,     27],
        ['Poly-Quest 2000XQ 20C',          2000,   .006,     1.87,    3.7,     40],
        ['Poly-Quest 2100XP 15C',          2100,   .012,     1.66,    3.7,     32],
        ['Poly-Quest 2150XP 15C',          2150,   .010,     1.84,    3.7,     32],
        ['Poly-Quest 2500XP 15C',          2500,   .0085,    2.12,    3.7,     38],
        ['Poly-Quest 2600',                2600,   .0221,    1.92,    3.7,	0],
        ['Poly-Quest 3200XQ 20C',          3200,   .004,     3.07,    3.7,     64],
        ['Poly-Quest 3300XP 15C',          3300,   .006,     2.68,    3.7,     50],
        ['Poly-Quest 3500',	           3500,   .0108,    2.86,    3.7,	0],
        ['Poly-Quest 3700XP 15C',          3700,   .0055,    3.0,     3.7,     56],
        ['Poly-Quest 3800Mn 15C',          3800,   .0041,    3.71,    3.7,     57],
        ['Poly-Quest 4400',                4400,   .0107,    3.15,    3.7,	0],
        ['Poly-Quest 4500XQ 20C',          4500,   .0035,    4.41,    3.7,     90],
        ['Poly-Quest 5000XP 15C',          5000,   .0026,    4.59,    3.7,     75],
        ['Poly-Quest 6000XP 15C',          6000,   .0024,    6.14,    3.7,     90],
        ['Radio Shack 700 NiMH',           750,    .03,      .46,    1.25,	0],
        ['Radio Shack 1420 NiMH',         1380,   .0235,    .85,     1.25,	0],
        ['Radio Shack 1800 NiMH',         1800,   .022,     .92,     1.25,	0],
        ['Rhino 1750 25C',                1750,   .015,     1.64,    3.7,      44],
        ['Rhino 2150 20C',                2150,   .009,     2.12,    3.7,      43],
        ['Rhino 2350 20C',                2350,   .006,     2.37,    3.7,      69],
        ['RockAmp ACF3 1700 30C',         1700,   .0085,    1.55,    3.7,      51],
        ['RockAmp ACF3 2200 30C',         2200,   .0068,    2.05,    3.7,      66],
        ['RockAmp ACF3 2500 30C',         2500,   .0059,    2.29,    3.7,      75],
        ['RockAmp ACF3 4400 30C',         4400,   .0038,    4.24,    3.7,     110],
        ['Saft 3000 NiMH',                2600,   .009,     2.05,    1.25,	0],

        ['Sanyo 50AAA',                     50,   .055,     .14,     1.25,	0],
        ['Sanyo 110AA',                    110,   .03,      .25,     1.25,	0],
        ['Sanyo 250AAA',                   250,   .024,     .39,     1.25,	0],
        ['Sanyo 270AA',                    270,   .015,     .49,     1.25,	0],
        ['Sanyo 500AR',                    500,   .009,     .67,     1.25,	0],
        ['Sanyo 600AA',                    600,   .012,     .81,     1.25,	0],
        ['Sanyo 600AE',                    600,   .01,      .63,     1.25,	0],
        ['Sanyo 700AR',                    700,   .007,     .99,     1.25,	0],
        ['Sanyo 720AAA NiMH',              720,   .04,      .44,     1.25,	0],
        ['Sanyo 800AR',                    800,   .006,     1.17,    1.25,	0],
        ['Sanyo 1000AE',                  1000,   .008,     1.09,    1.25,	0],
        ['Sanyo 1000AAU',                 1000,   .018,     .81,     1.25,	0],
        ['Sanyo 1000SCR',                 1000,   .0045,    1.48,    1.25,	0],
        ['Sanyo 1100AAE',                 1100,   .0135,    1.17,    1.25,	0],
        ['Sanyo 1100AE',                  1100,   .009,     .99,     1.25,	0],
        ['Sanyo 1100SCR',                 1100,   .0043,    1.52,    1.25,	0],
        ['Sanyo 1250SCR',                 1250,   .005,     1.5,     1.25,	0],
        ['Sanyo CP-1300SCR',      	  1300,   .0074,    1.16,    1.25,	0],
        ['Sanyo 1400AE',                  1400,   .0115,    1.09,    1.25,	0],
        ['Sanyo 1400SCR',                 1400,   .004,     1.86,    1.25,	0],
        ['Sanyo 1700SCR',                 1700,   .004,     1.89,    1.25,	0],
        ['Sanyo 1700SCRC',                1700,   .004,     1.91,    1.25,	0],
        ['Sanyo 1900SCR',                 1900,   .004,     1.96,    1.25,	0],
        ['Sanyo RC2000',                  2000,   .0035,    1.99,    1.25,	0],
        ['Sanyo 2000SCR',                 2000,   .004,     2.05,    1.25,	0],
        ['Sanyo 2200 NiMH',               2000,   .006,     1.4,     1.25,	0],
        ['Sanyo RC2400',                  2400,   .0032,    2.08,    1.25,	0],
        ['Sanyo CP-2400SCR',              2300,   .0053,    2.05,    1.25,	0],
        ['Sanyo 3000CR',                  3000,   .0032,    2.96,    1.25,	0],
        ['Sanyo RC3000 NiMH',             3000,   .0035,    2.08,    1.25,	0],


        ['Tadiran Lithium-Metal',          800,   .08,       .6,     1.25,	0],
        ['Tanic 350',                      350,   .070,      .42,     3.7,	0],
        ['Tanic 470',                      470,   .040,      .44,     3.7,	0],
        ['Tanic 520',                      520,   .018,      .39,     3.7,	0],
        ['Tanic 830',                      830,   .053,      .64,     3.7,	0],
        ['Tanic 780',                      780,   .022,      .71,     3.7,	0],
        ['Tanic 1050',                    1050,   .041,      .78,     3.7,	0],
        ['Tanic 1550',                    1550,   .0301,    1.17,     3.7,	0],
        ['Tanic 2150',                    2150,   .0228,    1.52,     3.7,	0],
        ['Tanic 2200',                    2200,   .012,     1.45,     3.7,	0],
        ['Tanic 2220',                    2220,   .0195,    1.52,     3.7,	0],
        ['Tanic 2450',                    2450,   .019,     1.7,      3.7,	0],
        ['Tanic 2500',                    2500,   .018,     1.84,     3.7,	0],
        ['Tanic 3650',                    3650,   .0055,    3.21,     3.7,	0],
        ['Tanic 5000',                    5000,   .0026,    4.59,     3.7,	0],
        ['ThunderPower 480 12/16C',	   480,   .03,      .387,     3.7,	8],
        ['ThunderPower 730 12/16C',	   730,   .0164,     .53,     3.7,     12],
        ['ThunderPower 900 12/16C',	   900,   .03,      .705,     3.7,     15],
        ['ThunderPower 1320 13/20C',	  1320,   .03,      .987,     3.7,     27],
        ['ThunderPower 2100 15/20C',	  2100,   .0086,   1.624,     3.7,     42],
        ['ThunderPower 2070SX 25/50C',	  2070,   .0084,    1.87,     3.7,    104],
        ['ThunderPower 3850SXL 22/50C',   3850,   .0032,    3.35,     3.7,    193],
        ['ThunderPower 5000SX 22/50C',	  5000,   .0026,   4.305,     3.7,    250],
        ['Turnigy nano-tech 460 25/40C',   460,   .011,     .58,      3.7,     12],
        ['Turnigy nano-tech 800 25/40C',   800,   .01,    2.26,      3.7,      32],
        ['Turnigy nano-tech 850 25/40C',   850,   .0012,   .81,      3.7,      21],
        ['Turnigy nano-tech 1300 25/50C', 1300,   .0012,    1.52,     3.7,     26],
        ['Turnigy nano-tech 2200 25C',	  2200,   .0015,     6.6,     3.7,     55],
        ['Turnigy nano-tech 4000 25C',	  4000,     .0012,  3.88,     3.7,    100],
        ['Turnigy 1000 15C',		  1000,    .008,   2.26,      3.7,     15],
        ['Turnigy 1000 25C',		  1000,    .0061,    1.1,      3.7,    25],
        ['Turnigy 1600 20/30C',		  1600,    .0057,   1.98,      3.7,    32],
        ['Turnigy 1800 20C',		  1800,    .01,      1.86,     3.7,    36],
        ['Turnigy 1800 30C',		  1800,    .005,    1.85,      3.7,    54],
        ['Turnigy 2200 35C',		  2200,    .003,    2.33,      3.7,    77],
        ['Turnigy 3000 20C',		  3000,    .01,     2.98,      3.7,    60],
        ['Turnigy 3600 20C',		  3600,    .01,     3.53,      3.7,    72],
        ['Turnigy 4000 20/30C',		  4000,    .006,    4.02,      3.7,    80],
        ['Turnigy 4000 30/40C',		  4000,    .006,    3.99,      3.7,   120],
        ['Turnigy 5000 40C',		  5000,    .005,    5.1,       3.7,   200],
        ['ZIPPY Flightmax 2650 40C',      2650,    .006,    2.82,      3.7,   106],
        ['ZIPPY Flightmax 4000 20C',      4000,    .006,    3.53,      3.7,    80],
        ['ZIPPY Flightmax 5000 20C',      5000,    .005,    3.53,      3.7,   100],
        ['ZIPPY H2100 30/40C',            2100,    .0082,   2.22,      3.7,    53],
        ['ZIPPY H2200 20/30C',            2200,    .01,     1.91,      3.7,    44],
        ['ZIPPY H3300 20/30C',            3300,    .0065,   3.04,      3.7,    50],
        ['ZIPPY H4400 15/20C',            4400,    .0057,   4.84,      3.7,    66],
        ['ZIPPY H5800 30/40C',            5800,    .0033,   4.94,      3.7,   174]
        ]
##        session['battery_mah']=request.form['mah'] a
##        session['battery_maxv']=request.form['maxv'] b
##        session['battery_weight']=request.form['maxw'] c
##        session['battery_amp']=request.form['c_amp'] d
    mah=a
    current=b
    volt=c
    weight=d
    c=[]
    for i in da:
        if i[1]<=mah:
            if weight<=i[3]:
                if i[4]<=volt:
                    if i[5]<=current:
                        c.append(i)
    return c
def propeller_s(a,b,c):
    d=[['Aeronaut 6x5 fixed E-prop',		.90,	.70,	6,	5,	2],
        ['Aeronaut 6.5x4 fixed E-prop',	        .84,	.68,	6.5,	4,	2],
        ['Aeronaut 7x7 fixed E-prop',	        .90,	.82,	7,	7,	2],
        ['Aeronaut 8.5x5 fixed E-prop',	        .66,	.53,	8.5,	5,	2],
        ['Aeronaut 8.5x6 fixed E-prop',	        .78,	.60,	8.5,	6,	2],
        ['Aeronaut 8.5x7 fixed E-prop',	        .89,	.70,	8.5,	7,	2],
        ['Aeronaut 9x5 fixed E-prop',	        1.1,	.98,	9,	5,	2],
        ['Aeronaut 9.5x5 fixed E-prop',	        .86,	.62,	9.5,	5,	2],
        ['Aeronaut 9.5x6 fixed E-prop',          .8,	.63,	9.5,	6,	2],
        ['Aeronaut 9.5x7 fixed E-prop',         .85,	.68,	9.5,	7,	2],
        ['Aeronaut 10x6 fixed E-prop',	        .78,	.62,	10,	6,	2],
        ['Aeronaut 10x7 fixed E-prop',	        .97,	.65,	10,	7,	2],
        ['Aeronaut 10x8 fixed E-prop',	        1.0,	.84,	10,	8,	2],
        ['Aeronaut 12x7 C Fold 42',	        .71,	.49,	12,	7,	2],
        ['Aeronaut 13x6.5 C Fold 42',	        .91,	.44,	13,   	6.5,	2],
        ['Aeronaut 13.5x7 C Fold 42',	        .73,	.44,	13.5,  	 7,	2],
        ['Aeronaut 14x7 C Fold 42',	        .74,	.62,	14,     7,	2],
        ['Aeronaut 8x5 CAM Fold 42',	        .81,	.72,	8,	5,	2],
        ['Aeronaut 9x5 CAM Fold 42',	        .77,	.70,	9,	5,	2],
        ['Aeronaut 9x7 CAM Fold 42',	        .80,	.81,	9,	7,	2],
        ['Aeronaut 9.5x5 CAM Fold 42', 	        .89,	.72,	9.5,	5,	2],
        ['Aeronaut 10x6 CAM Fold 42',	        .69,	.54,	10,	6,	2],
        ['Aeronaut 11x6 CAM Fold 42',	        .93,	.71,	11,	6,	2],
        ['Aeronaut 11x7 CAM Fold 42',	        .77,	.60,	11,	7,	2],
        ['Aeronaut 11x8 CAM Fold 42',	        .78,	.59,	11,	8,	2],
        ['Aeronaut 12x8 CAM Fold 42',	        .84,	.64,	12,	8,	2],
        ['Aeronaut 12x9 CAM Fold 42',	        .89,	.67,	12,	9,	2],
        ['Aeronaut 13x8 CAM Fold 42',	        .70,	.52,	13,	8,	2],
        ['Aeronaut 13x11 CAM Fold 42',	        .79,	.59,	13,    	11,	2],
        ['Aeronaut 14x8 CAM Fold 42',	        .94,	.74,	14,    	 8,	2],
        ['Align 5x3',			        .67,	.54,	5,	3,	2],
        ['Align 4.2x2',	       		       1.15,	.94,	4.2,	2,	2],
        ['APC E 4.1x4.1',      	               1.10,	.96,	4.1,  	4.1,	2],
        ['APC E 4.5x4.1',      	       	       1.09,	.94,	4.5,  	4.1,	2],
        ['APC E 4.7x4.2',			.95,	.81,	4.7,  	4.2,	2],
        ['APC E 4.75x4.5',		       1.05,	1.0,	4.75,  	4.5,	2],
        ['APC E 4.75x4.75',		        1.0,    .87,   	4.75, 	4.75,	2],
        ['APC E 4.75x5.5',		       1.05,    1.0,   	4.75,  	5.5,	2],
        ['APC E 5x5',			        .88,	.93,	5,	5,	2],
        ['APC E 5.25x4.75',		        .90,	.84,   	5.25, 	4.75,	2],
        ['APC E 5.5x4.5',     		        .87,	.85,   	5.5,   	4.5,	2],
        ['APC E 6x4',			        .88,	.73,	6,	4,	2],
        ['APC E 6x5.5',			        .98,	.84,	6,    	5.5,	2],
        ['APC E 7x4',	       		        .77,	.84,	7,	4,	2],
        ['APC E 7x5',	       		        1.1,	.83,	7,	5,	2],
        ['APC E 8x4',	       		       1.02,	.85,	8,	4,	2],
        ['APC E 8x6',	       		        1.1,   	1.02,	8,	6,	2],
        ['APC E 8x8',	       		       1.15,  	1.11,	8,	8,	2],
        ['APC E 9x4.5',	       		       1.01,	.78,	9,    	4.5,	2],
        ['APC E 9x6',			        .98,	.75,	9,	6,	2],
        ['APC E 9x7.5',			       1.08,	.95,	9,    	7.5,	2],
        ['APC E 9x9',			       1.03,	1.0,	9,    	9,	2],
        ['APC E 10x5',			        .97,	.74,   	10,     5,	2],
        ['APC E 10x7',          		.92,	.71,   	10,	7,	2],
        ['APC E 11x5.5',			.92,	.72,   	11,    	5.5,	2],
        ['APC E 11x7',	        		.88,	.69,   	11,	7,	2],
        ['APC E 11x8',          		.86,    .81,   	11,	8,	2],
        ['APC E 11x8.5',          		.90,   	.72,  	11,    	8.5,	2],
        ['APC E 12x6',			        .95,	.71,   	12,	6,	2],
        ['APC E 12x8',    			.87,	.67,   	12,	8,	2],
        ['APC E 12x12',    			.99,	.67,   	12,    	12,	2],
        ['APC E 13x4',         	       	       1.15,    .66,   	13,   	4,	2],
        ['APC E 13x6',         	        	.90,    .58,   	13,   	6,	2],
        ['APC E 13x6.5',       		        .92,    .67,   	13,    	6.5,	2],
        ['APC E 13x8',			        .87, 	.59,   	13,	8,	2],
        ['APC E 14x7',	        		.91,	.60,   	14,	7,	2],
        ['APC E 14x10',			        .88,	.63,   	14,     10,	2],
        ['APC E 15x8',			        .93,	.71,   	15,      8,	2],
        ['APC E 16x8',		               1.08,	.69,   	16,      8,	2],
        ['APC E 17x8',		        	.94,	.61,   	17,      8,	2],
        ['APC E 17x10',		        	.80,	.64,   	17,     10,	2],
        ['APC E 18x8',		       	       1.08,	.71,   	18,      8,	2],
        ['APC E 20x10',		        	.98,	.62,   	20,     10,	2],
        ['APC E 22x10',		        	.94,	.56,   	22,     10,	2],
        ['APC Sport 7x6',			1.0,	1.0,   	7,      6,	2],
        ['APC Sport 10x6',			.80,	.71,   	10,      6,	2],
        ['APC Sport 11x5',          		.98,	.68,   	11,	5,	2],
        ['APC Sport 11x6',	       		.88,	.72,   	11,	6,	2],
        ['APC Sport 11x8',          		.90,    .79,   	11,	8,	2],
        ['APC Sport 12x7',			.81,	.69,   	12,	7,	2],
        ['APC Sport 13x7',       		.84,    .62,   	13,     7,	2],
        ['APC Sport 15x8',      		.89,    .67,   	15,     8,	2],
        ['APC Sport 16x8',      		.95,    .68,   	16,     8,	2],
        ['APC Sport 16x10',      		.80,    .65,   	16,     10,	2],
        ['APC Sport 16x12',      		.85,    .67,   	16,     12,	2],
        ['APC Sport 18x6',             		1.12,   .65,   	18,      6,	2],
        ['APC SF 7x3.8',          		1.4,   1.55,     7,    3.8,	2],
        ['APC SF 7x4',          		1.03,   .95,     7,      4,	2],
        ['APC SF 7x5',          		1.07,   .95,     7,      5,	2],
        ['APC SF 7x6',          		1.25,   .93,     7,	 6,	2],
        ['APC SF 8x3.8',        		1.3,	1.17,   8,    	3.8,	2],
        ['APC SF 8x6',          		1.53,	1.45,   8,	6,	2],
        ['APC SF 9x3.8',        		1.3,	1.0,	9,    	3.8,	2],
        ['APC SF 9x4.7',        		1.1,    .85,    9,    	4.7,	2],
        ['APC SF 9x6',			        1.5,	1.25,   9,      6,	2],
        ['APC SF 10x3.8',			1.47,	1.17,  	10,    	3.8, 	2],
        ['APC SF 10x4.7',			1.4,	 .95,  	10,    	4.7,	2],
        ['APC SF 10x7',         		1.45,   1.3,   	10,      7,	2],
        ['APC SF 11x4.7',       		1.4,     .95,  	11,    	4.7,	2],
        ['APC SF 11x7',         		1.4,	1.07,  	11,      7,	2],
        ['APC SF 12x3.8',         		1.5,    1.18,  	12,    	3.8,	2],
        ['APC SF 12x6',         		1.48,    1.2,  	12,      6,	2],
        ['Dymond-E 15x8',      	        	.93,    .74,   	15,      8,	2],
        ['EM E-prop Metts 15x8',      		.90,    .70,   	15,      8,	2],
        ['EM E-prop Metts 16x7',      		.92,    .65,   	16,     7,	2],
        ['EM E-prop Metts 16x8',      		.99,    .68,   	16,      8,	2],
        ['GemFan 5x3',			        .72,	.65,	5,	3,	2],
        ['GemFan 5x4.5',		     	.90,	.65,	5,	4.5,	2],
        ['GemFan 6x3',			        .65,	.44,	6,	3,	2],
        ['Graupner CAM Speed 4.7x4.7',	       1.02,    1.1,  	4.7,   	4.7,	2],
        ['Graupner Nylon 5x2',	         	.22,    .88,    5,     	2,	2],
        ['Graupner CAM Speed 5.2x5.2',	        .96,	 .85,  	5.2,   	5.2,	2],
        ['Graupner CAM Speed 5.5x4.3',	        .82,	 .83,  	5.5,   	4.3,	2],
        ['Graupner Speed 5.5x5.5',	 	.95,	 .83,  	5.5,   	5.5,	2],
        ['Graupner Speed 6x5.5',	 	.91,	 .72,    6,   	5.5,	2],
        ['Graupner Speed 6x6',	 	        1.0,	 .74,    6,     6,	2],
        ['Graupner Speed 6.5x6.5',      	.82,     .71,  	6.5,   	6.5,	2],
        ['Graupner Speed 7x7',	 	         .8,	 .7,    7,     	7,	2],
        ['Graupner CAM Folding 8x6',	        .83,	 .75,   8,     	6,	2],
        ['Graupner CAM Folding 9x6',	 .88,	 .75,    	9,     	6,	2],
        ['Graupner CAM Folding 10x6',	 .77,	 .63,   	10,     	6,	2],
        ['Graupner CAM Folding 11x6',	 .8,	 .65,   	11,     	6,	2],
        ['Graupner CAM Folding 12x6',	 .81,	 .6,    	12,     	6,	2],
        ['Graupner CAM Folding 13x7',	 .81,	 .58,   	13,     	7,	2],
        ['Graupner CAM Folding 14x9.5',	 .85,	 .52,   	14,   	9.5,	2],
        ['Graupner CAM Folding 16x10',	 .61,	 .53,   	16,    	10,	2],
        ['Graupner Slim 8x4',		 .94,	 1.4,    	8,     	4,	2],
        ['Graupner Slim 8x6',		 .97,	 .77,    	8,     	6,	2],
        ['Graupner Slim 9x5',		 .82,	 .72,    	9,     	5,	2],
        ['Graupner Slim 10x6',		 1.01,	 .9,    	10,     	6,	2],
        ['Graupner Slim 10x8',	         	1.11,	 .95,   	10,     	8,	2],
        ['GWS 2.5x0.8',			 1.0,	 1.0,  	2.5,   	0.8,	2],
        ['GWS 2.5x1.0',			 .89,	 1.1,  	2.5,   	1.0,	2],
        ['GWS HD 3x2',			 1.15,	 1.5,    	3,     	2,	2],
        ['GWS HD 3x3',			 1.4,	 1.7,    	3,     	3,	2],
        ['GWS HD 4x2.5',	        		 0.92,	 1.0,    	4,   	2.5,	2],
        ['GWS HD 4x4',	                 	1.23,	 1.0,    	4,     	4,	2],
        ['GWS HD 4.5x3',	         		.94,	 .82,  	4.5,     	3,	2],
        ['GWS HD 4.5x4',	         		1.16,	 .75,  	4.5,     	4,	2],
        ['GWS HD 5x3',			 .79,	  .66,   	5,     	3,	2],
        ['GWS HD 5x4.3',		 	1.18,	  .72,   	5,   	4.3,	2],
        ['GWS HD 6x3',			 .84,	  .65,   	6,     	3,	2],
        ['GWS HD 6x3 3-Blade',		.76,	  .74,   	6,     	3,	3],
        ['GWS HD 7x3.5',	         		.65,	  .44,   	7,   	3.5,	2],
        ['GWS HD 7x3.5 3-Blade',	         	.69,	  .62,   	7,   	3.5,	3],
        ['GWS HD 8x4',			 .88,	  .62,   	8,     	4,	2],
        ['GWS HD 8x4 3-Blade pusher',	 .86,	  .9,   	8,     	4,	3],
        ['GWS HD 8x4 3-Blade tractor',	 .76,	  .75,   	8,     	4,	3],
        ['GWS HD 8x6',			 1.0,	  .82,   	8,     	6,	2],
        ['GWS HD 9x5',			 .95,	  .66,   	9,     	5,	2],
        ['GWS HD 10x6',			 .80,	  .57,  	10,     	6,	2],
        ['GWS HD 10x8',			 1.03,	  .75,  	10,     	8,	2],
        ['GWS HD 11x7',		         	.90,	  .60,  	11,     	7,	2],
        ['GWS RS 6x5',			 1.29,	  .96,   	6,     	5,	2],
        ['GWS RS 7x6',			 1.32,	  1.22,  	7,     	6,	2],
        ['GWS RS 8x4.3',		 	1.07,	   .76,  	8,   	4.3,	2],
        ['GWS RS 8x6',			 1.06,	  1.04,  	8,     	6,	2],
        ['GWS RS 9x4.7',		 	1.21,	   .89,  	9,   	4.7,	2],
        ['GWS RS 9x7',			 1.31,	   .96, 	9,     	7,	2],
        ['GWS RS 9x7 3-Blade',		 1.05,	   .9, 	9,     	7,	3],
        ['GWS RS 10x4.7',		 	1.38,	  1.1,  	10,   	4.7,	2],
        ['GWS RS 10x8',		 	1.39,	  1.1,  	10,     	8,	2],
        ['GWS RS 11x4.7',		 	1.42,	1.04,  	11,    	4.7,	2],
        ['Günter 4.9x4.3',		 	1.33,	  1.2,  	4.9,  	4.3,	2],
        ['Günter 5x4.3',		 	1.31,	  .74,    	5,  	4.3,	2],
        ['Günter 5.1x4.3',		 	1.47,	  .96,  	5.1,  	4.3,	2],
        ['Master Airscrew GF 8x4',		 .87,	  1.04,  	8,    	4,	2],
        ['Master Airscrew 8x5.5',		 1.04,	  1.64,  	8,   	5.5,	2],
        ['Master Air. electric 6x4 3-Blade',	 .8,	  1.06,  	6,    	4,	3],
        ['Master Airscrew electric 8x5.5',	 .95,	  1.3,    	8,   	5.5,	2],
        ['Master Airscrew electric 9x6',	 1.08,	  1.52,  	9,     	6,	2],
        ['Master Airscrew electric 10x6',	 1.23,	  1.68,  	10,     	6,	2],
        ['Master Airscrew electric 10x7',	 1.18,	  1.22,  	10,     	7,	2],
        ['Ramoser 15x12 3-Blade SG',	 1.45,	  1.24,  	15,     	12,	3],
        ['Ramoser 15x14 3-Blade SG',	 1.69,	  1.33,  	15,     	14,	3],
        ['Ramoser 15.2x15 5-Blade',	 	 .97,	  .77,  	15.2,     	15,	5],
        ['Ramoser 16.6x14 3-Blade',	 	 .75,	  .68,  	16.6,     	14,	3],
        ['Ramoser 16.6x14 4-Blade',	 	 .85,	  .71,  	16.6,     	14,	4],
        ['Ramoser 16.6x16 3-Blade',	 	 .86,	  .66,  	16.6,     	16,	3],
        ['Ramoser 16.6x16 4-Blade',	 	 .95,	  .74,  	16.6,     	16,	4],
        ['Zagi Carbon 5.1x4.9',		 1.11,	  1.14, 	5.1,  	4.9,	2]
        ]
    li_2=[]
##        session['s_dia'] =float(request.form['s_dia']) a
##        session['s_pit'] = float(request.form['s_pit']) b
##        session['s_nob'] = float(request.form['s_nob']) c

    for i in d:
        if a<=i[-3] and b<=i[-2] and c<=i[-1]:
            li_2.append(i)
    return li_2
def esc_s(a,b,c):
    esc =[['Airtronics 96334', 0.0025, 20, 0.5, 14.175],
          ['Astro 204', 0.005, 50, 1.1, 31.185000000000006],
          ['Astro 204D', 0.002, 60, 1.06, 30.051000000000002],
          ['Astro 210', 0.003, 45, 0.74, 20.979],
          ['Astro 211', 0.002, 75, 0.89, 25.2315],
          ['Astro 215', 0.003, 30, 0.32, 9.072000000000001],
          ['Astro 217', 0.005, 30, 0.53, 15.025500000000001],
          ['Astro 217D', 0.003, 35, 0.53, 15.025500000000001],
          ['Astro 800', 0.02, 15, 0.7, 19.845],
          ['Astro 801', 0.01, 25, 0.8, 22.680000000000003],
          ['Astro 805', 0.012, 30, 0.75, 21.262500000000003],
          ['Aveox A-15', 0.0036, 15, 0.2, 5.670000000000001],
          ['Aveox A-55', 0.0018, 55, 0.3, 8.505],
          ['Aveox EZ30', 0.014, 30, 1.6, 45.36000000000001],
          ['Aveox H160', 0.007, 60, 2.0, 56.7],
          ['Aveox H160C/CM', 0.0057, 70, 2.0, 56.7],
          ['Aveox H260', 0.007, 60, 2.0, 56.7],
          ['Aveox H260C/CM', 0.0057, 70, 2.0, 56.7],
          ['Aveox H360C/CM', 0.004, 90, 2.0, 56.7],
          ['Aveox L130', 0.0014, 35, 1.6, 45.36000000000001],
          ['Aveox L160', 0.007, 60, 2.0, 56.7],
          ['Aveox L160C/CM', 0.004, 70, 2.0, 56.7],
          ['Aveox L260', 0.007, 60, 2.0, 56.7],
          ['Aveox L260C/CM', 0.004, 70, 2.0, 56.7],
          ['Aveox L360C/CM', 0.004, 90, 4.0, 113.4],
          ['Aveox M160', 0.007, 60, 2.0, 56.7],
          ['Aveox M160C/CM', 0.004, 70, 2.0, 56.7],
          ['Aveox SH-24', 0.0028, 25, 1.7, 48.195],
          ['Aveox SH-48', 0.0028, 40, 1.7, 48.195],
          ['Aveox SH-48 BEC', 0.0028, 45, 1.7, 48.195],
          ['C. Creations Dragon 35', 0.0055, 35, 0.8, 22.680000000000003],
          ['C. Creations Dragon 55', 0.0023, 55, 1.2, 34.02],
          ['C. Creations Griffin 40', 0.0012, 40, 0.9, 25.515],
          ['C. Creations Griffin 50', 0.0011, 50, 0.75, 21.262500000000003],
          ['C. Creations Griffin 55', 0.001, 55, 1.0, 28.35],
          ['C. Creations Pegasus 35', 0.0015, 35, 0.75, 21.262500000000003],
          ['C. Creations Phoenix 10', 0.0013, 10, 0.21, 5.9535],
          ['C. Creations Phoenix 25', 0.0065, 25, 0.37, 10.4895],
          ['C. Creations Phoenix 35', 0.0045, 35, 0.9, 25.515],
          ['C. Creations Phoenix 45', 0.0026, 45, 1.0, 28.35],
          ['C. Creations Phoenix 60', 0.0012, 60, 2.0, 56.7],
          ['C. Creations Phoenix 80', 0.001, 80, 2.1, 59.535000000000004],
          ['C. Creations Phoenix 125', 0.0006, 125, 3.2, 90.72000000000001],
          ['C. Creations Pixie 14', 0.0045, 14, 0.3, 8.505],
          ['C. Creations Pixie 20P', 0.0025, 20, 0.3, 8.505],
          ['C. Creations Pixie 7', 0.009, 7, 0.11, 3.1185],
          ['C. Creations Pixie 7P', 0.007, 7, 0.1, 2.8350000000000004],
          ['C. Creations Pixie Lite', 0.0045, 14, 0.07, 1.9845000000000004],
          ['C. Creations Sprite 20', 0.004, 20, 0.4, 11.340000000000002],
          ['C. Creations Sprite 25', 0.0025, 25, 0.5, 14.175],
          ['C. Creations ThunderBird 18', 0.0065, 18, 0.6, 17.01],
          ['C. Creations ThunderBird 36', 0.0049, 36, 0.71, 20.1285],
          ['C. Creations ThunderBird 54', 0.0049, 54, 1.2, 34.02],
          ['Great Planes C05', 0.011, 5, 0.21, 5.9535],
          ['Great Planes C10', 0.0055, 10, 0.27, 7.6545000000000005],
          ['Great Planes C20', 0.0036, 20, 0.6, 17.01],
          ['Great Planes C30', 0.0028, 30, 0.7, 19.845],
          ['Great Planes C50', 0.0018, 50, 1.2, 34.02],
          ['G. Planes Electrifly BL-8', 0.013, 8, 0.42, 11.907],
          ['G. Planes Electrifly BL-12', 0.0075, 12, 0.42, 11.907],
          ['G. Planes Electrifly SS-8', 0.05, 8, 0.39, 11.056500000000002],
          ['G. Planes Electrifly SS-12', 0.03, 12, 0.49, 13.8915],
          ['G. Planes Electrifly SS-25', 0.015, 25, 0.92, 26.082],
          ['G. Planes Electrifly SS-35', 0.01, 35, 1.13, 32.0355],
          ['G. Planes Electrifly SS-45', 0.008, 45, 1.76, 49.896],
          ['Hacker 06-3P', 0.012, 6, 0.42, 11.907],
          ['Hacker 18-3P', 0.007, 18, 0.53, 15.025500000000001],
          ['Jeti 08-3P', 0.0013, 8, 0.55, 15.592500000000003],
          ['Jeti 150', 0.003, 140, 1.9, 53.865],
          ['Jeti eco', 0.003, 18, 0.71, 20.1285],
          ['Jeti 30-3P', 0.004, 30, 1.0, 28.35],
          ['Jeti Advance 70-3P Opto', 0.003, 70, 1.34, 37.989000000000004],
          ['Jeti JES 350', 0.003, 35, 0.6, 17.01], ['Jeti JES 020', 0.003, 20, 0.53, 15.025500000000001],
          ['Jeti JES 18-3P', 0.003, 18, 0.53, 15.025500000000001],
          ['Jeti 77 Opti', 0.001, 77, 2.0, 56.7],
          ['Jomar Mini-Max', 0.014, 30, 1.2, 34.02],
          ['Jomar Sport-Max', 0.009, 40, 1.4, 39.69],
          ['Kontronik 3SL 70-6-18', 0.004, 70, 1.24, 35.154],
          ['Kontronik Beat 40-6-12', 0.0056, 40, 1.17, 33.1695],
          ['Kontronik Beat 55-6-18', 0.0043, 55, 1.17, 33.1695],
          ['Kontronik Beat 70-6-12', 0.0021, 70, 1.3, 36.855000000000004],
          ['Kontronik Beat 80-6-18', 0.0021, 80, 1.32, 37.422000000000004],
          ['Kontronik Smile 40-6-12', 0.0056, 40, 1.3, 36.855000000000004],
          ['Master 70 B Flight', 0.001, 105, 1.41, 39.9735],
          ['MaxCim Maxu35A-21', 0.015, 60, 3.0, 85.05000000000001],
          ['MaxCim Maxu35A-25NB', 0.013, 65, 3.0, 85.05000000000001],
          ['MaxCim Maxu35C-21', 0.009, 65, 3.0, 85.05000000000001],
          ['MaxCim Maxu35C-25NB', 0.012, 65, 3.0, 85.05000000000001],
          ['Medusa Fusion ESC-2430BB', 0.0013, 30, 1.48, 41.958],
          ['Medusa Fusion ESC-2440BB', 0.001, 40, 1.63, 46.210499999999996],
          ['Medusa Fusion ESC-2450BB', 0.0008, 50, 1.66, 47.061],
          ['Medusa Spectrum ESC-1210BB', 0.004, 10, 0.39, 11.056500000000002],
          ['Medusa Spectrum ESC-1218BB', 0.002, 10, 0.64, 18.144000000000002],
          ['Medusa Spectrum ESC-1230BB', 0.0013, 30, 0.99, 28.0665],
          ['Medusa Spectrum ESC-1240BB', 0.001, 40, 1.17, 33.1695], ['Medusa Spectrum ESC-1250BB', 0.0008, 50, 1.24, 35.154], ['MGM ComPro 2512-3', 0.0039, 25, 0.71, 20.1285], ['MGM 1210', 0.0126, 12, 0.39, 11.056500000000002], ['MGM 4012', 0.0026, 40, 1.17, 33.1695], ['Microdrive M10P', 0.014, 10, 0.71, 20.1285], ['Microdrive M20P', 0.0035, 20, 0.71, 20.1285], ['Microdrive M30P', 0.0018, 40, 1.24, 35.154], ['NES-050', 0.025, 4, 0.14, 3.9690000000000007], ['NES-110', 0.02, 11, 0.57, 16.159499999999998], ['NES-140-compact', 0.02, 14, 0.57, 16.159499999999998], ['NES-180', 0.009, 18, 0.6, 17.01], ['NES-350', 0.004, 35, 0.88, 24.948], ['RipMax Xtra 05', 0.011, 5, 0.21, 5.9535], ['RipMax Xtra 12', 0.0055, 12, 0.28, 7.9380000000000015], ['RipMax Xtra 22', 0.0038, 22, 0.6, 17.01], ['RipMax Xtra 30', 0.0028, 30, 0.74, 20.979], ['RipMax Xtra 40', 0.0018, 40, 1.2, 34.02], ['RipMax Xtra 50', 0.0014, 50, 1.34, 37.989000000000004], ['RipMax Xtra 60', 0.0011, 60, 1.24, 35.154], ['Schulze future-11.20e', 0.008, 20, 0.62, 17.577], ['Schulze future-11.30e', 0.007, 30, 0.72, 20.412], ['Schulze future-11.40Ke', 0.004, 40, 1.24, 35.154], ['Schulze future-11.40KWe', 0.004, 40, 1.31, 37.1385], ['Schulze future-12.36e', 0.007, 36, 1.45, 41.1075], ['Schulze future-12.46e', 0.0046, 46, 1.45, 41.1075], ['Schulze future-12.46We', 0.0046, 46, 1.48, 41.958], ['Schulze future-12.97Fe', 0.0016, 97, 1.55, 43.9425], ['Schulze future-18.129F', 0.0004, 129, 1.55, 43.9425], ['Schulze future-18.129FW', 0.0008, 129, 1.59, 45.0765], ['Schulze future-18.36', 0.007, 36, 1.17, 33.1695], ['Schulze future-18.46K', 0.0046, 46, 1.45, 41.1075], ['Schulze future-18.46WK', 0.0046, 50, 1.66, 47.061], ['Schulze future-18.61', 0.0026, 61, 1.27, 36.0045], ['Schulze future-18.97F', 0.0016, 97, 1.55, 43.9425], ['Schulze future-18.97FW', 0.0016, 97, 1.59, 45.0765], ['Schulze future-18.97KFW', 0.0016, 97, 2.58, 73.143], ['Schulze future-24.40K', 0.006, 40, 1.45, 41.1075], ['Schulze future-24.89F', 0.001, 89, 1.55, 43.9425], ['Schulze future-32.170W', 0.0018, 170, 6.89, 195.3315], ['Schulze future-32.28K', 0.016, 28, 1.45, 41.1075], ['Schulze future-32.40K', 0.0074, 40, 1.45, 41.1075], ['Schulze future-32.55', 0.0054, 55, 1.7, 48.195], ['Schulze future-32.55WK', 0.0054, 62, 2.12, 60.102000000000004], ['Schulze future-32.80F', 0.0024, 80, 1.55, 43.9425], ['Schulze future-32.80FWK', 0.0024, 95, 2.23, 63.2205], ['Schulze future-40.70', 0.0036, 70, 1.8, 51.03], ['Schulze future-40.70WK', 0.0036, 83, 2.51, 71.1585], ['Schulze future-9.06ek', 0.033, 6, 0.21, 5.9535], ['Schulze future-9.12ek', 0.015, 12, 0.21, 5.9535], ['Schulze future-25b', 0.005, 25, 0.6, 17.01], ['Schulze future-45be', 0.0022, 45, 1.48, 41.958], ['Schulze mcf31-47be', 0.0033, 47, 0.74, 20.979], ['Schulze mcf31-47bo', 0.0033, 47, 0.74, 20.979], ['Schulze mcf31-52bo', 0.0027, 52, 0.74, 20.979], ['Schulze mcf43-110bo', 0.002, 110, 1.17, 33.1695], ['Schulze mcf43-70be', 0.0025, 70, 1.17, 33.1695], ['Schulze mcf43-75bo', 0.002, 75, 1.17, 33.1695], ['Schulze smart-47bo', 0.0033, 47, 0.74, 20.979], ['Schulze smart-52bo', 0.0027, 47, 0.74, 20.979], ['Schulze smart-70be', 0.0025, 70, 1.17, 33.1695], ['Schulze smart-75be', 0.002, 75, 1.17, 33.1695], ['Stefan 1-Fet BEC', 0.01, 12, 0.9, 25.515], ['Stefan 4-Fet BEC Brake', 0.0025, 48, 1.2, 34.02], ['Stefan 4-Fet Brake', 0.007, 40, 1.0, 28.35], ['Stefan Light 1-Fet BEC', 0.01, 12, 0.6, 17.01],
          ['TMM 40', 0.0025, 40, 1.55, 43.9425]]
    current=a
    min_weight=b
    max_weight=c
    c=[]
    w=[]
    for i in esc:
        if i[2]<=current:
            c.append(i)
            if i[-1]>min_weight and i[-1]<max_weight:
                w.append(i)
    return w
def motor_s(a,b,c):
    motorarray = [
        ['Above All 2813-18',         1200,     .075,	 1.2,	 25,	 1.94,	 165,    1.55,   1.01,    60, 8.2],
        ['Align BL450S 1000Kv',       1000,     .23,	.45,	 14,	 1.7,	 144,    1.55,   1.0,     30,   8],
        ['Align BL450S 1500Kv',	      1500,     .115,	.5,	 15,     1.7,    144,    1.55,   1.0,     30,	8],
        ['ARC-20-27-80', 	      4447,     .153,	.57,     12,     1.02,    87,    1.55,	 1.1,     50,	8],
        ['ARC-20-34-110',	      3026,     .1155,  .55,     12,     1.38,   117,    1.55,	 1.1,     40,	8],
        ['ARC-20-34-130',	      4600,     .05,    .87,     20,     1.38,   117,    1.55,	 1.1,     60,	8],
        ['ARC-28-37-2',	              3789,     .0556,  1.1,     60,     2.93,   250,    1.5,	 1.05,    20,	8],
        ['ARC-28-37-3',	              2729,     .103,   .8,      35,     2.72,   230,    1.55,	 1.05,    20,	8],
        ['ARC-28-47-2',	              2258,     .0592,  .95,     25,     4.06,   345,    1.5,	 1.05,    20,	8],
        ['ARC-28-58-1',	              3165,     .0249,  1.4,     80,     5.4,    460,    1.54,	 1.1,    20, 12.5],

        ['Astro C035 #603',	      2765,     .04,     2.5,     30,     6.0,   510,    1.55,	 1.1,     60,	8],
        ['Astro C05 #605',	      2125,     .045,    2.5,     30,     7.5,   636,    1.55, 	 1.1,     60,	8],
        ['Astro C15 #615',	      1488,     .069,    2,       25,     8.0,   680,    1.55,	 1.1,     60,	8],
        ['Astro C25 #625',	       971,     .093,    2,       30,     11,    936,    1.55,	 1.1,     60,	8],
        ['Astro C40 #640',	       682,     .121,    2,       30,     13,    1100,   1.55,	 1.1,     60,	8],
        ['Astro C60P #661',	       347,     .103,    2.5,     30,     22,    1870,   1.55,	 1.1,     60,	8],

        ['Aveox 1005/2Y',	      6173,     .018,    1.5,    35,      3.1,   264,    1.45,	 1.1,     60,	8],
        ['Aveox 1005/3Y',             4115,     .041,    1,      25,      3.1,   264,    1.45,	 1.0,     60,	8],
        ['Aveox 1005/4Y',	      3086,     .073,    .7,     15,      3.1,   264,    1.45, 	 1.0,     60,	8],
        ['Aveox 1005/5Y',	      2469,     .114,    .6,     12,      3.1,   264,    1.55,	 1.0,     60,	8],
        ['Aveox 1010/1Y',             5955,     .006,    1.8,    74,      4.6,   390,    1.40,	 1.2,     60,	8],
        ['Aveox 1010/1.5Y',           3970,     .014,    1.2,    35,      4.5,   384,    1.50,	 1.05,    60,	8],
        ['Aveox 1010/2Y',	      2978,     .024,    .9,     30,      4.6,   390,    1.56,	 1.0,     60,	8],
        ['Aveox 1010/3Y',	      1985,     .054,    .6,     15,      4.6,   390,    1.58,	 1.06,    60,	8],
        ['Aveox 1010/4Y',             1489,     .096,    .44,    10,      4.6,   390,    1.43,	 1.0,     60,	8],
        ['Aveox 27/13/2',	      4686,     .018,    1.68,   30,      2.86,  240,    1.47,	 1.0,     60,	8],
        ['Aveox 27/13/3',	      3124,     .041,    1.12,   30,      2.86,  240,    1.55,	 1.0,     60,	8],
        ['Aveox 27/13/4',	      2343,     .073,    .84,    23,      2.86,  240,    1.55,	 1.0,     60,	8],
        ['Aveox 27/13/5',	      1874,     .114,    .67,    15,      2.86,  240,    1.58,	 1.0,     60,	8],
        ['Aveox 27/26/1',	      4686,     .006,    3,      90,      4.34,  369,    1.48,	 1.0,     60,	8],
        ['Aveox 27/26/1.5',	      3124,     .014,    2,      60,      4.34,  369,    1.51,	 1.3,     60,	8],
        ['Aveox 27/26/2',             2343,     .024,    1.5,    45,      4.34,  369,    1.57,	 1.1,     60,	8],
        ['Aveox 27/26/3',	      1562,     .054,    1,      30,      4.34,  369,    1.57,	 1.1,     60,	8],
        ['Aveox 27/26/4',	      1172,     .096,    .75,    23,      4.34,  369,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/1',	      3124,     .007,    2.3,    90,      5.7,   486,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/1.5',	      2083,     .016,    1.53,   60,      5.7,   486,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/2',	      1562,     .028,    1.15,   45,      5.7,   486,    1.55,	 1.1,     60,	8],
        ['Aveox 27/39/3',	      1041,     .063,    .77,    30,      5.7,   486,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/4',	       781,     .112,    .58,    23,      5.7,   486,    1.55,	 1.0,     60,	8],

        ['AXI 2203/40 VPP Gold Line V2', 2000,  .245,    .5,     10,      .67,    60,    1.5,	 1.1,     60,	8],
        ['AXI 2203/Race Gold Line V2', 2355,    .213,    .62,    10,      .67,    62,    1.5,	 1.1,     20,  7.6],
        ['AXI 2203/46 Gold Line V2',  1785,     .387,    .32,    9.5,     .71,    60,    1.5,	 1.1,     50,	7],
        ['AXI 2203/52 Gold Line V2',  1579,     .452,    .31,    8.0,     .71,    50,    1.5,	 1.1,     53,	7],
        ['AXI 2204/54 Gold Line V2',  1395,     .420,    .36,    8.5,     .97,    80,    1.5,	 1.1,     35,	8],
        ['AXI 2208/20 Gold Line V2',  1863,     .143,   1.05,    18,      1.54,  130,    1.5,	 1.1,     25,	8],
        ['AXI 2208/26 Gold Line V2',  1428,     .191,    .6,     13,      1.54,  130,    1.5,	 1.1,     22,	8],
        ['AXI 2208/34 Gold Line V2',  1090,     .274,    .4,     10,      1.54,  130,    1.5,	 1.1,     27,	8],
        ['AXI 2212/12 Gold Line V2',  2043,     .061,   1.28,    30,      1.98,  300,    1.5,	 1.1,     50, 7.2],
        ['AXI 2212/20 Gold Line V2',  1159,     .149,    .71,    18,      1.98,  170,    1.5,	 1.1,     25,  10],
        ['AXI 2212/26 Gold Line V2',  944,      .224,    .5,     14,      1.98,  170,    1.5,	 1.1,     50, 9.3],
        ['AXI 2212/34 Gold Line V2',  691,      .292,    .31,    12,      1.98,  170,    1.5,	 1.1,    100,   8],
        ['AXI 2217/12 Gold Line V2',  1454,     .067,   1.38,    32,      2.45,  330,    1.5,	 1.1,     12,   8],
        ['AXI 2217/16 Gold Line V2',  1011,     .100,    .78,    24,      2.45,  245,    1.5,	 1.1,     19,   8],
        ['AXI 2217/20 Gold Line V2',   848,     .165,    .6,     24,      2.45,  270,    1.5,	 1.1,     33,   8],
        ['AXI 2808/16 Gold Line V2',  1875,     .073,    1.4,    26,      2.72,  230,    1.5,	 1.1,     10,   7],
        ['AXI 2808/20 Gold Line V2',  1495,     .091,    .92,    26,      2.72,  230,    1.5,	 1.1,     11,   7],
        ['AXI 2808/24 Gold Line V2',  1225,     .118,    .97,    23,      2.72,  230,    1.5,	 1.1,     15,   7],
        ['AXI 2814/6D Gold Line V2',  2866,     .027,    4.5,    56,      3.78,  550,    1.5,	 1.1,     10,	6],
        ['AXI 2814/10 Gold Line V2',  1742,     .046,    2.1,    46,      3.78,  320,    1.5,	 1.1,     10,	7],
        ['AXI 2814/12 Gold Line V2',  1446,     .06,     1.6,    36,      3.78,  320,    1.5,	 1.1,     10,	7],
        ['AXI 2814/16 Gold Line V2',  1063,     .065,    1.1,    32,      3.78,  325,    1.5,	 1.1,     19,	8],
        ['AXI 2814/20 Gold Line V2',  824,      .097,    .81,    26,      3.78,  355,    1.5,	 1.1,     28, 9.2],
        ['AXI 2820/08 Gold Line V2',  1486,     .038,    3.2,    56,      5.22,  565,    1.5,	 1.1,     13,	7],
        ['AXI 2820/10 Gold Line V2',  1138,     .040,    2.3,    43,      5.22,  440,    1.5,	 1.1,     10,	8],
        ['AXI 2820/12 Gold Line V2',  992,      .049,    1.5,    38,      5.22,  440,    1.5,	 1.1,     10,  10],
        ['AXI 2820/14 Gold Line V2',  831,      .063,    1.2,    37,      5.22,  520,    1.5,	 1.1,     15,   9],
        ['AXI 2826/06 Gold Line V2',  1501,     .030,    3.2,    66,      6.25,  665,    1.5,	 1.1,     15, 7.2],
        ['AXI 2826/08 Gold Line V2',  1119,     .040,    2.3,    56,      6.25,  570,    1.5,	 1.1,     15,  10],
        ['AXI 2826/10 Gold Line V2',  925,      .055,    1.9,    43,      6.25,  530,    1.5,	 1.1,     15, 9.5],
        ['AXI 2826/12 Gold Line V2',  740,      .055,    1.4,    38,      6.25,  530,    1.5,	 1.1,     10,  10],
        ['AXI 2826/13 Gold Line V2',  710,      .065,    1.5,    40,      6.25,  530,    1.5,	 1.1,     10,   8],
        ['AXI 4120/14 Gold Line V2',  662,      .034,    2.4,    57,     11.12, 1000,    1.5,	 1.1,     10,  10],
        ['AXI 4120/18 Gold Line V2',  505,      .056,    1.3,    59,     11.12, 1500,    1.5,	 1.1,     18,  12],
        ['AXI 4120/20 Gold Line V2',  456,      .072,    1.7,    53,     11.12, 1160,    1.5,	 1.1,     20,  21],
        ['AXI 4130/16 Gold Line V2',  370,      .069,    1.4,    61,     14.47, 1780,    1.5,	 1.1,     21,  15],
        ['AXI 4130/20 Gold Line V2',  300,      .088,    1.1,    56,     14.47, 1650,    1.5,	 1.1,     50,  15],
        ['AXI 5320/18 Gold Line V2',  370,      .023,    1.3,    79,     18.18, 1850,    1.5,	 1.1,     20,  20],
        ['AXI 5320/18 3D Extreme V2', 370,      .023,    1.3,    79,     18.71, 1900,    1.5,	 1.1,     20,  20],
        ['AXI 5320/28 Gold Line V2',  235,      .091,    1.2,    65,     18.18, 1600,    1.5,	 1.1,     42,  25],
        ['AXI 5320/34 Gold Line V2',  192,      .124,    0.9,    50,     18.18, 1850,    1.5,	 1.1,     53,  25],
        ['AXI 5325/16 Gold Line V2',  350,      .026,    2.0,    86,     21.0,  2650,    1.5,	 1.1,     50,  20],
        ['AXI 5325/18 Gold Line V2',  308,      .032,    1.6,    81,     21.0,  2440,    1.5,	 1.1,     50,  20],
        ['AXI 5325/20 Gold Line V2',  280,      .037,    1.9,    79,     21.0,  2430,    1.5,	 1.1,     50,  30],
        ['AXI 5325/24 Gold Line V2',  232,      .045,    1.6,    76,     21.0,  2850,    1.5,	 1.1,     50,  30],
        ['AXI 5330/18 Gold Line V2',  255,      .038,    1.8,    76,     23.72, 2870,    1.5,	 1.1,     23,  25],
        ['AXI 5330/F3A Gold Line V2', 220,      .038,    1.3,    73,     23.72, 2780,    1.5,	 1.1,     37,  25],
        ['AXI 5330/24 Gold Line V2',  197,      .057,    1.4,    59,     23.72, 2220,    1.5,	 1.1,     50,  30],
        ['AXI 5345/14HD Gold Line V2', 225,     .027,    2.5,   112,     35.12, 4200,    1.5,	 1.1,     50,  30],
        ['AXI 5345/16HD Gold Line V2', 195,     .034,    2.0,    92,     35.12, 4195,    1.5,	 1.1,     50,  30],
        ['AXI 5345/18HD Gold Line V2', 171,     .042,    1.5,    77,     35.12, 3510,    1.5,	 1.1,     50,  30],
        ['AXI 5345/20HD Gold Line V2', 145,     .042,    1.5,    85,     35.12, 3870,    1.5,	 1.1,     50,  30],
        ['AXI 5360/18HD Gold Line V2', 125,     .058,    1.8,    75,     44.83, 2900,    1.5,	 1.1,     50,  30],
        ['AXI 5360/20HD Gold Line V2', 115,     .068,    1.8,    65,     44.83, 3000,    1.5,	 1.1,     50,  30],
        ['AXI 5360/24HD Gold Line V2',  95,     .082,    1.8,    65,     44.83, 3120,    1.5,	 1.1,     50,  30],

        ['Cobra C-2202/70',           1530,     .504,    .25,     6,      0.53,   45,    1.3,	 1.1,     40,   8],
        ['Cobra C-2203/46',           1720,     .220,    .40,     8,      0.62,   60,    1.3,	 1.1,     40,   8],
        ['Cobra C-2204/32',           1900,     .173,    .58,    12,      0.79,   90,    1.3,	 1.1,     40,   8],
        ['Cobra C-2208/20',           2000,     .096,    .80,    18,      1.64,  200,    1.3,	 1.05,    40,   8],
        ['Cobra C-2208/34',           1180,     .228,    .40,    12,      1.66,  130,    1.3,	 1.05,    40,   8],
        ['Cobra C-2213/12',           1957,     .077,    1.2,    30,      2.11,  330,    1.45,	 1.1,     40,   8],
        ['Cobra C-2213/18',           1350,     .102,    .68,    20,      2.15,  220,    1.3,	 1.1,     40,   8],
        ['Cobra C-2213/22',           1082,     .178,    .55,    17,      2.11,  190,    1.45,	 1.1,     40,   8],
        ['Cobra C-2213/26',            950,     .220,    .8,     14,      2.15,  150,    1.3,	 1.1,     40,  11],
        ['Cobra C-2217/8',            2300,     .042,   2.10,    40,      2.61,  300,    1.3,	 1.1,     20,   8],
        ['Cobra C-2217/12',           1540,     .086,   1.15,    32,      2.61,  230,    1.3,	 1.1,     20,   8],
        ['Cobra C-2221/8',            1850,     .049,   1.59,    45,      3.10,  500,    1.3,	 1.1,     20,   8],
        ['Cobra C-2221/10',           1500,     .055,   1.38,    38,      3.10,  420,    1.3,	 1.1,     20,  12],
        ['Cobra C-2221/12',           1250,     .075,   1.09,    32,      3.10,  360,    1.3,	 1.1,     20,  12],
        ['Cobra C-2221/16',            940,     .126,    .75,    25,      3.10,  280,    1.3,	 1.1,     40,  12],
        ['Cobra C-2808/16',           1780,     .056,   1.35,    30,      2.85,  330,    1.3,	 1.1,     20,   8],
        ['Cobra C-2808/22',           1330,     .084,    .82,    24,      2.85,  270,    1.3,	 1.1,     40,   8],
        ['Cobra C-2808/26',           1130,     .113,    .75,    22,      2.85,  240,    1.3,	 1.1,     40,   8],
        ['Cobra C-2808/30',           1000,     .144,    .53,    20,      2.85,  220,    1.3,	 1.1,     40,   8],
        ['Cobra C-2814/10',           1700,     .036,   2.06,    48,      3.84,  530,    1.3,	 1.1,     20,  10],
        ['Cobra C-2814/12',           1390,     .045,   1.44,    40,      3.84,  450,    1.3,	 1.1,     20,  10],
        ['Cobra C-2814/16',           1050,     .068,    .9,     30,      3.84,  330,    1.3,	 1.1,     40,  10],
        ['Cobra C-2814/20',            850,     .099,    .7,     25,      3.84,  280,    1.3,	 1.1,     40,  10],
        ['Cobra C-2820/8',            1450,     .030,   2.5,     55,      4.9,   610,    1.3,	 1.1,     20,  10],
        ['Cobra C-2820/10',           1170,     .041,   1.6,     45,      5.01,  490,    1.3,	 1.1,     20,  10],
        ['Cobra C-2820/12',            970,     .059,   1.3,     40,      4.87,  440,    1.3,	 1.1,     20,  10],
        ['Cobra C-2820/14',            840,     .071,   1.0,     36,      4.94,  400,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/6',            1470,     .027,   3.0,     65,      6.03,  720,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/8',            1130,     .038,   2.3,     55,      6.03,  610,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/10',            930,     .048,   1.3,     45,      6.03,  610,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/12',            760,     .068,   1.1,     42,      6.03,  460,    1.3,	 1.1,     20,  10],
        ['Cobra C-3510/16',           1200,     .042,   1.4,     42,      4.97,  460,    1.3,	 1.1,     20,  14],
        ['Cobra C-3510/20',           1000,     .060,   1.06,    32,      4.97,  350,    1.3,	 1.1,     20,  14],
        ['Cobra C-3510/24',            820,     .080,    .81,    26,      4.97,  480,    1.3,	 1.1,     40,  14],
        ['Cobra C-3515/12',           1100,     .036,   1.64,    45,      6.28,  500,    1.3,	 1.1,     20,  14],
        ['Cobra C-3515/14',            950,     .044,   1.39,    44,      6.28,  500,    1.3,	 1.1,     20,  14],
        ['Cobra C-3515/18',            740,     .065,   1.01,    36,      6.28,  530,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/10',            980,     .037,   1.84,    60,      7.41,  670,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/12',            820,     .039,   1.45,    56,      7.62,  650,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/14',            700,     .048,   1.33,    46,      7.62,  680,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/18',            550,     .075,    .93,    36,      7.62,  670,    1.3,	 1.1,     40,  14],
        ['Cobra C-3525/10',            780,     .035,   1.65,    62,      8.92,  760,    1.3,	 1.1,     20,  14],
        ['Cobra C-3525/12',            650,     .045,   1.48,    52,      8.92,  960,    1.3,	 1.1,     20,  20],
        ['Cobra C-3525/14',            560,     .055,   1.18,    45,      8.92,  670,    1.3,	 1.1,     20,  20],
        ['Cobra C-3525/18',            430,     .087,    .84,    38,      8.92,  700,    1.3,	 1.1,     40,  20],
        ['Cobra C-4120/12',            850,     .021,   2.74,    75,     10.34, 1110,    1.3,	 1.1,     20,  14],
        ['Cobra C-4120/14',            710,     .027,   1.99,    68,     10.34, 1260,    1.3,	 1.1,     20,  14],
        ['Cobra C-4120/16',            610,     .036,   1.51,    62,     10.34, 1150,    1.3,	 1.1,     20,  14],
        ['Cobra C-4120/18',            540,     .045,   1.5,     54,     10.23, 1200,    1.3,	 1.1,     20,  20],
        ['Cobra C-4120/22',            430,     .06,    1.14,    45,     10.23, 1000,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/12',            540,     .029,   1.85,    65,     14.04, 1440,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/14',            450,     .036,   1.46,    60,     14.11, 1330,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/16',            390,     .048,   1.12,    55,     13.97, 1220,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/20',            300,     .069,   .77,     52,     13.97, 1150,    1.3,	 1.1,     40,  20],
        ['Cobra CM-2204/28',          2300,     .126,   .66,     17,       .87,  125,    1.3,	 1.1,     30,   8],
        ['Cobra CM-2204/32',          1960,     .153,   .58,     13,       .87,   90,    1.3,	 1.1,     30,   8],
        ['Cobra CM-2208/20',          2000,     .114,   .77,     20,       1.56, 150,    1.3,	 1.1,     30,   8],
        ['Cobra CM-2208/34',          1200,     .265,   .36,     12,       1.56, 135,    1.3,	 1.1,     40,  10],
        ['Cobra CM-2213/26',           950,     .230,   .42,     12,       2.29, 155,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2213/36',           700,     .389,   .28,     11,       2.42, 120,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2217/20',           950,     .188,   .53,     20,       2.68, 220,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2217/26',           695,     .269,   .36,     16,       2.86, 175,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2814/24',           700,     .142,   .55,     23,       4.09, 340,    1.3,	 1.1,     50,  12],
        ['Cobra CM-2814/36',           470,     .282,   .29,     17,       4.13, 330,    1.3,	 1.1,     50,  12],
        ['Cobra CM-2820/16',           740,     .111,   .92,     35,       5.15, 430,    1.3,	 1.1,     50,  15],
        ['Cobra CM-2820/24',           490,     .166,   .53,     27,       5.15, 500,    1.3,	 1.1,     50,  15],
        ['Cobra CM-2820/32',           350,     .300,   .33,     20,       5.15, 450,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3515/20',           650,     .087,   .78,     34,       7.02, 600,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3515/34',           385,     .200,   .38,     24,       7.02, 530,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3520/20',           480,     .104,   .68,     32,       8.25, 650,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3520/28',           350,     .176,   .43,     26,       8.25, 575,    1.3,	 1.1,     50,  15],
        ['Cobra CM-4008/24',           600,     .086,   .72,     23,       3.74, 340,    1.3,	 1.1,     50,  12],
        ['Cobra CM-4008/36',           400,     .151,   .52,     18,       3.74, 400,    1.3,	 1.1,     50,  21],
        ['Cobra CM-4510/28',           420,     .087,   .68,     35,       7.44, 780,    1.3,	 1.1,     50,  20],
        ['Cobra CM-4510/40',           310,     .170,   .31,     22,       7.44, 490,    1.3,	 1.1,     50,  15],
        ['Cobra CM-4515/18',           435,     .051,   .95,     54,       9.63, 1200,   1.3,	 1.1,     50,  15],
        ['Cobra CM-4520/14',           400,     .048,  1.45,     60,      12.06, 1330,   1.3,	 1.1,     50,  21],
        ['Cobra CM-4520/18',           310,     .066,   .99,     45,      11.99, 1000,   1.3,	 1.1,     50,  21],

        ['Dualsky 2822-24',           1533,     .446,     .50,   10,     1.06,    90,    1.52,	 1.0,     20,   8],
        ['Dualsky 2826-15',           1208,     .211,     .60,   15,     1.55,   130,    1.52,	 1.0,     20,   8],
        ['Dualsky 450EP 2834-8',      3330,     .084,    2.60,   32,     2.40,   200,    1.52,	 1.0,     10, 9.3],
        ['Dualsky XM2826-18',         1012,     .345,     .40,   12,     1.55,   150,    1.35,	 1.05,    20,   7],
        ['Dualsky XM2830CA-10',       1168,     .179,    1.17,   20,     1.94,   165,    1.5,	 1.02,    10,12.2],
        ['Dualsky XM2834CA-9T',        971,     .125,     .7,    24,     2.47,   210,    1.5,	 1.02,    10,  10],
        ['Dualsky XM3530EA-13',        963,     .128,     .92,   19,     2.54,   215,    1.5,	 1.02,    15, 8.3],
        ['Dualsky XM3536CA-8',        1037,     .101,    1.24,   35,     3.64,   300,    1.50,	 1.1,     10,  12],
        ['Dualsky XM3542CA-7T',        789,    .0795,    1.64,   34,     4.84,   400,    1.50,	 1.1,     10,  10],
        ['Dualsky XM3548-5',          1124,    .0865,    1.6,    40,     5.82,   490,    1.50,	 1.05,    10,   8],
        ['Dualsky XM4240CA-12T',       984,    .0958,    1.15,   35,     4.48,   380,    1.45,	 1.1,     12,  10],

        ['E-flite Park 300 BL 1380',  1380, 	.33,	 .4,	 9,	  .8,     85,    1.5,    1.1,     60,  10],
        ['E-flite Park 370 BL 1080',  1080, 	.19,	 .7,	 10,	  1.6,   100,    1.5,    1.1,     60,  10],
        ['E-flite Park 370 BL 1360',  1360, 	.1,	 1.0,	 13,	  1.6,   125,    1.5,    1.1,     40,  10],
        ['E-flite Park 400 BL 740',    740, 	.26,	 0.55,	 10,	  2.0,   100,    1.5,    1.1,     40,  10],
        ['E-flite Park 400 BL 920',    920, 	.1,	 0.7,	 13,	  2.0,   140,    1.5,    1.1,     40,  10],
        ['E-flite Park 450 BL 890',    890, 	.2,	 .7,	 18,	  2.5,   175,    1.5,    1.1,     40,  10],
        ['E-flite Park 480 BL 910',    910, 	.08,	 .85,	 25,	  3.1,   250,    1.5,    1.1,     40,  10],
        ['E-flite Park 480 BL 1020',  1020, 	.06,	 1.1,	 28,	  3.1,   275,    1.5,    1.1,     40,  10],
        ['E-flite Power 10 BL',	      1100, 	.04,	 2.1,	 38,	  4.3,   375,    1.5,    1.1,     40,  10],
        ['E-flite Power 15 BL',	       950, 	.03,	 2.0,	 42,	  5.4,   425,    1.5,    1.1,     40,  10],
        ['E-flite Power 25 BL',	       870, 	.03,	 2.4,	 44,	  6.7,   550,    1.5,    1.1,     40,  10],
        ['E-flite Power 32 BL',	       770, 	.02,	 2.4,	 60,	  7.0,   700,    1.5,    1.1,     40,  10],
        ['E-flite Power 46 BL',	       670, 	.04,	 3.9,	 55,	 10.0,   800,    1.5,    1.1,     40,  15],
        ['E-flite Power 60 BL',	       400, 	.06,	 2.7,	 60,	 13.0,  1200,    1.5,    1.1,     40,  15],
        ['E-flite Power 110 BL',       295, 	.03,	 1.3,	 65,	 17.5,  1900,    1.5,    1.1,     40,  15],
        ['E-flite Power 160 BL',       260, 	.02,	 1.6,	 75,	 23.0,  2500,    1.5,    1.1,     40,  15],

        ['Electrifly RimFire 28-22-1380',1380,  .370,    .4,      9,      .96,    81,    1.25,	 1.1,     30, 7.4],
        ['Electrifly RimFire 28-26-1000',1000,  .165,    .7,     12,      1.45,  123,    1.25,   1.3,     30, 7.4],
        ['Electrifly RimFire 28-26-1300',1300,  .155,    .9,     15,      1.45,  123,    1.38,   1.02,    19, 7.4],
        ['Electrifly RimFire 28-26-1600',1600,  .098,    1.0,    17,      1.45,  123,    1.50,   1.02,    15, 7.4],
        ['Electrifly RimFire 28-30-750',  740,  .185,    .6,     10,      1.91,  162,    1.25,   1.3,     13, 7.4],
        ['Electrifly RimFire 28-30-950',  940,  .098,    .7,     14,      1.91,  162,    1.28,   1.35,    12, 7.4],
        ['Electrifly RimFire 28-30-1250',1250,  .120,    .9,     18,      1.91,  162,    1.50,   1.1,     13, 7.4],
        ['Electrifly RimFire 28-30-1450',1450,  .065,    1.07,   23,      1.91,  162,    1.55,   1.01,    13, 7.4],
        ['Electrifly RimFire 35-30-950',  940,  .065,    .8,     20,      2.51,  213,    1.45,   1.35,    15,  11],
        ['Electrifly RimFire 35-30-1250',1250,  .115,    1.2,    30,      2.51,  213,    1.40,   1.0,     15,  11],
        ['Electrifly RimFire 35-36-1000',1000,  .055,    1.4,    40,      3.6,   306,    1.45,   1.0,     13,  11],
        ['Electrifly RimFire 35-36-1200',1200,  .047,    1.8,    45,      3.6,   306,    1.48,   1.0,     13,  11],
        ['Electrifly RimFire 35-36-1500',1500,  .030,    2.6,    50,      3.6,   306,    1.25,   1.0,     13,  11],
        ['Electrifly RimFire 35-48-700',  670,  .025,    1.4,    35,      6.0,   510,    1.40,   1.4,     10, 14,8],

        ['Goldberg Turbo 550',        2528,     .085,    2,      60,      7.8,   663,    1.55,	 1.0,     60,	8],
        ['Graupner Sp280 6V',         2320,     1.12,    .28,    8,       1.5,   127,    1.50,	 1.1,     50,	6],
        ['Graupner Sp300 6V',         4833,     .214,    .7,     12,      1.8,   153,    1.55,	 1.1,     50,	8],
        ['Graupner Sp400 6V',         3000,     .303,    .7,     12,      2.6,   222,    1.55,	 1.15,    15,	6],
        ['Graupner Sp400 7.2V',       2277,     .450,    .5,     18,      2.6,   222,    1.55,   1.15,    28, 7.2],
        ['Graupner Sp480 7.2V',       2350,     .298,    1.1,    20,      3.7,   315,    1.40,	 1.16,    32, 7.2],
        ['Graupner Sp480 Race 7.2V',  2936,     .155,    2.0,    20,      3.7,   315,    1.53,	 1.05,    18, 7.2],
        ['Graupner Sp500 Race 7.2V',  2985,     .105,    2.5,    20,      3.7,   315,    1.55,	 1.05,    18, 7.2],
        ['Graupner Sp600 7.2V',       2437,     .112,    2.0,    25,      6.9,   585,    1.53,	 1.06,    15, 7.2],
        ['Graupner Sp600 8.4V',       1780,     .150,    1.8,    25,      7.8,   663,    1.55,	 1.05,    25, 8.4],
        ['Graupner Sp600 9.6V',       1470,     .201,    1.0,    30,      6.9,   585,    1.52,	 1.08,    40, 9.6],
        ['Graupner Sp700 Race 9.6V',  1875,     .120,    3.0,    25,      11.5,  978,    1.55,	 1.08,    60, 9.6],
        ['G. P. Goldfire',            2441,     .094,    2,      25,      7.6,   645,    1.55,	 1.0,      60,	8],
        ['G. P. Thrustmaster',        2168,     .18,     1.5,    25,      7.6,   645,    1.55,	 1.0,      60,	8],

        ['Hacker A05-10S',            4200,     .3,      .5,     5,       .265,   25,    1.5,    1.1,     26, 8.4],
        ['Hacker A05-13S',            3200,     .29,     .4,     5,       .265,   30,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-7L',             2200,     .11,     1.1,    8,       .71,    60,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-9L',             1700,     .18,     .72,    8,       .71,    60,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-12S',            2900,     .185,    1.0,    6,       .53,    45,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-13L',            1200,     .28,     .39,    9,       .71,    60,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-15S',            2320,     .289,    .63,    6,       .53,    45,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-6XL 8Pole EVO',  3500,     .014,    3.4,    55,      2.75,  300,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-6XL 10Pole EVO', 2500,     .020,    3.4,    40,      2.75,  300,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-8XL EVO',        1500,     .026,    2.6,    35,      2.75,  300,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-12XL EVO',       1039,     .075,    1.2,    30,      2.75,  230,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-20L EVO',        1022,     .089,    .85,    19,      1.94,  165,    1.5,	 1.1,     30, 8.4],
        ['Hacker A20-20L',            1022,     .109,    .85,    19,      2.01,  210,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-22L EVO',         924,     .109,    .75,    17,      1.94,  165,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-22L',             924,     .089,    .75,    17,      2.01,  190,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-26M EVO',        1130,     .117,    .7,     15,      1.48,  126,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-26M',            1130,     .117,    .7,     15,      1.48,  150,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-30M',             980,     .174,    .6,     14,      1.48,  150,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-34S',            1500,     .147,    .75,    10,      1.02,  100,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-50S',            1088,     .232,    .4,     8,       1.02,   80,    1.5,    1.1,     26, 8.4],
        ['Hacker A30-10L V3',         1185,     .023,    2.3,    40,      5.05,  500,    1.5,    1.1,     26, 8.4],
        ['Hacker A30-22S V3',         1440,     .041,    1.4,    28,      2.47,  275,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-10XL V4',         900,     .024,    1.9,    50,      6.25,  530,    1.5,    1.1,     26, 8.4],
        ['Hacker A30-12L V4',         1000,     .03,     1.8,    35,      5.05,  500,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-12XL V4',         700,     .034,    1.5,    37,      6.25,  600,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-14L V4',         800,      .036,    1.6,    35,      5.05,  800,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-16M V4',         1060,     .038,    1.6,    35,      3.67,  350,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-12M V4',         1370,     .022,    2.2,    35,      3.67,  350,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-22S V4',         1440,     .041,    1.4,    25,      2.47,  250,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-28S V4',         1140,     .068,    1.1,    25,      2.47,  250,    1.5,    1.1,     50, 8.4],
        ['Hacker A50-12L Glider',      355,     .021,    1.5,    70,      17.8, 1500,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-12S V4',          480,     .016,    1.8,    55,     12.18, 1030,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-14L V4',          300,     .025,    1.0,    70,     15.71, 1330,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-14S V4',          425,     .021,    1.5,    55,     12.18, 1030,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-16S V4',          365,     .026,    1.4,    70,     12.18, 1030,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-8S Tornado V3',   850,     .009,    4.1,    80,     12.28, 1040,    1.5,	 1.1,     60, 8.4],
        ['Hacker A50-10S Tornado V3',  690,     .011,    3.1,    80,     12.28, 1040,    1.5,	 1.1,     66, 8.4],
        ['Hacker A60-5XS V2',         3065,     .125,    .4,     12,      1.8,   153,    1.5,	 1.1,     26, 8.4],
        ['Hacker Q60-7M F3A',          210,     .025,   1.8,     90,     20.47, 1740,    1.5,	 1.1,     60, 8.4],

        ['Himax HC2808-0860',          860,     .255,    .36,    11,      1.83,  156,    1.55,   1.05,     26,	8],
        ['Himax HC2808-0980',          980,     .22,     .4,     12,      1.83,  156,    1.50,	 1.09,     26,	8],
        ['Himax HC2808-1160',         1160,     .15,     .6,     15,      1.83,  156,    1.55,	 1.05,     26,	8],
        ['Himax HC2812-0650',          650,     .285,    .36,    11,      2.26,  192,    1.55,	 1.05,     26,	8],
        ['Himax HC2812-0850',          850,     .169,    .6,     14,      2.26,  192,    1.55,	 1.05,     26,	8],
        ['Himax HC2812-1080',         1080,     .111,    .75,    15,      2.26,  192,    1.55,	 1.05,     26,	8],
        ['Himax HC2816-0890',          890,     .119,    .8,     18,      2.72,  230,    1.55,	 1.05,     40,	8],
        ['Himax HC2816-1220',         1200,     .071,    1.4,    25,      2.72,  230,    1.55,	 1.1,      30, 10],
        ['Himax HC3510-1100',         1100,     .055,    1.2,    30,      3.14,  267,    1.55,	 1.05,     50,	8],
        ['Himax HC3510-1540',         1540,     .029,    1.8,    42,      3.14,  267,    1.55,	 1.05,     50,	8],
        ['Himax HC3516-0840',          840,     .051,    1.5,    37,      4.73,  400,    1.55,	 1.05,     60,	8],
        ['Himax HC3516-1130',         1130,     .03,     1.8,    48,      4.73,  400,    1.55,	 1.05,     60,	8],
        ['Himax HC3516-1350',         1350,     .023,    2.3,    56,      4.73,  400,    1.55,	 1.05,     60,	8],
        ['Himax HC3522-0700',          700,     .049,    1.3,    40,      5.71,  486,    1.53,	 1.05,     60,	8],
        ['Himax HC3522-0990',          990,     .027,    2.2,    54,      5.71,  486,    1.53,	 1.05,     60,	8],
        ['Himax HC3528-0800',          800,     .031,    1.7,    54,      6.95,  590,    1.30,	 1.0,      60,	8],
        ['Himax HC3528-1000',         1000,     .02,     2.6,    68,      6.95,  590,    1.50,	 1.05,     60,	8],

        ['Hyperion Z-2205-34',        1500,     .34,     .5,      8,      1.04,   90,    1.52,	 1.0,      60,	8],
        ['Hyperion Z-2205-38',        1300,     .42,     .38,     7,      1.04,   90,    1.59,	 1.0,      40,	8],
        ['Hyperion Z-2209-26',        1100,     .170,    .65,    11,      1.47,  126,    1.57,	 1.0,      38,	8],
        ['Hyperion Z-2209-32',         900,     .240,    .55,    10,      1.47,  126,    1.52,	 1.05,     32,	8],
        ['Hyperion Z-2213-20',        1010,     .150,    .65,    14,      1.87,  159,    1.58,	 1.0,      32,	8],
        ['Hyperion Z-2213-24',         850,     .175,    .60,    12,      1.87,  159,    1.56,	 1.0,      28,	8],
        ['Hyperion Z-3007-26',        1228,     .085,    1.11,   28,      2.65,  150,    1.50,	 1.05,     16,	8],
        ['Hyperion Z-3007-30',        1033,     .095,    1.2,    25,      2.65,  150,    1.50,	 1.02,     16,	8],
        ['Hyperion Z-3013-14',        1080,     .048,    2.5,    40,      3.88,  330,    1.50,	 1.0,      23,	8],
        ['Hyperion Z-3013-16',         985,     .059,    2.0,    36,      3.88,  330,    1.50,	 1.05,     18,	8],
        ['Hyperion Z-3019-10',        1230,     .031,    2.42,   46,      5.01,  426,    1.51,	 1.02,     10,	8],
        ['Hyperion Z-3019-12',         900,     .034,    2.35,   42,      5.01,  426,    1.55,	 1.05,     10,	8],
        ['Hyperion Z-3025-08',         985,     .036,    4.8,    65,      6.56,  558,    1.50,	 1.05,     10,  10],
        ['Hyperion Z-3025-10',         815,     .025,    2.3,    46,      6.56,  558,    1.55,	 1.0,      60,	8],

        ['Jeti Phasor 15-3',          2300,     .025,    2.5,    35,      4.8,   408,    1.50,	 1.3,      60,	8],
        ['Jeti Phasor 15-4',          1800,     .042,    1.9,    32,      4.8,   408,    1.50,	 1.2,      60,	8],
        ['Jeti Phasor 30-3',          1200,     .034,    2.8,    35,      4.8,   408,    1.50,	 1.2,      60,	8],

        ['KDA20-34S',                 1850,     .330,    .72,     9,      1.06,   90,    1.50,	 1.05,    20,  11],
        ['KDA2217/20',                 875,     .195,    1.0,    22,      2.51,  213,    1.50,	 1.0,     20,12.4],
        ['KDA KB2835-35',             2350,     .190,    1.0,    20,      3.21,  270,    1.50,	 1.05,    20,   7],

        ['Kontronik FUN400-23',       2300,     .058,    .5,     30,      3.88,  330,    1.5,	 1.1,      60,	8],
        ['Kontronik FUN400-42',       4000,     .017,    2.0,    50,      3.88,  330,    1.40,	 1.1,      40,  7],
        ['Kyosho AP-29L',             4099,     .0907,   3.5,    30,      5.5,   468,    1.55,	 1.05,     60,	8],
        ['Kyosho AP-29L meas',        3914,     .034,    3.8,    35,      5,     426,    1.55,	 1.05,     60,	8],
        ['Kyosho Atomic Force',       3531,     .035,    2.94,   30,      6.3,   537,    1.55,	 1.05,     60,	8],
        ['Kyosho EndoPlasma',         3785,     .022,    2.5,    30,      6.3,   537,    1.55,	 1.05,     60,	8],
        ['Kyosho LeMans 480 Gold',    2500,     .076,    1.1,    30,      6.25,  530,    1.55,	 1.05,     60,	8],
        ['Kyosho LeMans DMC20BB',     4939,     .054,    .54,    30,      6.3,   537,    1.55,	 1.05,     60,	8],
        ['Kyosho Magnetic Mayhem',    2260,     .0667,   1.37,   30,       8,    680,    1.55,	 1.05,     60,	8],
        ['MEC Turbo 10 GT',           3400,     .038,    2.3,    35,       10,   852,    1.55,	 1.05,     60,	8],
        ['MEC Turbo 10 Plus',         4850,     .025,    3.4,    35,       11,   936,    1.55,	 1.05,     60,	8],

        ['Medusa MR-012-030-4000',    3940,     .386,     .3,     6,       .53,   45,    1.53,	 1.05,     20,	8],
        ['Medusa MR-012-030-5300',    5230,     .228,     .43,    7,       .53,   45,    1.53,	 1.01,     20,	8],
        ['Medusa MR-028-032-1200',    1200,     .185,     .35,   15,      2.47,  210,    1.48,	 1.05,     40,	8],
        ['Medusa MR-028-032-1500',    1490,     .118,    .5,     19,      2.47,  210,    1.50,   1.02,     30,	8],
        ['Medusa MR-028-032-1900',    1890,     .085,    .65,    23,      2.47,  210,    1.48,	 1.03,     40,	8],
        ['Medusa MR-028-032-2400',    2390,     .050,    .85,    28,      2.47,  210,    1.53,	 1.0,      30,	8],
        ['Medusa MR-028-032-2800',    2790,     .040,     1.0,   30,      2.47,  210,    1.52,	 1.05,     30,	8],

        ['Mega ACn 16-15-4',          2300,     .045,     1.1,   20,      2.7,   230,    1.5,	 1.1,      50,	8],
        ['Mega ACn 16-15-5',          1800,     .060,    .80,    20,      2.7,   230,    1.80,	 1.0,      50,	8],
        ['Mega ACn 16-15-6',          1500,     .112,    .79,    18,      2.7,   230,    1.80,	 1.0,      50,  12],
        ['Mega ACn 16-15-8',          1230,     .176,    .33,    15,      2.7,   230,    1.78,	 1.0,      50, 8.2],
        ['Mega ACn 22-20-4',          1550,     .055,    1.8,    50,      5.82,  495,    1.70,	 1.0,      60,  14],
        ['Mega ACn 22-30-3',          1300,     .042,    1.11,   70,      7.79,  660,    1.80,	 1.0,      60, 8.6],

        ['Mini AC 1215/16',	      3800,     .086,    1.4,    18,      1.7,   144,    1.55,	 1.3,      60,	8],
        ['Mini AC 1215/20',           3000,     .117,    1.1,    16,      1.73,  147,    1.55,	 1.4,      60,	8],
        ['Mini AC Extreme',           6370,     .045,    3.9,    28,      2.72,  231,    1.50,	 1.0,      60,	8],
        ['MP Jet AC 25/35-20',        3850,     .1,      1.34,   25,      2.54,  216,    1.55,	 1.0,      60,	8],

        ['Motrolfly DM 2205-1350',     1189,     .272,     .5,     9,       .99,  100,    1.2,	 1.2,      35,  10],
        ['Motrolfly DM 2205-1800',     1890,     .110,     .9,    12,       .99,  129,    1.2,	 1.2,      15, 7.0],
        ['Motrolfly DM 2205-2800',     2840,     .095,     .85,   22,       .99,  200,    1.2,	 1.2,      10, 7.0],
        ['Motrolfly DM 2210-1080',      993,     .172,     .51,   15,      1.52,  155,    1.2,	 1.2,      26, 7.0],
        ['Motrolfly DM 2210-1400',     1290,     .095,    1.033,  15,      1.52,  155,    1.2,	 1.2,      26, 7.0],
        ['Motrolfly DM 2210-1700',     1623,     .0621,   1.245,  20,      1.52,  180,    0.97,	 1.8,      10, 7.0],
        ['Motrolfly DM 2210-2200',     2190,     .032,    1.94,   25,      1.52,  250,    1.25,	 1.9,      10, 7.0],
        ['Motrolfly DM 2215-850',       731,     .1522,    .51,   17,      2.07,  162,    1.35,	 1.4,     100, 7.0],
        ['Motrolfly DM 2215-1150',     1080,     .086,     .92,   17,      2.07,  188,    1.35,	 1.7,      17, 7.0],
        ['Motrolfly DMH 2215-3100',    3165,     .078,    1.983,  29,      1.9,   265,    0.8,	 1.2,      10, 7.0],
        ['Motrolfly DMH 2215-3500',    3670,     .045,    2.11,   32,      1.9,   260,    0.9,	 1.5,      10, 6.0],

        ['Multiplex Permax BL-X22-13',1350,    .280,    .45,    12,      1.13,    96,    1.46,	 1.05,     20,  10],
        ['Multiplex Permax BL-X22-18',1790,    .195,    .75,    15,      1.13,    96,    1.44,	 1.05,     20,  10],
        ['Multiplex Permax BL-X22-23',2300,    .080,    .85,    18,      1.13,    96,    1.42,	 1.05,     20,  10],
        ['Multiplex Permax 280 7.2V', 2417,     .553,    .3,   4.5,      1.6,    135,    1.55,	 1.0,      40, 7.2],
        ['Multiplex Permax 280 BB',   4464,     .429,    .7,     8,       1.9,   160,    1.50,	 1.0,      40,	 8],
        ['Multiplex Permax 400 6V',   2946,     .357,    .73,    7,       2.6,   222,    1.55,	 .98,      40,	 6],
        ['Multiplex Permax 400 7.2V', 2268,     .473,    .70,    8,       2.6,   222,    1.55,	 .98,      40, 7.2],
        ['Multiplex Permax 450 Turbo',2189,     .138,    1.2,    25,      4.9,   417,    1.55,	 1.05,     60,	 8],
        ['Multiplex Permax 480 7.2V', 2459,     .312,    .92,    12,      3.3,   280,    1.50,	 1.02,     50, 7.2],

        ['PJS 550 E',                  802,     .1,     1.0,     15,      1.9,   160,    1.35,	 1.1,      40,	8],
        ['PJS 550 R',                 1225,     .22,    1.5,     12,      1.9,   160,    1.45,	 1.1,      40,	8],

        ['Plettenberg Freestyle 20',  1461,     .149,   .93,     12,      2.65,  225,   1.35,	 1.1,      50,	8],
        ['Plettenberg Freestyle 24',  1183,     .240,   .82,     10,      2.65,  225,   1.45,	 1.05,     50,	8],
        ['Plettenberg Freestyle XL',   942,     .095,   1.05,    15,      5.0,    425,    1.55,	 1.05,     60,	8],
        ['Plettenberg Orbit 10-22',   1080,     .064,   1.8,    35,       4.77,  400,    1.30,	 1.1,      60,  11],
        ['Plettenberg Orbit 15-14',   1100,     .035,   2.5,    55,       6.18,  525,    1.35,	 1.1,      60,  11],
        ['Plettenberg Orbit 20-14',    810,     .040,   1.8,    25,       7.59,  645,    1.53,	 1.06,     60,10.5],
        ['Plettenberg Typhoon 6-20',  1600,     .133,   .7,     12,       1.52,  130,    1.41,	 1.2,      60,	8],

        ['Scorpion S-1804-1650',      1700,     .8,     .25,     5,       .42,   33,    1.3,	 1.1,      20, 6.5],
        ['Scorpion S-1805-2250',      2250,     .41,    .25,     7,       .56,   45,    1.3,	 1.1,      20, 6.5],
        ['Scorpion SII-2205-1490',    1500,     .32,    .42,    10,       1.25,  110,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2208-1100',    1105,     .29,    .41,    12,       1.59,  133,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2208-1280',    1285,     .27,    .47,    14,       1.59,  155,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-885',      885,     .29,    .41,    13,       2.05,  192,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-960',      960,     .27,    .51,    13,       2.05,  192,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-1070',    1090,     .25,    .59,    15,       2.05,  222,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-1850',    1850,     .08,   1.31,    22,       2.05,  326,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2215-900',      920,     .27,    .52,    16,       2.42,  237,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2215-1127',    1127,     .1,     .73,    20,       2.42,  296,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2215-1810',    1810,     .058,  1.35,    25,       2.42,  370,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-3008-1090',    1105,     .117,   .79,    26,       3.35,  370,   1.3,	 1.1,     18, 9.15],
        ['Scorpion SII-3008-1220',    1105,     .0971,  .88,    26,       3.35,  425,   1.3,	 1.1,     16,    9],
        ['Scorpion SII-3014-830',      870,     .0732, 1.35,    30,       4.55,  550,   1.3,	 1.1,     15,   10],
        ['Scorpion SII-3014-1040',    1063,     .0589, 1.27,    40,       4.55,  600,   1.3,	 1.1,     15,  9.1],
        ['Scorpion SII-3014-1220',    1237,     .0503, 1.64,    46,       4.55,  640,   1.3,	 1.1,     10,    9],
        ['Scorpion SII-3020-780',      793,     .0598, 1.26,    40,       5.86,  800,   1.3,	 1.1,     17, 10.2],

        ['TowerPro TP2409_12D',       1600,     .071,   1.4,    25,       2.23,  190,    1.50,	 1.05,     40,   8],

        ['Turnigy 2020-3500',         3500,     .262,   .3,     10,       .39,   1.55,    1.5,  1.1,      60, 7.4],
        ['Turnigy C2222-2850',        2850,     .485,   .7,     10,       .53,   1.55,    1.5,  1.1,      60, 7.4],
        ['Turnigy C1826-2400',        2400,     .212,   .4,     10,       .64,   1.55,    1.5,  1.1,      60, 7.4],

        ['Turnigy C3542-1450 14p',    1400,     .044,   1.85,   55,       4.73,  400,    1.45,   1.0,      30, 7.1],
        ['Turnigy L2210C-1200',       1200,     .209,    0.95,  16,      1.69,   150,    1.45,   1.05,     40,  10],
        ['Turnigy 2213-20',            920,     .280,    .75,   19,       2.08,  180,    1.45,   1.05,     40,  12],
        ['Turnigy 2217-16',           1120,     .133,   1.15,   23,       2.51,  210,    1.45,   1.0,      40,11.5],
        ['Turnigy 2217-20',            940,     .190,    .94,   22,       2.51,  210,    1.45,   1.0,      40,12.4],
        ['Turnigy 2826-1650',         1570,     .163,    1.3,   16,       1.59,  135,    1.47,   1.05,     40,  11],
        ['Turnigy 2830-800',           960,     .245,    .86,   14,       2.01,  170,    1.50,   1.05,     10,  12],
        ['Turnigy 42-60 600',          620,     .085,    6.0,   50,       9.81,  830,    1.55,   1.0,      10,  15],
        ['Turnigy 50-45 890',          900,     .060,    2.0,   55,       9.18,  780,    1.55,   1.05,     10,   5],
        ['Turnigy 50-55A 400',         500,     .110,    2.7,   68,      10.59,  900,    1.50,   1.05,     10,  16],
        ['Turnigy 50-55B 600',         550,     .045,    5.0,   80,      10.59,  900,    1.45,   1.05,     10,18.5],
        ['Turnigy 80-100-A 180',       180,     .050,    3.5,  150,      55.41, 4710,    1.50,   1.07,     10,  20],


        ['Uberall Nippy 0508/73',      720,     .422,   .45,     5,       1.34,  115,    1.30,	 1.3,      40,	8],
        ['Uberall Nippy 0808/98',      970,     .255,   .7,      8,       1.4,   120,    1.30,	 1.4,      40,	8],
        ['Uberall Nippy 1208/180',    1700,     .195,   .5,     15,       2.4,   200,    1.30,	 1.4,      40,	8],
        ['Uberall Nippy 1812/100',    1020,     .064,   1.5,    25,       2.2,   190,    1.40,	 1.4,      40,	8],
        ['Uberall Nippy 2510/114',    1140,     .079,   2.0,    25,       2.2,   190,    1.50,	 1.0,      40,	8],

        ['XPWR 30CC',                  214,     .054,   1.2,    60,      18.92,  1600,   1.50,	 1.0,      20,8.4],
        ['XPWR 35CC',                  221,     .024,   2.1,    75,      27.32,  2300,   1.50,	 1.0,      20,8.4],
        ['XPWR 40CC',                  200,     .021,   2.2,    85,      30.75,  2600,   1.50,	 1.0,      20,8.4],
        ['XPWR 60CC',                  190,     .015,   3.0,   120,      41.23,  3500,   1.50,	 1.0,      20,8.4]
        ]
    li_1=[]
##        session['maxcurrent'] =float(request.form['maxcurrent']) a
##        session['maxpower'] =float(request.form['maxpower']) b
##        session['maxweight'] =float(request.form['maxweight']) c
    for i in motorarray: #6power
        if i[6] >b and i[5]>c/28.3495 and i[4]>a:
            li_1.append(i)
    return li_1


@app.route('/About')
def about():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("about_home.html",a='Login',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('about_home.html',a=d.username,b='/database')
    return render_template('about_home.html')

@app.route('/about-home')
def about_home():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("about.html",a='Login',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('about.html',a=d.username,b='/database')
    return render_template('about.html')


@app.route('/overview')
def overview():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("overview.html",a='Login',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('overview.html',a=d.username,b='/database')
    return render_template('overview.html')


@app.route('/contact',methods = ["POST"])
def con():
    if request.method == "POST":
        session['name1']=request.form['name']
        session['message1']=request.form['message']
        session['email1']=request.form['email']
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "choosemydrone@gmail.com"
    password ="Mail_Password"
    message ="Hiiii " + session['name1'] + " " + 'we will contact you soon...'
    message1 =session['name1']+session['message1']+session['email1']
    try:
        receiver_email =session['email1']
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        receiver_email ="wisdomquiz123@gmail.com"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message1)
    except:
        pass
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("index.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('index.html',a=d.username,b='/database')
    return render_template('index.html')

@app.route('/design')
def design():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("design.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('design.html',a=d.username,b='/database')

@app.route('/design/propeller')
def prop():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("propeller.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('propeller.html',a=d.username,b='/database')

@app.route('/outprop',methods = ["POST"])
def outprop():
    if request.method == "POST":
        session['dia']=request.form['dia']
        session['diaunit'] = request.form['diaunit']
        if session['diaunit']=='in':
            propdiameter=float(session['dia'])
        else:
            propdiameter=float(session['dia'])/2.54
        metric_propdiameter=float(propdiameter)*2.54 #in cm
        session['nof']=request.form['nof']
        session['gear']=request.form['gear']
        session['pitch']=request.form['pitch']
        session['tc']=request.form['tc']
        session['pc']=request.form['pc']
        tconst=float(session['tc']) #tconstant
        pconst=float(session['pc']) #pconstant
        session['pu'] = request.form['pu']#pitch unit
        if session['pu']=='p_in':
            proppitch=float(session['pitch'])
        else:
            proppitch=float(session['pitch'])/2.54
        metric_proppitch=proppitch*2.54 #in cm
        #PROPELLER Section:
        propblades=int(session['nof']) #no.of blades
        gearratio=float(session['gear'])
        gear=gearratio
        #Battery Section
        outCellCap=2300 #Cell Capacity
        numcells=3 #series
        par=1 #Parallel
        MaxI=46 #Max Current
        Vcell=3.3 #voltpercell
        metric_outCellOz=72 #Cell Weight g
        outCellOz=2.54 #Cell Weight oz
        outCellRes=0.0089 #Cell Resistance
        outPackOz=7.6#pack weight in oz
        outPackgr=216 #pack weight in g
        outPackV=9.9 #Pack Voltage
        #Electronic Speed Controller ESC SEction
        Resc=0.0025# ESC Resistance
        Amp=20#Max Current
        escoz=0.5#esc weight in oz
        metric_escoz=15 #esc weight in g
        #  MOTOR Section
        outKv=1200 #Kv rpm/m
        outIo=1.2#IO
        outVo=8.2 #motor Voltage
        outRm=0.075 #motor rm
        outKt=1.127 #motor kt
        outIMax=25#motor max power A
        outMotorPwr=165#motor max power w
        motoroz=1.94# weight OZ
        metric_motoroz=55#Weight gram
        MotorKi=1.55 #Default List Values Need to update
        MotorKrpm = 1.01 #Default List Values Need to update
        MotorRk = 60 #Default List Values Need to update
        MotorKv=outKv
        MotorRm=outRm
        #BaaroMeter Section
        temp=59# Temperature
        metric_temp=15 #in celsius
        alt=492 #altitude
        metric_alt=150 #in meter
        baro=29.4#Barometric Pressure inHg
        metric_baro=995#in mbar
        #calculations
        effdiameter = propdiameter * math.pow(propblades/2, .2)
        outEffDiameter=round(effdiameter,2);
        effdiameter=outEffDiameter
        MotorIO = (1*outIo) + ((Vcell*numcells - outVo)/MotorRk)
        if gear > 1:
            gear = gear * .98
        if effdiameter <= 0 or proppitch <= 0:
            Imotor = MotorIO
        else:
            tempg=(baro/29.92)*((460+59)/(460+1*temp)) * pconst * MotorKi * pow(effdiameter,4) * proppitch * (pow(12,-5)*1E-9) *pow((MotorKv/gear),3)
            tempr = (outCellRes * numcells) + (1* Resc) + (1 * MotorRm)
            Vbatt = Vcell * numcells
            tempb = (-2 * tempr * Vbatt - 1 / tempg ) / (tempr * tempr)
            tempc = ( pow(Vbatt,2) + MotorIO / tempg ) / (tempr * tempr)
            if tempb* tempb/4 > tempc:
                tempz = math.sqrt(pow(tempb,2)/4- tempc)
                tempi1 = -tempb/2 + tempz
                tempi2 = -tempb/2 - tempz
                if tempi2 > 0:
                    Imotor = tempi2
            else:
                Imotor = 0
        outImotor = round(Imotor)
        '''if Imotor > outIMax:
            print('Motor Max Current exceeded!')
        if Imotor > Amp:
            print('ESC Max Current exceeded!')
        if Imotor > MaxI:
            print('Battery Max Current exceeded!')'''
        #CalcMotorValues Main Calculations
        metric_motoroz=round(motoroz * 28.34952,1)
        VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * outImotor )+ (1* Resc * outImotor))
        WattsIn = round( VoltsToMotor * outImotor,1)
        MotorRPM = MotorKv * ( VoltsToMotor - ( outImotor * MotorRm *(1 + .039*(pow(outImotor,2))/(metric_motoroz*2)) * MotorKrpm))
        FELoss = VoltsToMotor * MotorIO
        CULoss = pow(outImotor,2) * MotorRm *(1 + .039*(pow(outImotor,2))/(metric_motoroz*2))
        WattsOut = round(WattsIn - (1 * FELoss + CULoss ),2)
        if WattsOut <= 0:
            WattsOut = 0
        PctEff = round((WattsOut / WattsIn) * 100,1)
        if PctEff <= 0:
            PctEff = 0
        Pheat = WattsIn-WattsOut
        outVmotor = round(VoltsToMotor,2)
        outWin = round(WattsIn,1)
        outWout = round(WattsOut,1)
        outPctEff = round(PctEff,1)
        outRPM = round(MotorRPM,0)
        effdiameter = outEffDiameter
        outMotorPwr = 220
        if gearratio <= 0:
            gearratio = 1
        proprpm = MotorRPM / gearratio
##        if (1*outWin) > outMotorPwr:
##            print(" Motor Max Power exceeded!")
        noLoadVoltsToMotor = (1 * Vcell * numcells) - ((1 * outCellRes * numcells * MotorIO )+ (1* Resc * MotorIO))
        noLoadMotorRPM = MotorKv * ( noLoadVoltsToMotor - (MotorIO * MotorRm))
        noLoadproprpm = noLoadMotorRPM / gearratio
        noLoadPitchspeed = noLoadproprpm * proppitch * .00094697
        noLoadmpspeed = noLoadPitchspeed * 1.609344
        try:
            Tgrams = round((baro/29.92)*((460+59)/(460+1*temp)) * tconst * proppitch * pow(effdiameter,3) * pow(proprpm / 1000,2.1) * 28.34952 * .858 / 10000)
        except:
            flash("Error Came Increase RM Valuses")
            return render_template('analyze_drone.html')
        if proppitch/propdiameter > .6:
            Tgrams = round((baro/29.92)*((460+59)/(460+1*temp)) * tconst * propdiameter * .6 * pow(effdiameter,3) * pow(proprpm / 1000,2.1) * 28.34952 * .858 / 10000)
        Tkg = Tgrams / 1000
        Tn = Tkg * 9.80665
        Tlbs = Tn / 4.44822161526
        StaticToz = Tgrams/28.34952
        Propwatts = (baro/29.92)*((460+59)/(460+1*temp)) * pconst * pow(effdiameter/12,4) * (proppitch / 12 ) * pow(proprpm / 1000,3)
        HP = Propwatts / 745.699871582
        Pitchspeed = proprpm * proppitch * .00094697
        mpspeed = Pitchspeed * 1.609344;
        ThrustatSpeed = 16 * 375 * Propwatts / ( 746 * Pitchspeed )
        outmpspeed = round(mpspeed,0)
        outPropRpm = round(proprpm,0)
        outPropSThrust = round(StaticToz,1)
        outPropSThTgrams = round(Tgrams,1)
        ###
        #otPackOz=round(outCellOz * numcells * par,1)
        outPowersysOz = round((( 1 * motoroz) + ( 1 * outPackOz ) + ( 1 * escoz))*1.1,1)
        mspeed = round(1000* (effdiameter*3.1416*.083333333*proprpm*60)/(5280 * pow(temp*1 + 460,.5)*33.4))/1000
        outPitchSpeed = round(Pitchspeed,1)
        outPowersysgr = round(outPowersysOz * 28.34952,0)

        if effdiameter <= 0 or proppitch <= 0:
            Imotor = MotorIO
        outDuration=round( ((outCellCap * par/1000) / Imotor ) * 60 * 0.9, 2)
        '''if 1*outPropSThrust < outPowersysOz :
            print(" Static Thrust < Power System Weight!")
        if  mspeed > .92:
            print("Prop Tip MACH Speed exceeded!")'''
        li1=[]
        len1 = 100
        xmin=round(outIo)
        if outImotor < 10:
            xmax = 20
        if (outImotor > 10) and ( outImotor <= 20):
            xmax = 30
        if (outImotor > 20) and outImotor <= 30:
            xmax = 40
        if (outImotor > 30) and  outImotor <= 40:
            xmax = 60
        if (outImotor > 40) and (outImotor <= 60):
            xmax = 100
        if (outImotor > 60) and  outImotor <= 100:
            xmax = 200
        if (outImotor > 100) and outImotor <= 200:
            xmax = 400
        if (outImotor > 200):
            xmax = 600
        #outoutpower
        for i in range(1,len1):
            x1 = i/(len1)*(xmax-xmin)+xmin
            VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * x1 )+ (1* Resc * x1))
            FELoss = VoltsToMotor * MotorIO
            CULoss = pow(x1,2) * MotorRm *(1 + .039*(pow(x1,2))/(metric_motoroz*2))
            WattsIn = round( VoltsToMotor * x1,1)
            WattsOut = round(WattsIn - (1 * FELoss + CULoss ),2)
            if  WattsOut > 0 :
                y1 = WattsOut
                li1.append([x1, y1])
        Woutmax=max(li1)[0]
        # Motor RPM
        li3=[]
        len3 = 50
        for i in range(xmin,len3+1):
            x3 = i/(len3)*(xmax-xmin)+xmin
            VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * x3 )+ (1* Resc * x3))
            MotorRPM = MotorKv * ( VoltsToMotor - ( x3 * MotorRm *(1 + .039*(pow(x3,2))/(metric_motoroz*2)) * MotorKrpm))
        if MotorRPM > 0:
            y3 = MotorRPM/1000
            li3.append([x3,y3])
        maxrpm=max(li3)[0]
        #efficiency
        len2 = 100;
        li2=[]
        f11=[]
        for i in range(xmin,len2+1):
            x2 = (i / len2) * (xmax - xmin) + xmin
            VoltsToMotor =  1 * Vcell * numcells - (1 * outCellRes * numcells * x2 + 1 * Resc * x2)
            FELoss = VoltsToMotor * MotorIO
            CULoss = pow(x2, 2) * MotorRm * (1 + (0.039 * pow(x2, 2)) / (metric_motoroz * 2))
            WattsIn = round(VoltsToMotor * x2, 1);
            WattsOut = round(WattsIn - (1 * FELoss + CULoss), 2)
            if  WattsOut > 0 :
                y2 = round((WattsOut / WattsIn) * 100, 2)
                li2.append([x2, y2])
                f11.append([x2,x2])
        PctEffmax=max(li2)[0]
        # Motor Heating
        li4=[]
        len4 = 50
        for i in range(xmin,len4+1):
            x4 = i/(len4)*(xmax-xmin)+xmin
            VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * x4 )+ (1* Resc * x4))
            FELoss = VoltsToMotor * MotorIO
            CULoss = pow(x4,2) * MotorRm *(1 + .039*(pow(x4,2))/(metric_motoroz*2))
            WattsIn = round( VoltsToMotor * x4,1)
            WattsOut = round(WattsIn - (1 * FELoss + CULoss ),2)
            if WattsOut > 0:
                y4 = WattsIn-WattsOut
                li4.append([x4,y4])
    l=[['Propeller Static RPM',outPropRpm],['Static Pitch Speed',outmpspeed],['Prop Static Tip Speed',mspeed],['Static Thrust in g',outPropSThTgrams],['Approx Full-Throttle duration',outDuration],['Power System Weight +10% in g ',outPowersysgr]]
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    try:
        func_call=propeller_s(float(session['dia']),float(session['pitch']),float(session['nof']))
    except:
        func_call=[[]]
    if session['email']==None:
        return render_template("outprop1.html",a='Login/signup',b='/login',ls=l,func_call=func_call)
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('outprop1.html',a=d.username,b='/database',ls=l,func_call=func_call)


@app.route('/motor')
@app.route('/design/motor')
def mot():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("motor.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('motor.html',a=d.username,b='/database')

@app.route('/outmotor',methods = ["POST"])
def outmotor():
    if request.method == "POST":
        session['v']=request.form['v']
        session['maxc']=request.form['maxc']
        session['rm']=request.form['rm']
        session['io']=request.form['io']
        session['kv']=request.form['kv']
        try:
            session['an_motor_temp']=request.form['an_motor_temp']
            if session['an_motor_temp']=="celsius":
                session['temp']=request.form['temp']
            elif session['an_motor_temp']=="kelvin":
                session['temp']=request.form['temp']
                session['temp']=float(session['temp'])-273.15
        except:
            session['temp']=request.form['temp']
        try:
            session['ana_motor_weight_unit']=request.form['ana_motor_weight_unit']
            if session['ana_motor_weight_unit']=="gram":
                session['weight']=request.form['weight']
            elif session['ana_motor_weight_unit']=="oz":
                session['weight']=request.form['weight']
                session['weight']=float(session['weight'])*28.3495
        except:
            session['weight']=request.form['weight']
        Bat_no_load_volts=9.10
        Volts_1=float(session['v'])
        Amps_1=float(session['maxc'])
        Rm_1=float(session['rm'])
        Io_1=float(session['io'])
        Kv_1=float(session['kv'])
        Weight_1=float(session['weight'])
        Ambient_T_1=float(session['temp'])
        Esc_own_Amps_1 = 0.02
        BAT_Rm_1=12#LiPo Battery Cell Resistance (Ri)
        winding_temp =106.3
        total = Rm_1 * (1 + 0.00393 * (winding_temp - 20))
        new_Rm_1 = total
        if (Amps_1 * 1.08 < 8.01):
            escAmps = 8
            escRm = 0.0645
        elif (Amps_1 * 1.08 < 12.01):
            escAmps = 12
            escRm = 0.0437
        elif (Amps_1 * 1.08 < 18.01):
            escAmps = 18
            escRm = 0.0298
        elif (Amps_1 * 1.08 < 25.01):
            escAmps = 25
            escRm = 0.022
        elif (Amps_1 * 1.08 < 30.01):
            escAmps = 30
            escRm = 0.0187
        elif (Amps_1 * 1.08 < 40.01):
            escAmps = 40
            escRm = 0.0145
        elif (Amps_1 * 1.08 < 60.01):
            escAmps = 60
            escRm = 0.0103
        elif (Amps_1 * 1.08 < 70.01):
            escAmps = 70
            escRm = 0.0091
        elif (Amps_1 * 1.08 < 80.01):
            escAmps = 80
            escRm = 0.0083
        elif (Amps_1 * 1.08 < 100.01):
            escAmps = 100
            escRm = 0.007
        elif (Amps_1 * 1.08 < 200.01):
            escAmps = 200
            escRm = 0.0045
        elif (Amps_1 * 1.1 < 400.01):
            escAmps = 400
            escRm = 0.0033
        else:
            escAmps = "400"
            escRm = 0.0033
        Esc_loss_1 = round(((Amps_1 * Amps_1 * escRm) + (5 * Esc_own_Amps_1)) * 10) / 10
        total1 = round((Amps_1 * Amps_1 * new_Rm_1) * 10) / 10
        Cu_loss_1 = total1
        Rth1 = 0.4
        Rth2 = 0.4
        correction = 0
        total = (Cu_loss_1 * (Rth1 + Rth2) / Weight_1 * 100)
        total = ((total * 1) + (correction * 1) + (Ambient_T_1 * 1))
        Mot_Temp_1 = total
        total3 = round((Volts_1 * Io_1) * 10) / 10
        Fe_loss_1 = total3
        total1 = round((Amps_1 * Amps_1 * new_Rm_1) * 10) / 10
        Cu_loss_1 = total1
        C_loss = Cu_loss_1
        I_loss = Fe_loss_1
        total = round(((C_loss * 1) + (I_loss * 1)) * 10) / 10
        Mot_loss_1 = total
        total2 = round((Volts_1 * Amps_1) * 10) / 10
        P_in_1 = total2
        total = round(((P_in_1 - Mot_loss_1) / P_in_1 * 100) * 10) / 10
        total = ((total * 1) + 0.0)
        Motor_efficiency_1 = total
        cells = math.ceil(Volts_1 / 3.7)
        total = round((Amps_1 * Amps_1 * BAT_Rm_1 / 1000 * cells) * 10) / 10
        No_load_volts_1 = (Volts_1 * 1) + (Amps_1 * BAT_Rm_1 / 1000 * cells)
        Bat_loss_1 = total
        total = ((Esc_loss_1 * 1) + (Bat_loss_1 * 1) + (Mot_loss_1 * 1))
        Tot_loss_1 = total
        total = round(((P_in_1 - Tot_loss_1) / P_in_1 * 100) * 10) / 10
        sys_eff=total
        total = round((P_in_1 - Tot_loss_1) * 10) / 10
        if (total <= 0):
            total = ""
        if (Cu_loss_1 == "" or Fe_loss_1 == ""):
            total = ""
        P_out_1 = total
        Kv_Si_val = Kv_1 / 60 * 2 * 3.141592654
        Kt_val =  1 / (Kv_Si_val / 1000)
        total_Kt = Kt_val
        total = round(total_Kt * 100) / 100
        Kt_1 = total
        Kt_val = Kt_1
        total = round(Kt_val * Amps_1)
        Torq = total
        Kt_val = Kt_1
        total = (((Kt_val / 1000) / math.sqrt(Rm_1)) * 100) / 100
        Km_1 = total
        drop = ((No_load_volts_1 * 1) - (Volts_1 * 1))
        total = (pow(1-(math.sqrt(( Io_1 * Rm_1 ) / (Volts_1 *1) - (drop * 0))),2) * 1000) / 10
        Maximum_efficiency_1 = total
        total = (math.sqrt((Volts_1 * Io_1) / Rm_1) * 10) / 10
        A_Max_eff = total
        total = (Motor_efficiency_1 / Maximum_efficiency_1 * 1000 / 10);
        if (total >= 100.0):
            total = "100.0"
        pct_Eta=total
        total = (Km_1 * Km_1 / Weight_1 * 1000000)
        Pwr_Dens = total
        try:
            session['analysis_motor']=request.form['analysis_motor']
            r=[['Input_power_watts',P_in_1],['Output_power_watts',P_out_1],['Torque [mN.m]',Torq],['Power_density [Km²/g]',Pwr_Dens],['Motor_max_heat oC',Mot_Temp_1],['Maximum_efficiency',Maximum_efficiency_1],['Copper_Loss   [W] ',C_loss],['Iron_Loss   [W] ',I_loss],['Motor_Losses [W]',Mot_loss_1],['ESC Loss   [W] ',Esc_loss_1],['Battery Loss   [W]',Bat_loss_1],['Total Losses   [W] ',Tot_loss_1],['Kt   [mNm/A]',Kt_1],['Km   [Nm/√Watt]',Km_1],['% of EtaMax',pct_Eta],[' Amps @ EtaMax',A_Max_eff],['System Efficiency',sys_eff]]
            session['email']= request.cookies.get('email')
            session['pass']=request.cookies.get('pass')
            if session['email']==None:
                return render_template("outmotor.html",a='Login/signup',b='/login',ls=r)
            else:
                try:
                    d= user97.query.filter_by(email=session['email']).first()
                except:
                    flash("Error Came Try again")
                    return render_template('signup.html')
                return render_template('outmotor.html',a=d.username,b='/database',ls=r)
        except:

            r=[['Input_power_watts',P_in_1],['Output_power_watts',P_out_1],['Torque [mN.m]',Torq],['Power_density [Km²/g]',Pwr_Dens],['Motor_max_heat oC',Mot_Temp_1],['Maximum_efficiency',Maximum_efficiency_1]]
            session['email']= request.cookies.get('email')
            session['pass']=request.cookies.get('pass')
            try:
                func_para=motor_s(float(session['v']),float(session['maxc']),float(session['weight']))
            except:
                func_para=[[]]
            if session['email']==None:
                return render_template("outmotor1.html",a='Login/signup',b='/login',ls=r,func_para=func_para)
            else:
                try:
                    d= user97.query.filter_by(email=session['email']).first()
                except:
                    flash("Error Came Try again")
                    return render_template('signup.html')
                return render_template('outmotor1.html',a=d.username,b='/database',ls=r,func_para=func_para)

@app.route('/esc')
@app.route('/design/esc')
def ec():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("desc.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('desc.html',a=d.username,b='/database')
@app.route('/outesc',methods = ["POST"])
def outesc():
    session['maxcc']=request.form['maxcc']
    session['weight1']=request.form['weight1']
    session['weight2']=request.form['weight2']
    session['min_d']=request.form['max_d']
    session['max_d']=request.form['max_d']
    if session['max_d']=='moz':
        session['weight2']=float(float(session['weight2'])*0.035274)
    else:
        pass
    if session['min_d']=='oz':
        session['weight1']=float(float(session['weight1'])*0.035274)
    else:
        pass
    esc =[['Airtronics 96334', 0.0025, 20, 0.5, 14.175],
          ['Astro 204', 0.005, 50, 1.1, 31.185000000000006],
          ['Astro 204D', 0.002, 60, 1.06, 30.051000000000002],
          ['Astro 210', 0.003, 45, 0.74, 20.979],
          ['Astro 211', 0.002, 75, 0.89, 25.2315],
          ['Astro 215', 0.003, 30, 0.32, 9.072000000000001],
          ['Astro 217', 0.005, 30, 0.53, 15.025500000000001],
          ['Astro 217D', 0.003, 35, 0.53, 15.025500000000001],
          ['Astro 800', 0.02, 15, 0.7, 19.845],
          ['Astro 801', 0.01, 25, 0.8, 22.680000000000003],
          ['Astro 805', 0.012, 30, 0.75, 21.262500000000003],
          ['Aveox A-15', 0.0036, 15, 0.2, 5.670000000000001],
          ['Aveox A-55', 0.0018, 55, 0.3, 8.505],
          ['Aveox EZ30', 0.014, 30, 1.6, 45.36000000000001],
          ['Aveox H160', 0.007, 60, 2.0, 56.7],
          ['Aveox H160C/CM', 0.0057, 70, 2.0, 56.7],
          ['Aveox H260', 0.007, 60, 2.0, 56.7],
          ['Aveox H260C/CM', 0.0057, 70, 2.0, 56.7],
          ['Aveox H360C/CM', 0.004, 90, 2.0, 56.7],
          ['Aveox L130', 0.0014, 35, 1.6, 45.36000000000001],
          ['Aveox L160', 0.007, 60, 2.0, 56.7],
          ['Aveox L160C/CM', 0.004, 70, 2.0, 56.7],
          ['Aveox L260', 0.007, 60, 2.0, 56.7],
          ['Aveox L260C/CM', 0.004, 70, 2.0, 56.7],
          ['Aveox L360C/CM', 0.004, 90, 4.0, 113.4],
          ['Aveox M160', 0.007, 60, 2.0, 56.7],
          ['Aveox M160C/CM', 0.004, 70, 2.0, 56.7],
          ['Aveox SH-24', 0.0028, 25, 1.7, 48.195],
          ['Aveox SH-48', 0.0028, 40, 1.7, 48.195],
          ['Aveox SH-48 BEC', 0.0028, 45, 1.7, 48.195],
          ['C. Creations Dragon 35', 0.0055, 35, 0.8, 22.680000000000003],
          ['C. Creations Dragon 55', 0.0023, 55, 1.2, 34.02],
          ['C. Creations Griffin 40', 0.0012, 40, 0.9, 25.515],
          ['C. Creations Griffin 50', 0.0011, 50, 0.75, 21.262500000000003],
          ['C. Creations Griffin 55', 0.001, 55, 1.0, 28.35],
          ['C. Creations Pegasus 35', 0.0015, 35, 0.75, 21.262500000000003],
          ['C. Creations Phoenix 10', 0.0013, 10, 0.21, 5.9535],
          ['C. Creations Phoenix 25', 0.0065, 25, 0.37, 10.4895],
          ['C. Creations Phoenix 35', 0.0045, 35, 0.9, 25.515],
          ['C. Creations Phoenix 45', 0.0026, 45, 1.0, 28.35],
          ['C. Creations Phoenix 60', 0.0012, 60, 2.0, 56.7],
          ['C. Creations Phoenix 80', 0.001, 80, 2.1, 59.535000000000004],
          ['C. Creations Phoenix 125', 0.0006, 125, 3.2, 90.72000000000001],
          ['C. Creations Pixie 14', 0.0045, 14, 0.3, 8.505],
          ['C. Creations Pixie 20P', 0.0025, 20, 0.3, 8.505],
          ['C. Creations Pixie 7', 0.009, 7, 0.11, 3.1185],
          ['C. Creations Pixie 7P', 0.007, 7, 0.1, 2.8350000000000004],
          ['C. Creations Pixie Lite', 0.0045, 14, 0.07, 1.9845000000000004],
          ['C. Creations Sprite 20', 0.004, 20, 0.4, 11.340000000000002],
          ['C. Creations Sprite 25', 0.0025, 25, 0.5, 14.175],
          ['C. Creations ThunderBird 18', 0.0065, 18, 0.6, 17.01],
          ['C. Creations ThunderBird 36', 0.0049, 36, 0.71, 20.1285],
          ['C. Creations ThunderBird 54', 0.0049, 54, 1.2, 34.02],
          ['Great Planes C05', 0.011, 5, 0.21, 5.9535],
          ['Great Planes C10', 0.0055, 10, 0.27, 7.6545000000000005],
          ['Great Planes C20', 0.0036, 20, 0.6, 17.01],
          ['Great Planes C30', 0.0028, 30, 0.7, 19.845],
          ['Great Planes C50', 0.0018, 50, 1.2, 34.02],
          ['G. Planes Electrifly BL-8', 0.013, 8, 0.42, 11.907],
          ['G. Planes Electrifly BL-12', 0.0075, 12, 0.42, 11.907],
          ['G. Planes Electrifly SS-8', 0.05, 8, 0.39, 11.056500000000002],
          ['G. Planes Electrifly SS-12', 0.03, 12, 0.49, 13.8915],
          ['G. Planes Electrifly SS-25', 0.015, 25, 0.92, 26.082],
          ['G. Planes Electrifly SS-35', 0.01, 35, 1.13, 32.0355],
          ['G. Planes Electrifly SS-45', 0.008, 45, 1.76, 49.896],
          ['Hacker 06-3P', 0.012, 6, 0.42, 11.907],
          ['Hacker 18-3P', 0.007, 18, 0.53, 15.025500000000001],
          ['Jeti 08-3P', 0.0013, 8, 0.55, 15.592500000000003],
          ['Jeti 150', 0.003, 140, 1.9, 53.865],
          ['Jeti eco', 0.003, 18, 0.71, 20.1285],
          ['Jeti 30-3P', 0.004, 30, 1.0, 28.35],
          ['Jeti Advance 70-3P Opto', 0.003, 70, 1.34, 37.989000000000004],
          ['Jeti JES 350', 0.003, 35, 0.6, 17.01], ['Jeti JES 020', 0.003, 20, 0.53, 15.025500000000001],
          ['Jeti JES 18-3P', 0.003, 18, 0.53, 15.025500000000001],
          ['Jeti 77 Opti', 0.001, 77, 2.0, 56.7],
          ['Jomar Mini-Max', 0.014, 30, 1.2, 34.02],
          ['Jomar Sport-Max', 0.009, 40, 1.4, 39.69],
          ['Kontronik 3SL 70-6-18', 0.004, 70, 1.24, 35.154],
          ['Kontronik Beat 40-6-12', 0.0056, 40, 1.17, 33.1695],
          ['Kontronik Beat 55-6-18', 0.0043, 55, 1.17, 33.1695],
          ['Kontronik Beat 70-6-12', 0.0021, 70, 1.3, 36.855000000000004],
          ['Kontronik Beat 80-6-18', 0.0021, 80, 1.32, 37.422000000000004],
          ['Kontronik Smile 40-6-12', 0.0056, 40, 1.3, 36.855000000000004],
          ['Master 70 B Flight', 0.001, 105, 1.41, 39.9735],
          ['MaxCim Maxu35A-21', 0.015, 60, 3.0, 85.05000000000001],
          ['MaxCim Maxu35A-25NB', 0.013, 65, 3.0, 85.05000000000001],
          ['MaxCim Maxu35C-21', 0.009, 65, 3.0, 85.05000000000001],
          ['MaxCim Maxu35C-25NB', 0.012, 65, 3.0, 85.05000000000001],
          ['Medusa Fusion ESC-2430BB', 0.0013, 30, 1.48, 41.958],
          ['Medusa Fusion ESC-2440BB', 0.001, 40, 1.63, 46.210499999999996],
          ['Medusa Fusion ESC-2450BB', 0.0008, 50, 1.66, 47.061],
          ['Medusa Spectrum ESC-1210BB', 0.004, 10, 0.39, 11.056500000000002],
          ['Medusa Spectrum ESC-1218BB', 0.002, 10, 0.64, 18.144000000000002],
          ['Medusa Spectrum ESC-1230BB', 0.0013, 30, 0.99, 28.0665],
          ['Medusa Spectrum ESC-1240BB', 0.001, 40, 1.17, 33.1695], ['Medusa Spectrum ESC-1250BB', 0.0008, 50, 1.24, 35.154], ['MGM ComPro 2512-3', 0.0039, 25, 0.71, 20.1285], ['MGM 1210', 0.0126, 12, 0.39, 11.056500000000002], ['MGM 4012', 0.0026, 40, 1.17, 33.1695], ['Microdrive M10P', 0.014, 10, 0.71, 20.1285], ['Microdrive M20P', 0.0035, 20, 0.71, 20.1285], ['Microdrive M30P', 0.0018, 40, 1.24, 35.154], ['NES-050', 0.025, 4, 0.14, 3.9690000000000007], ['NES-110', 0.02, 11, 0.57, 16.159499999999998], ['NES-140-compact', 0.02, 14, 0.57, 16.159499999999998], ['NES-180', 0.009, 18, 0.6, 17.01], ['NES-350', 0.004, 35, 0.88, 24.948], ['RipMax Xtra 05', 0.011, 5, 0.21, 5.9535], ['RipMax Xtra 12', 0.0055, 12, 0.28, 7.9380000000000015], ['RipMax Xtra 22', 0.0038, 22, 0.6, 17.01], ['RipMax Xtra 30', 0.0028, 30, 0.74, 20.979], ['RipMax Xtra 40', 0.0018, 40, 1.2, 34.02], ['RipMax Xtra 50', 0.0014, 50, 1.34, 37.989000000000004], ['RipMax Xtra 60', 0.0011, 60, 1.24, 35.154], ['Schulze future-11.20e', 0.008, 20, 0.62, 17.577], ['Schulze future-11.30e', 0.007, 30, 0.72, 20.412], ['Schulze future-11.40Ke', 0.004, 40, 1.24, 35.154], ['Schulze future-11.40KWe', 0.004, 40, 1.31, 37.1385], ['Schulze future-12.36e', 0.007, 36, 1.45, 41.1075], ['Schulze future-12.46e', 0.0046, 46, 1.45, 41.1075], ['Schulze future-12.46We', 0.0046, 46, 1.48, 41.958], ['Schulze future-12.97Fe', 0.0016, 97, 1.55, 43.9425], ['Schulze future-18.129F', 0.0004, 129, 1.55, 43.9425], ['Schulze future-18.129FW', 0.0008, 129, 1.59, 45.0765], ['Schulze future-18.36', 0.007, 36, 1.17, 33.1695], ['Schulze future-18.46K', 0.0046, 46, 1.45, 41.1075], ['Schulze future-18.46WK', 0.0046, 50, 1.66, 47.061], ['Schulze future-18.61', 0.0026, 61, 1.27, 36.0045], ['Schulze future-18.97F', 0.0016, 97, 1.55, 43.9425], ['Schulze future-18.97FW', 0.0016, 97, 1.59, 45.0765], ['Schulze future-18.97KFW', 0.0016, 97, 2.58, 73.143], ['Schulze future-24.40K', 0.006, 40, 1.45, 41.1075], ['Schulze future-24.89F', 0.001, 89, 1.55, 43.9425], ['Schulze future-32.170W', 0.0018, 170, 6.89, 195.3315], ['Schulze future-32.28K', 0.016, 28, 1.45, 41.1075], ['Schulze future-32.40K', 0.0074, 40, 1.45, 41.1075], ['Schulze future-32.55', 0.0054, 55, 1.7, 48.195], ['Schulze future-32.55WK', 0.0054, 62, 2.12, 60.102000000000004], ['Schulze future-32.80F', 0.0024, 80, 1.55, 43.9425], ['Schulze future-32.80FWK', 0.0024, 95, 2.23, 63.2205], ['Schulze future-40.70', 0.0036, 70, 1.8, 51.03], ['Schulze future-40.70WK', 0.0036, 83, 2.51, 71.1585], ['Schulze future-9.06ek', 0.033, 6, 0.21, 5.9535], ['Schulze future-9.12ek', 0.015, 12, 0.21, 5.9535], ['Schulze future-25b', 0.005, 25, 0.6, 17.01], ['Schulze future-45be', 0.0022, 45, 1.48, 41.958], ['Schulze mcf31-47be', 0.0033, 47, 0.74, 20.979], ['Schulze mcf31-47bo', 0.0033, 47, 0.74, 20.979], ['Schulze mcf31-52bo', 0.0027, 52, 0.74, 20.979], ['Schulze mcf43-110bo', 0.002, 110, 1.17, 33.1695], ['Schulze mcf43-70be', 0.0025, 70, 1.17, 33.1695], ['Schulze mcf43-75bo', 0.002, 75, 1.17, 33.1695], ['Schulze smart-47bo', 0.0033, 47, 0.74, 20.979], ['Schulze smart-52bo', 0.0027, 47, 0.74, 20.979], ['Schulze smart-70be', 0.0025, 70, 1.17, 33.1695], ['Schulze smart-75be', 0.002, 75, 1.17, 33.1695], ['Stefan 1-Fet BEC', 0.01, 12, 0.9, 25.515], ['Stefan 4-Fet BEC Brake', 0.0025, 48, 1.2, 34.02], ['Stefan 4-Fet Brake', 0.007, 40, 1.0, 28.35], ['Stefan Light 1-Fet BEC', 0.01, 12, 0.6, 17.01],
          ['TMM 40', 0.0025, 40, 1.55, 43.9425]]
    current=float(session['maxcc'])
    min_weight=float(session['weight1'])
    max_weight=float(session['weight2'])
    c=[]
    w=[]
    for i in esc:
        if i[2]<=current:
            c.append(i)
            if i[-1]>min_weight and i[-1]<max_weight:
                w.append(i)
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("suggest_esc.html",a='Login/signup',b='/login',books=w)
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('suggest_esc.html',a=d.username,b='/database',books=w)
@app.route('/design/battery')
def battery():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("battery.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('battery.html',a=d.username,b='/database')

@app.route('/battery',methods = ["POST","GET"])
@app.route('/analysis/battery1',methods = ["POST","GET"])
def battery1():
    if request.method == "POST":
        session['mah1']=float(request.form['mah1'])
        session['ds']=float(request.form['ds'])
        session['dc']=float(request.form['dc'])
        x=(session['mah1']/session['dc'])*1-(session['ds']/100)
        ls=[["Battery Hours",x]]
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template("stall_out.html",a='Login/signup',b='/login',ls=ls)
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('stall_out.html',a=d.username,b='/database',ls=ls)
    else:
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template("analysis_battery_form.html",a='Login/signup',b='/login')
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('analysis_battery_form.html',a=d.username,b='/database')



@app.route('/outbattery',methods = ["POST"])
def outbattery():
    if request.method == "POST":
                #[Cap,     Res,     Wgt,     Volt,   MaxI],
        da = [
        ['A123 - 2300 LiNP 15/20C',        2300,   .009,     2.54,    3.3,     46],
        ['AnyRc Lipo 1700',                1700,   .06,      1.4,     3.7,	0],
        ['Apogee 830',                      850,   .012,     .61,     3.7,      0],
        ['Apogee 1050',                    1050,   .012,     .76,     3.7,	0],
        ['Apogee 1570',                    1570,   .012,     1.27,    3.7,	0],
        ['Apogee 2480',                    2480,   .012,     1.67,    3.7,	0],
        ['BlackLine 1700 35C',             1700,   .0089,     1.16,   3.7,     60],
        ['BlackLine 2200 35C',             2200,   .0071,     2.05,   3.7,     77],
        ['BlackLine 2600 35C',             2600,   .0058,     2.47,   3.7,     91],
        ['BlackLine 3200 35C',             3200,   .0048,     3.39,   3.7,    112],
        ['BlackLine 3800 35C',             3800,   .0038,     3.60,   3.7,    133],
        ['BlackLine 4400 35C',             4400,   .0033,     4.31,   3.7,    154],
        ['Dualsky XPower 1000 16C',        1000,   .035,      0.92,   3.7,     33],
        ['Dualsky XPower 1000 25C',        1000,   .030,      1.06,   3.7,     25],
        ['Dualsky XPower 2200 25C',        1000,   .009,      1.94,   3.7,     55],
        ['Dualsky XPower 2200 16C',        2200,   .013,      1.77,   3.7,     33],

        ['Dymond XS-1350 22C',             1350,   .017,      2.73,   3.7,     31],
        ['Dymond XS-1700 22C',             1700,   .015,      1.73,   3.7,     38],
        ['Dymond XC-2250 22C',             2250,   .0148,     2.26,   3.7,     38],
        ['Dymond ZC-2500 30C',             2500,   .0065,     2.4,    3.7,     60],
        ['Dymond XC-3200 30C',              3200,  .006,      3.32,   3.7,     80],
        ['ePower 450 15/20C',               450,   .0276,    .353,    3.7,	9],
        ['ePower 700 12/18C',               700,   .0336,    .493,    3.7,     12],
        ['ePower 1000HP 10/16C',           1000,   .044,     .847,    3.7,     16],
        ['ePower 1000HPT 12/18C',          1000,   .015,     .883,    3.7,     18],
        ['ePower 1200XP 15/25C',           1200,   .015,     1.01,    3.7,     30],
        ['ePower 1250HPT 12/15C',          1250,   .015,     .953,    3.7,     19],
        ['ePower 1500XP 15/25C',           1500,   .012,     1.34,    3.7,     38],
        ['ePower 1700HP 10/15C',           1700,   .025,     1.34,    3.7,     26],
        ['ePower 1800XP 15/25C',           1800,   .01,      1.586,   3.7,     45],
        ['ePower 2500XP 15/25C',           2500,   .0096,    2.256,   3.7,     63],
        ['ePower 3700XP 15/25C',           3700,   .0049,    3.35,    3.7,     93],
        ['ePower 5000XP 15/25C',           5000,   .0032,    4.234,   3.7,    125],
        ['E-Tec ET-0250',                   250,   .09,      .2,      3.7,	0],
        ['E-Tec ET-0700',                   700,   .042,     .53,     3.7,	0],
        ['E-Tec ET-1200',                  1200,   .033,     .85,     3.7,	0],
        ['E-Tec ET-1200HD',                1200,   .032,     .93,     3.7,	0],
        ['FlightPower 400 20C',	            400,   .0037,    .65,     3.7,	8],
        ['FlightPower 800 20C',	            800,   .0023,    .85,     3.7,     16],
        ['FlightPower 1200 20C',	   1200,   .0125,    1.27,    3.7,     24],
        ['FlightPower 1500 20C',	   1500,   .0098,    1.27,    3.7,     30],
        ['FlightPower 1800 20C',	   1800,   .0063,    1.71,    3.7,     36],
        ['FlightPower 2100 20C',	   2100,   .01,      2.24,    3.7,     42],
        ['FlightPower 2500 20C',	   2500,   .0065,    2.51,    3.7,     50],
        ['FlightPower 3300 20C',	   3300,   .0038,    3.34,    3.7,     66],
        ['FlightPower 3700 20C',	   3700,   .0037,    3.5,     3.7,     74],
        ['Gold Peak GP750 NiMH',	    750,   .06,       .5,    1.25,	0],
        ['Gold Peak GP3300 NiMH 12C',	   3300,   .005,     2.19,   1.25,     40],
        ['Gold Peak GP3700 NiMH 12C',	   3700,   .005,     2.4,    1.25,     45],
        ['G. Planes Electrifly 300 20C',    300,   .06,       .28,    3.7,	6],
        ['G. Planes Electrifly 640 20C',    640,   .022,      .6,     3.7,     13],
        ['G. Planes Electrifly 910 20C',    910,   .018,      .88,    3.7,     18],
        ['G. Planes Electrifly 1250 20C',  1250,   .0115,    1.02,    3.7,     25],
        ['G. Planes Electrifly 1500 20C',  1500,   .011,     1.23,    3.7,     30],
        ['G. Planes Electrifly 2100 20C',  2100,   .0075,    1.83,    3.7,     42],
        ['G. Planes Electrifly 3200 20C',  3200,   .0045,    2.75,    3.7,     64],
        ['G. Planes Electrifly 5000 20C',  5000,   .003,     4.3,     3.7,    100],
        ['Hecell HE23AF 1050 NiMH',        1050,   .025,      .71,   1.25,	0],
        ['Hecellusa 1100 NiMH',            1100,    .01,      .7,    1.25,	0],
        ['Hyperion HP-LVX 0300 20C',        300,   .056,      .32,    3.7,	6],
        ['Hyperion HP-LCL 0350 26C',        350,   .073,      .4,     3.7,	9],
        ['Hyperion HP-LVX 0400 20C',        400,   .042,      .46,    3.7,	8],
        ['Hyperion HP-LVX 0800 20C',        800,   .021,      .53,    3.7,     16],
        ['Hyperion HP-LCL 0950 25C',        950,   .027,      .98,    3.7,     24],
        ['Hyperion HP-LVX 1200 20C',       1200,   .014,      1.13,   3.7,     24],
        ['Hyperion HP-LVX 1500 20C',       1500,   .011,      1.34,   3.7,     30],
        ['Hyperion HP-LVX 1800 20C',       1800,   .0093,     1.5,    3.7,     36],
        ['Hyperion HP-LVX 2000 20C',       2000,   .0084,     1.64,   3.7,     40],
        ['Hyperion HP-LVX 2100 20C',       2100,   .008,      1.88,   3.7,     42],
        ['Hyperion HP-LCL 2100 16C',       2100,   .012,      1.43,   3.7,     34],
        ['Hyperion HP-LVX 2200 20C',       2200,   .0076,     1.98,   3.7,     44],
        ['Hyperion HP-LVX 2500 20C',       2500,   .0067,     2.17,   3.7,     50],
        ['Hyperion HP-LVX 3300 20C',       3300,   .0005,     2.89,   3.7,     66],
        ['Hyperion HP-LVX 3700 20C',       3700,   .0045,     3.16,   3.7,     74],
        ['Hyperion HP-LVX 4350 20C',       4350,   .0038,     3.69,   3.7,     87],
        ['Hyperion HP-LCL 4000 20C',       2100,   .0064,    3.65,    3.7,     80],
        ['Hyperion HP-LCL 4200 16C',       4200,   .0061,    3.2,     3.7,     67],
        ['Hyperion HP-LCL 4800 20C',       4800,   .0053,    4.32,    3.7,     96],
        ['Hyperion HP-LVX 5000 20C',       5000,   .0033,    4.3,     3.7,    100],
        ['Kokam 145 8C',		    145,   .019,     .12,     3.7,    1.2],
        ['Kokam 340',                       340,   .02,      .36,     3.7,	0],
        ['Kokam 360SHD 20C',                360,   .0688,    .39,     3.7,    7.2],
        ['Kokam 630',                       630,   .04,      .58,     3.7,	0],
        ['Kokam 640SHD 15C',                640,   .044,     .6,      3.7,    9.6],
        ['Kokam 730SHD 20C',                730,   .0257,    .74,     3.7,     15],
        ['Kokam 910SHD 15C',                920,   .0275,    .81,     3.7,     14],
        ['Kokam 1020',                     1020,   .06,      .72,     3.7,	0],
        ['Kokam 1100 5C',		   1100,   .02,      11.1,    3.7,    5.5],
        ['Kokam 1200 2C',		   1200,   .06,      .82,     3.7,    4.2],
        ['Kokam 1250 15C', 		   1250,   .012,     1.16,    3.7,     19],
        ['Kokam 1250 20C',		   1250,   .027,     1.26,    3.7,     25],
        ['Kokam 1500',		           1500,   .027,     1.15,    3.7,	0],
        ['Kokam 1500 10C',		   1500,   .017,     1.15,    3.7,     15],
        ['Kokam 1500 2S',                  1500,   .015,     1.24,    3.7,	0],
        ['Kokam 1500 8/16C',               1500,   .019,     1.15,    3.7,     24],
        ['Kokam 2000 10C',		   2000,   .017,     1.62,    3.7,     20],
        ['Kokam 2000 15/30C',              2000,   .012,     1.79,    3.7,     60],
        ['Kokam 2000SHD 15C',              2000,   .0178,    1.84,    3.7,     30],
        ['Kokam 2100 20/40C',		   2100,   .01,      2.41,    3.7,     84],
        ['Kokam 2100SHD 20C',              2100,   .0114,    2.37,    3.7,     42],
        ['Kokam 3100 5C',		   3100,   .02,      3.03,    3.7,     16],
        ['Kokam 3200 20C', 		   3200,   .01,      2.91,    3.7,     64],
        ['Kokam 3200SHD 20C',	           3200,   .008,     2.83,    3.7,     64],
        ['Kokam 3200H5 25C',	           3200,   .004,     3.14,    3.7,     80],
        ['Kokam 4000H 20C',	           4000,   .0025,    3.67,    3.7,     80],
        ['Kokam 4000H5 20/25C',	           4000,   .0025,    3.67,    3.7,    100],
        ['Kokam 4800H 15C',	           4000,   .0034,    4.06,    3.7,     75],
        ['Kokam 5000H 25C',	           5000,   .0025,    4.59,    3.7,    125],
        ['Lipoly.de 1800',                 1800,   .0183,    1.45,    3.7,	0],
        ['LiteStorm  350CL 20/30C',	    350,   .028,     .46,     3.7,   10.5],
        ['LiteStorm  950CL 20/30C',	    950,   .0145,    .917,    3.7,     29],
        ['LiteStorm 1200VX 20/25C',	   1200,   .015,     1.165,   3.7,     30],
        ['LiteStorm 1600CL 20/30C',	   1600,   .0113,    1.305,   3.7,     48],
        ['LiteStorm 2100CL 16/22C',	   2100,   .01,	     1.587,   3.7,     46],
        ['LiteStorm 2100VX 20/25C',	   2100,   .01,	     1.975,   3.7,     53],
        ['LiteStorm 2200VX 20/25C',	   2200,   .009,     2.045,   3.7,     55],
        ['LiteStorm 2500CL 20/30C',	   2500,   .008,     2.221,   3.7,     75],
        ['LiteStorm 2500VX 20/25C',	   2500,   .007,     2.224,   3.7,     63],
        ['LiteStorm 3200CL 20/30C',	   3200,   .0075,    2.892,   3.7,     96],
        ['LiteStorm 4000CL 20/30C',	   4000,   .0045,    3.705,   3.7,    120],
        ['LiteStorm 4350VX 20/25C',	   4350,   .0042,    3.88,    3.7,    109],
        ['LiteStorm 4800CL 20/30C',	   4800,   .0042,    4.41,    3.7,    144],
        ['LiteStorm 5000VX 20/25C',	   5000,   .0032,    4.445,   3.7,    125],
        ['Litronics 2200 25C',	           2200,   .0087,    1.98,     3.7,    44],
        ['Litronics 2500 25C',	           2200,   .007,     2.37,     3.7,    50],
        ['Litronics 3200 25C',	           3200,   .0055,    3.18,     3.7,    64],
        ['Litronics 5000 22C',	           5000,   .0038,    4.45,     3.7,   100],
        ['Panasonic 2000 NiMH',            1950,   .0055,    1.48,   1.25,	0],
        ['Panasonic 3000 NiMH',            2900,   .0055,    2.01,   1.25,	0],
        ['Panasonic 3000 Sq NiMH',         3300,   .0055,    2.43,   1.25,	0],
        ['Panasonic HHR150AA',             1500,   .02,      .92,    1.25,	0],
        ['Panasonic HHR300SCU',            3000,   .004,     1.94,   1.25,	0],

        ['Panasonic NCR18650GA 3500',      3500,   .025,     1.67,    3.7,     10],
        ['Panasonic NCR20700B  4250',      3500,   .020,     2.24,    3.7,     15],

        ['Poly-Quest 300',                  300,   .216,     .3,      3.7,	0],
        ['Poly-Quest 300XP 20C',            300,   .098,     .32,     3.7,	6],
        ['Poly-Quest 400XP 15C',            400,   .075,     .49,     3.7,	6],
        ['Poly-Quest 800XP 13C',            800,   .038,     .78,     3.7,     10],
        ['Poly-Quest 880',                  880,   .0813,    .64,     3.7,	0],
        ['Poly-Quest 1200XP 15C',          1200,   .018,     .99,     3.7,     18],
        ['Poly-Quest 1800',                1800,   .0287,    1.48,    3.7,	0],
        ['Poly-Quest 1800XP 15C',          1800,   .012,     1.45,    3.7,     27],
        ['Poly-Quest 2000XQ 20C',          2000,   .006,     1.87,    3.7,     40],
        ['Poly-Quest 2100XP 15C',          2100,   .012,     1.66,    3.7,     32],
        ['Poly-Quest 2150XP 15C',          2150,   .010,     1.84,    3.7,     32],
        ['Poly-Quest 2500XP 15C',          2500,   .0085,    2.12,    3.7,     38],
        ['Poly-Quest 2600',                2600,   .0221,    1.92,    3.7,	0],
        ['Poly-Quest 3200XQ 20C',          3200,   .004,     3.07,    3.7,     64],
        ['Poly-Quest 3300XP 15C',          3300,   .006,     2.68,    3.7,     50],
        ['Poly-Quest 3500',	           3500,   .0108,    2.86,    3.7,	0],
        ['Poly-Quest 3700XP 15C',          3700,   .0055,    3.0,     3.7,     56],
        ['Poly-Quest 3800Mn 15C',          3800,   .0041,    3.71,    3.7,     57],
        ['Poly-Quest 4400',                4400,   .0107,    3.15,    3.7,	0],
        ['Poly-Quest 4500XQ 20C',          4500,   .0035,    4.41,    3.7,     90],
        ['Poly-Quest 5000XP 15C',          5000,   .0026,    4.59,    3.7,     75],
        ['Poly-Quest 6000XP 15C',          6000,   .0024,    6.14,    3.7,     90],
        ['Radio Shack 700 NiMH',           750,    .03,      .46,    1.25,	0],
        ['Radio Shack 1420 NiMH',         1380,   .0235,    .85,     1.25,	0],
        ['Radio Shack 1800 NiMH',         1800,   .022,     .92,     1.25,	0],
        ['Rhino 1750 25C',                1750,   .015,     1.64,    3.7,      44],
        ['Rhino 2150 20C',                2150,   .009,     2.12,    3.7,      43],
        ['Rhino 2350 20C',                2350,   .006,     2.37,    3.7,      69],
        ['RockAmp ACF3 1700 30C',         1700,   .0085,    1.55,    3.7,      51],
        ['RockAmp ACF3 2200 30C',         2200,   .0068,    2.05,    3.7,      66],
        ['RockAmp ACF3 2500 30C',         2500,   .0059,    2.29,    3.7,      75],
        ['RockAmp ACF3 4400 30C',         4400,   .0038,    4.24,    3.7,     110],
        ['Saft 3000 NiMH',                2600,   .009,     2.05,    1.25,	0],

        ['Sanyo 50AAA',                     50,   .055,     .14,     1.25,	0],
        ['Sanyo 110AA',                    110,   .03,      .25,     1.25,	0],
        ['Sanyo 250AAA',                   250,   .024,     .39,     1.25,	0],
        ['Sanyo 270AA',                    270,   .015,     .49,     1.25,	0],
        ['Sanyo 500AR',                    500,   .009,     .67,     1.25,	0],
        ['Sanyo 600AA',                    600,   .012,     .81,     1.25,	0],
        ['Sanyo 600AE',                    600,   .01,      .63,     1.25,	0],
        ['Sanyo 700AR',                    700,   .007,     .99,     1.25,	0],
        ['Sanyo 720AAA NiMH',              720,   .04,      .44,     1.25,	0],
        ['Sanyo 800AR',                    800,   .006,     1.17,    1.25,	0],
        ['Sanyo 1000AE',                  1000,   .008,     1.09,    1.25,	0],
        ['Sanyo 1000AAU',                 1000,   .018,     .81,     1.25,	0],
        ['Sanyo 1000SCR',                 1000,   .0045,    1.48,    1.25,	0],
        ['Sanyo 1100AAE',                 1100,   .0135,    1.17,    1.25,	0],
        ['Sanyo 1100AE',                  1100,   .009,     .99,     1.25,	0],
        ['Sanyo 1100SCR',                 1100,   .0043,    1.52,    1.25,	0],
        ['Sanyo 1250SCR',                 1250,   .005,     1.5,     1.25,	0],
        ['Sanyo CP-1300SCR',      	  1300,   .0074,    1.16,    1.25,	0],
        ['Sanyo 1400AE',                  1400,   .0115,    1.09,    1.25,	0],
        ['Sanyo 1400SCR',                 1400,   .004,     1.86,    1.25,	0],
        ['Sanyo 1700SCR',                 1700,   .004,     1.89,    1.25,	0],
        ['Sanyo 1700SCRC',                1700,   .004,     1.91,    1.25,	0],
        ['Sanyo 1900SCR',                 1900,   .004,     1.96,    1.25,	0],
        ['Sanyo RC2000',                  2000,   .0035,    1.99,    1.25,	0],
        ['Sanyo 2000SCR',                 2000,   .004,     2.05,    1.25,	0],
        ['Sanyo 2200 NiMH',               2000,   .006,     1.4,     1.25,	0],
        ['Sanyo RC2400',                  2400,   .0032,    2.08,    1.25,	0],
        ['Sanyo CP-2400SCR',              2300,   .0053,    2.05,    1.25,	0],
        ['Sanyo 3000CR',                  3000,   .0032,    2.96,    1.25,	0],
        ['Sanyo RC3000 NiMH',             3000,   .0035,    2.08,    1.25,	0],


        ['Tadiran Lithium-Metal',          800,   .08,       .6,     1.25,	0],
        ['Tanic 350',                      350,   .070,      .42,     3.7,	0],
        ['Tanic 470',                      470,   .040,      .44,     3.7,	0],
        ['Tanic 520',                      520,   .018,      .39,     3.7,	0],
        ['Tanic 830',                      830,   .053,      .64,     3.7,	0],
        ['Tanic 780',                      780,   .022,      .71,     3.7,	0],
        ['Tanic 1050',                    1050,   .041,      .78,     3.7,	0],
        ['Tanic 1550',                    1550,   .0301,    1.17,     3.7,	0],
        ['Tanic 2150',                    2150,   .0228,    1.52,     3.7,	0],
        ['Tanic 2200',                    2200,   .012,     1.45,     3.7,	0],
        ['Tanic 2220',                    2220,   .0195,    1.52,     3.7,	0],
        ['Tanic 2450',                    2450,   .019,     1.7,      3.7,	0],
        ['Tanic 2500',                    2500,   .018,     1.84,     3.7,	0],
        ['Tanic 3650',                    3650,   .0055,    3.21,     3.7,	0],
        ['Tanic 5000',                    5000,   .0026,    4.59,     3.7,	0],
        ['ThunderPower 480 12/16C',	   480,   .03,      .387,     3.7,	8],
        ['ThunderPower 730 12/16C',	   730,   .0164,     .53,     3.7,     12],
        ['ThunderPower 900 12/16C',	   900,   .03,      .705,     3.7,     15],
        ['ThunderPower 1320 13/20C',	  1320,   .03,      .987,     3.7,     27],
        ['ThunderPower 2100 15/20C',	  2100,   .0086,   1.624,     3.7,     42],
        ['ThunderPower 2070SX 25/50C',	  2070,   .0084,    1.87,     3.7,    104],
        ['ThunderPower 3850SXL 22/50C',   3850,   .0032,    3.35,     3.7,    193],
        ['ThunderPower 5000SX 22/50C',	  5000,   .0026,   4.305,     3.7,    250],
        ['Turnigy nano-tech 460 25/40C',   460,   .011,     .58,      3.7,     12],
        ['Turnigy nano-tech 800 25/40C',   800,   .01,    2.26,      3.7,      32],
        ['Turnigy nano-tech 850 25/40C',   850,   .0012,   .81,      3.7,      21],
        ['Turnigy nano-tech 1300 25/50C', 1300,   .0012,    1.52,     3.7,     26],
        ['Turnigy nano-tech 2200 25C',	  2200,   .0015,     6.6,     3.7,     55],
        ['Turnigy nano-tech 4000 25C',	  4000,     .0012,  3.88,     3.7,    100],
        ['Turnigy 1000 15C',		  1000,    .008,   2.26,      3.7,     15],
        ['Turnigy 1000 25C',		  1000,    .0061,    1.1,      3.7,    25],
        ['Turnigy 1600 20/30C',		  1600,    .0057,   1.98,      3.7,    32],
        ['Turnigy 1800 20C',		  1800,    .01,      1.86,     3.7,    36],
        ['Turnigy 1800 30C',		  1800,    .005,    1.85,      3.7,    54],
        ['Turnigy 2200 35C',		  2200,    .003,    2.33,      3.7,    77],
        ['Turnigy 3000 20C',		  3000,    .01,     2.98,      3.7,    60],
        ['Turnigy 3600 20C',		  3600,    .01,     3.53,      3.7,    72],
        ['Turnigy 4000 20/30C',		  4000,    .006,    4.02,      3.7,    80],
        ['Turnigy 4000 30/40C',		  4000,    .006,    3.99,      3.7,   120],
        ['Turnigy 5000 40C',		  5000,    .005,    5.1,       3.7,   200],
        ['ZIPPY Flightmax 2650 40C',      2650,    .006,    2.82,      3.7,   106],
        ['ZIPPY Flightmax 4000 20C',      4000,    .006,    3.53,      3.7,    80],
        ['ZIPPY Flightmax 5000 20C',      5000,    .005,    3.53,      3.7,   100],
        ['ZIPPY H2100 30/40C',            2100,    .0082,   2.22,      3.7,    53],
        ['ZIPPY H2200 20/30C',            2200,    .01,     1.91,      3.7,    44],
        ['ZIPPY H3300 20/30C',            3300,    .0065,   3.04,      3.7,    50],
        ['ZIPPY H4400 15/20C',            4400,    .0057,   4.84,      3.7,    66],
        ['ZIPPY H5800 30/40C',            5800,    .0033,   4.94,      3.7,   174]
        ]
        session['battery_mah']=request.form['mah']
        session['battery_maxv']=request.form['maxv']
        session['battery_weight']=request.form['maxw']
        session['battery_amp']=request.form['c_amp']
        mah=float(session['battery_mah'])
        current=float(session['battery_amp'])
        volt=float(session['battery_maxv'])
        weight=float(session['battery_weight'])
        c=[]
        for i in da:
            if i[1]<=mah:
                if weight<=i[3]:
                    if i[4]<=volt:
                        if i[5]<=current:
                            c.append(i)
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("suggest_battery.html",a='Login/signup',b='/login',books=c)
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('suggest_battery.html',a=d.username,b='/database',books=c)

@app.route('/design/all')
def all():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("dall.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('dall.html',a=d.username,b='/database')

@app.route('/outall',methods = ["POST"])
def outall():
    if request.method == "POST":
        flag=1
        try:
            session['custId']=request.form['custId']
            if session['custId']=="3487":
                flag=1
        except:
            flag=0
        try:
            session['a_n_s']=request.form['a_n_s']
            session['a_n_p']=request.form['a_n_p']
            par=int(session['a_n_p'])
            numcells=float(session['a_n_s'])
        except:
            par=1
            numcells=float(session['all_nob']) #series
        session['all_mah']=request.form['all_mah']
        session['all_amp']=request.form['all_amp']
        session['all_r']=request.form['all_r']
        try:
            session['ana_battery_wei_unit']=request.form['ana_battery_wei_unit']
            if session['ana_battery_wei_unit']=='gram':
                session['all_bat']=request.form['all_bat']
            elif session['ana_battery_wei_unit']=='oz':
                session['all_bat']=request.form['all_bat']
                session['all_bat']=float(session['all_bat'])*28.3495
        except:
            session['all_bat']=request.form['all_bat']
        session['all_volt']=request.form['all_volt']
        session['all_res']=request.form['all_res']
        session['all_mc']=request.form['all_mc']
        try:
            session['ana_wei_esc_unit']=request.form['ana_wei_esc_unit']
            if session['ana_wei_esc_unit']=="gram":
                session['all_weight']=request.form['all_weight']
            elif session['ana_wei_esc_unit']=='oz':
                session['all_weight']=request.form['all_weight']
                session['all_weight']=session['all_weight']*28.3495
        except:
            session['all_weight']=request.form['all_weight']
        session['all_nos']=request.form['all_nos']
        session['gx']=request.form['gx']
        session['all_tk']=request.form['all_tk']
        session['all_pk']=request.form['all_pk']
        try:
            session['ana_dia_unit']=request.form['ana_dia_unit']
            if session['ana_dia_unit']=='cm':
                session['all_dia']=request.form['all_dia']
            else:
                session['all_dia']=request.form['all_dia']
                session['all_dia']=float(session['all_dia'])*2.54
        except:
            session['all_dia']=request.form['all_dia']
        try:
            session['ana_pitch_unit']=request.form['ana_pitch_unit']
            if session['ana_pitch_unit']=='cm':
                session['all_pitch']=request.form['all_pitch']
            elif session['ana_pitch_unit']=='in':
                session['all_pitch']=float(session['all_pitch'])*2.54
        except:
            session['all_pitch']=request.form['all_pitch']
        try:
            session['ana_temp_unit_1']=request.form['ana_temp_unit_1']
            if session['ana_temp_unit_1']=="cell":
                session['all_temp']=request.form['all_temp']
            elif session['ana_temp_unit_1']=="kel":

                session['all_temp']=float(session['all_temp'])+273.15
        except:
            session['all_temp']=request.form['all_temp']
        try:
            session['ana_att_unit']=request.form['ana_att_unit']
            if session['ana_att_unit']=='m':
                session['all_att']=request.form['all_att']
            else:
                session['all_att']=request.form['all_att']
                session['all_att']=float(session['all_att'])*0.3048
        except:
            session['all_att']=request.form['all_att']
        session['1']=request.form['1']
        session['2']=request.form['2']
        session['3']=request.form['3']
        session['4']=request.form['4']
        session['5']=request.form['5']
        session['6']=request.form['6']
        session['7']=request.form['7']
        try:
            session['ana_motor_weight_unit']=request.form['ana_motor_weight_unit']
            if session['ana_motor_weight_unit']=='gram':
                session['8']=request.form['8']
            elif session['ana_motor_weight_unit']=='oz':
                session['8']=request.form['8']
                session['8']=float(session['8'])*28.3495
        except:
            session['8']=request.form['8']
        #PROPELLER Section:
        propblades=int(session['all_nos']) #no.of blades
        gearratio=int(session['gx'])
        gear=gearratio
        tconst=float(session['all_tk']) #tconstant
        pconst=float(session['all_pk']) #pconstant
        metric_propdiameter=float(session['all_dia']) #in cm
        propdiameter=metric_propdiameter/2.54
        metric_proppitch=float(session['all_pitch']) #in cm
        proppitch=metric_proppitch/2.54
        #Battery Section
        outCellCap=float(session['all_mah']) #Cell Capacity
        #numcells=float(session['all_nob']) #series
        outPackgr=float(session['all_bat'])   #pack weight in g
        MaxI=float(session['all_amp']) #Max Current
        outPackV=float(session['all_volt'])
        outCellRes=float(session['all_r']) #Cell Resistance
        Vcell=outPackV/numcells #voltpercell
        #par=1 #Parallel
        outPackOz=outPackgr/28.354   #pack weight in oz
        metric_outCellOz=outPackgr/numcells #Cell Weight g
        outCellOz=outPackOz/numcells #Cell Weight oz
        #Electronic Speed Controller ESC SEction
        Resc=float(session['all_res'])# ESC Resistance
        Amp=float(session['all_mc'])#Max Current
        metric_escoz=float(session['all_weight']) #esc weight in g
        escoz=metric_escoz/28.354#esc weight in oz
        #  MOTOR Section
        outKv=float(session['1'])  #Kv rpm/m
        outIo=float(session['3']) #IO
        outVo=float(session['4'])   #motor Voltage
        outRm=float(session['2']) #motor rm
        outKt=float(session['7']) #motor kt
        outIMax=float(session['5'])  #motor max power A
        outMotorPwr=float(session['6']) #motor max power w
        metric_motoroz=float(session['8'])  #Weight gram
        motoroz=metric_motoroz/28.354    # weight OZ
        MotorKi=1.55 #Default List Values Need to update
        MotorKrpm = 1.01 #Default List Values Need to update
        MotorRk = 60 #Default List Values Need to update
        MotorKv=outKv
        MotorRm=outRm
        #BaaroMeter Section
        metric_temp=float(session['all_temp']) #in celsius
        metric_alt=float(session['all_att']) #in meter
        temp=(metric_temp* 9/5) + 32# Temperature
        alt=metric_alt/0.3048 #altitude
        metric_baro = round(1013.25* (pow (1- (2.25577 * 0.00001* metric_alt),5.25588)))
        baro = round(10*metric_baro / 33.86388)/10
        mbar=round(baro * 33.86388)
        #calculations
        f1=[]
        f2=[]
        f3=[]
        f4=[]
        f5=[]
        f11=[]
        effdiameter = propdiameter * math.pow(propblades/2, .2)
        outEffDiameter=round(effdiameter,2);
        effdiameter=outEffDiameter
        MotorIO = (1*outIo) + ((Vcell*numcells - outVo)/MotorRk)
        if gear > 1:
            gear = gear * .98
        if effdiameter <= 0 or proppitch <= 0:
            Imotor = MotorIO
        else:
            tempg=(baro/29.92)*((460+59)/(460+1*temp)) * pconst * MotorKi * pow(effdiameter,4) * proppitch * (pow(12,-5)*1E-9) *pow((MotorKv/gear),3)
            tempr = (outCellRes * numcells) + (1* Resc) + (1 * MotorRm)
            Vbatt = Vcell * numcells
            tempb = (-2 * tempr * Vbatt - 1 / tempg ) / (tempr * tempr)
            tempc = ( pow(Vbatt,2) + MotorIO / tempg ) / (tempr * tempr)
            if tempb* tempb/4 > tempc:
                tempz = math.sqrt(pow(tempb,2)/4- tempc)
                tempi1 = -tempb/2 + tempz
                tempi2 = -tempb/2 - tempz
                if tempi2 > 0:
                    Imotor = tempi2
            else:
                Imotor = 0
        outImotor = round(Imotor)
        mmc=0
        if Imotor > outIMax:
            mmc=1
##            print('Motor Max Current exceeded!')
        emc=0
        if Imotor > Amp:
            emc=1
##            print('ESC Max Current exceeded!')
        bmc=0
        if Imotor > MaxI:
            bmc=1
##            print('Battery Max Current exceeded!')
        #CalcMotorValues Main Calculations
        metric_motoroz=round(motoroz * 28.34952,1)
        VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * outImotor )+ (1* Resc * outImotor))
        WattsIn = round( VoltsToMotor * outImotor,1)
        MotorRPM = MotorKv * ( VoltsToMotor - ( outImotor * MotorRm *(1 + .039*(pow(outImotor,2))/(metric_motoroz*2)) * MotorKrpm))
        FELoss = VoltsToMotor * MotorIO
        CULoss = pow(outImotor,2) * MotorRm *(1 + .039*(pow(outImotor,2))/(metric_motoroz*2))
        WattsOut = round(WattsIn - (1 * FELoss + CULoss ),2)
        if WattsOut <= 0:
            WattsOut = 0
        PctEff = round((WattsOut / WattsIn) * 100,1)
        if PctEff <= 0:
            PctEff = 0
        Pheat = WattsIn-WattsOut
        outVmotor = round(VoltsToMotor,2)
        outWin = round(WattsIn,1)
        outWout = round(WattsOut,1)
        outPctEff = round(PctEff,1)
        outRPM = round(MotorRPM,0)
        effdiameter = outEffDiameter
        outMotorPwr = 220
        if gearratio <= 0:
            gearratio = 1
        proprpm = MotorRPM / gearratio
        mmp=0
        if (1*outWin) > outMotorPwr:
            mmp=1
##            print(" Motor Max Power exceeded!")
        noLoadVoltsToMotor = (1 * Vcell * numcells) - ((1 * outCellRes * numcells * MotorIO )+ (1* Resc * MotorIO))
        noLoadMotorRPM = MotorKv * ( noLoadVoltsToMotor - (MotorIO * MotorRm))
        noLoadproprpm = noLoadMotorRPM / gearratio
        noLoadPitchspeed = noLoadproprpm * proppitch * .00094697
        noLoadmpspeed = noLoadPitchspeed * 1.609344
        Tgrams = round((baro/29.92)*((460+59)/(460+1*temp)) * tconst * proppitch * pow(effdiameter,3) * pow(proprpm / 1000,2.1) * 28.34952 * .858 / 10000)
        if proppitch/propdiameter > .6:
            Tgrams = round((baro/29.92)*((460+59)/(460+1*temp)) * tconst * propdiameter * .6 * pow(effdiameter,3) * pow(proprpm / 1000,2.1) * 28.34952 * .858 / 10000)
        Tkg = Tgrams / 1000
        Tn = Tkg * 9.80665
        Tlbs = Tn / 4.44822161526
        StaticToz = Tgrams/28.34952
        Propwatts = (baro/29.92)*((460+59)/(460+1*temp)) * pconst * pow(effdiameter/12,4) * (proppitch / 12 ) * pow(proprpm / 1000,3)
        HP = Propwatts / 745.699871582
        Pitchspeed = proprpm * proppitch * .00094697
        mpspeed = Pitchspeed * 1.609344;
        ThrustatSpeed = 16 * 375 * Propwatts / ( 746 * Pitchspeed )
        outmpspeed = round(mpspeed,0)
        outPropRpm = round(proprpm,0)
        outPropSThrust = round(StaticToz,1)
        outPropSThTgrams = round(Tgrams,1)
        ###
        #outPackOz=round(outCellOz * numcells * par,1)
        outPowersysOz = round((( 1 * motoroz) + ( 1 * outPackOz ) + ( 1 * escoz))*1.1,1)
        mspeed = round(1000* (effdiameter*3.1416*.083333333*proprpm*60)/(5280 * pow(temp*1 + 460,.5)*33.4))/1000
        outPitchSpeed = round(Pitchspeed,1)
        outPowersysgr = round(outPowersysOz * 28.34952,0)
        if effdiameter <= 0 or proppitch <= 0:
            Imotor = MotorIO
        outDuration=round( ((outCellCap * par/1000) / Imotor ) * 60 * 0.9, 2)
        st=0
        if 1*outPropSThrust < outPowersysOz :
            st=1
##            print(" Static Thrust < Power System Weight!")
        pms=0
        if  mspeed > .92:
            pms=1
##            print("Prop Tip MACH Speed exceeded!")
        li1=[]
        len1 = 100
        xmin=round(outIo)
        if outImotor < 10:
            xmax = 20
        if (outImotor > 10) and ( outImotor <= 20):
            xmax = 30
        if (outImotor > 20) and outImotor <= 30:
            xmax = 40
        if (outImotor > 30) and  outImotor <= 40:
            xmax = 60
        if (outImotor > 40) and (outImotor <= 60):
            xmax = 100
        if (outImotor > 60) and  outImotor <= 100:
            xmax = 200
        if (outImotor > 100) and outImotor <= 200:
            xmax = 400
        if (outImotor > 200):
            xmax = 600
        #outoutpower
        for i in range(1,len1):
            x1 = i/(len1)*(xmax-xmin)+xmin
            VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * x1 )+ (1* Resc * x1))
            FELoss = VoltsToMotor * MotorIO
            CULoss = pow(x1,2) * MotorRm *(1 + .039*(pow(x1,2))/(metric_motoroz*2))
            WattsIn = round( VoltsToMotor * x1,1)
            WattsOut = round(WattsIn - (1 * FELoss + CULoss ),2)
            if  WattsOut > 0 :
                y1 = WattsOut
                li1.append([x1, y1])
                f1.append([x1,y1])
        Woutmax=max(li1)[0]
        # Motor RPM
        li3=[]
        len3 = 50
        for i in range(xmin,len3+1):
            x3 = i/(len3)*(xmax-xmin)+xmin
            VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * x3 )+ (1* Resc * x3))
            MotorRPM = MotorKv * ( VoltsToMotor - ( x3 * MotorRm *(1 + .039*(pow(x3,2))/(metric_motoroz*2)) * MotorKrpm))
        if MotorRPM > 0:
            y3 = MotorRPM/1000
            li3.append([x3,y3])
            f3.append([x3,y3])
        try:
            maxrpm=max(li3)[0]
        except:
            maxrpm=0
        #efficiency
        len2 = 100;
        li2=[]
        f11=[]
        for i in range(xmin,len2+1):
            x2 = (i / len2) * (xmax - xmin) + xmin
            VoltsToMotor =  1 * Vcell * numcells - (1 * outCellRes * numcells * x2 + 1 * Resc * x2)
            FELoss = VoltsToMotor * MotorIO
            CULoss = pow(x2, 2) * MotorRm * (1 + (0.039 * pow(x2, 2)) / (metric_motoroz * 2))
            WattsIn = round(VoltsToMotor * x2, 1);
            WattsOut = round(WattsIn - (1 * FELoss + CULoss), 2)
            if  WattsOut > 0 :
                y2 = round((WattsOut / WattsIn) * 100, 2)
                li2.append([x2, y2])
                f2.append([x2,y2])
                f11.append([x2,x2])
        PctEffmax=max(li2)[0]
        # Motor Heating
        li4=[]
        len4 = 50
        for i in range(xmin,len4+1):
            x4 = i/(len4)*(xmax-xmin)+xmin
            VoltsToMotor = (1 * Vcell * numcells)-((1 * outCellRes * numcells * x4 )+ (1* Resc * x4))
            FELoss = VoltsToMotor * MotorIO
            CULoss = pow(x4,2) * MotorRm *(1 + .039*(pow(x4,2))/(metric_motoroz*2))
            WattsIn = round( VoltsToMotor * x4,1)
            WattsOut = round(WattsIn - (1 * FELoss + CULoss ),2)
            if WattsOut > 0:
                y4 = WattsIn-WattsOut
                li4.append([x4,y4])
                f4.append([x4,y4])
        f6=[[outImotor,0]]
        f7=[[outWout]]
        f8=[[outImotor,outPctEff]]
        f9=[[outImotor,outRPM/1000]]
        f10=[[outImotor,Pheat]]

        now_utc = datetime.now(timezone('UTC'))
        now_local = now_utc.astimezone(get_localzone())
        li=now_local.strftime(format)
        li=li.split(' ')
        cal=li[0].split('-')
        time=li[1]
        mon=calendar.month_name[int(cal[1])]
        year=cal[0]
        date=cal[2]
        xx=date+' '+mon+' '+year
        if mmc==1 and emc==1 and bmc==1 and st==1 and pms==1 and flag==0:
            try:
                register= user98(email=session['email'],Max_Output_Power=Woutmax,Input_Power_In_watts=outWin,Output_Power_In_watts=outWout,Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=PctEffmax,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,time=time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Static Thrust < Power System Weight! Prop Tip MACH Speed exceeded!  Motor Max Power exceeded! Battery Max Current exceeded! ESC Max Current exceeded! Motor Max Current exceeded!",bb="In order to get reasonable climb and acceleration capabilities, the Static Thrust should be at least about1/3 of the planes weight",cc="class = alert alert-danger")
            except:
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Static Thrust < Power System Weight! Prop Tip MACH Speed exceeded!  Motor Max Power exceeded! Battery Max Current exceeded! ESC Max Current exceeded! Motor Max Current exceeded!",bb="In order to get reasonable climb and acceleration capabilities, the Static Thrust should be at least about1/3 of the planes weight",cc="class = alert alert-danger")
        elif mmc==1  and flag==0:
            try:
                register= user98(Max_Output_Power=Woutmax,Input_Power_In_watts=outWin,Output_Power_In_watts=outWout,Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=PctEffmax,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,time=time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="  Motor Max Power exceeded!",bb="In order to get reasonable get rid of these problem u have to recude Kv load to motor",cc="class = alert alert-danger")
            except:
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="  Motor Max Power exceeded!",bb="In order to get reasonable get rid of these problem u have to recude Kv load to motor",cc="class = alert alert-danger")
        elif emc==1  and flag==0:
            try:
                register= user98(Max_Output_Power=Woutmax,Input_Power_In_watts=outWin,Output_Power_In_watts=outWout,Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=PctEffmax,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,time=time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="ESC Max Current exceeded!",bb="In order to get reasonable get rid of these problem you have to recude Kv load to motor and increase battery mah and volts",cc="class = alert alert-danger")
            except:
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="ESC Max Current exceeded!",bb="In order to get reasonable get rid of these problem you have to recude Kv load to motor and increase battery mah and volts",cc="class = alert alert-danger")
        elif bmc==1  and flag==0:
            try:
                register= user98(email=session['email'],Max_Output_Power=Woutmax,Input_Power_In_watts=outWin,Output_Power_In_watts=outWout,Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=PctEffmax,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,time=time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Battery Max Current exceeded!",bb="In order to get reasonable get rid of these problem you have to  increase battery mah and volts",cc="class = alert alert-danger")
            except:
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Battery Max Current exceeded!",bb="In order to get reasonable get rid of these problem you have to  increase battery mah and volts",cc="class = alert alert-danger")

        elif st==1  and flag==0:
            try:
                register= user98(email=session['email'],Max_Output_Power=Woutmax,Input_Power_In_watts=outWin,Output_Power_In_watts=outWout,Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=PctEffmax,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,time=time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Static Thrust < Power System Weight!",bb="In order to get reasonable climb and acceleration capabilities, the Static Thrust should be at least about 1/3 of the planes weight",cc="class = alert alert-danger")
            except:
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Static Thrust < Power System Weight!",bb="In order to get reasonable climb and acceleration capabilities, the Static Thrust should be at least about 1/3 of the planes weight",cc="class = alert alert-danger")

        elif pms==1  and flag==0:
            try:
                register= user98(email=session['email'],Max_Output_Power=Woutmax,Input_Power_In_watts=outWin,Output_Power_In_watts=outWout,Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=PctEffmax,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,time=time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Prop Tip MACH Speed exceeded!",bb="In order to get reasonable get rid of these problem you have to recude Kv load to motor and increase battery mah and volts",cc="class = alert alert-danger")
            except:
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Prop Tip MACH Speed exceeded!",bb="In order to get reasonable get rid of these problem you have to recude Kv load to motor and increase battery mah and volts",cc="class = alert alert-danger")


        elif flag==1:
            try:
                register= user99(email=session['email'],Input_Power_In_watts=outWin, Output_Power_In_watts=outWout, Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=outPctEff,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,Static_Thrust_in_g=outPropSThTgrams,Prop_Static_Tip_Speed=mspeed,time =time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],['Max Output Power',Woutmax],['Static Current Draw ',outImotor],
                ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr],['Prop Static Tip Speed ',mspeed],['Static Thrust in g',outPropSThTgrams]]
                session['email']= request.cookies.get('email')
                session['pass']=request.cookies.get('pass')
                if session['email']==None:
                    return render_template("outall1.html",a='Login/signup',b='/login',ls=l)
                else:
                    try:
                        d= user97.query.filter_by(email=session['email']).first()
                    except:
                        flash("Error Came Try again")
                        return render_template('signup.html')
                    return render_template('outall1.html',a=d.username,b='/database',ls=l)
            except:
                l=[['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],['Max Output Power',Woutmax],['Static Current Draw ',outImotor],
                ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr],['Prop Static Tip Speed ',mspeed],['Static Thrust in g',outPropSThTgrams]]
                session['email']= request.cookies.get('email')
                session['pass']=request.cookies.get('pass')
                if session['email']==None:
                    return render_template("outall1.html",a='Login/signup',b='/login',ls=l)
                else:
                    try:
                        d= user97.query.filter_by(email=session['email']).first()
                    except:
                        flash("Error Came Try again")
                        return render_template('signup.html')
                    return render_template('outall1.html',a=d.username,b='/database',ls=l)
        else:
            try:
                register= user98(email=session['email'],Max_Output_Power=Woutmax,Input_Power_In_watts=outWin,Output_Power_In_watts=outWout,Motor_Rpm=outRPM,Static_Efficiency=outPctEff,Volts_to_Motor=outVmotor,Maximum_efficiency=PctEffmax,Propeller_Static_RPM=outPropRpm,Static_Pitch_Speed=outmpspeed,time=time,o_date=xx)
                db.session.add(register)
                db.session.commit()
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Great",bb="Your Drone had Complete All Test for Flying",cc="alert alert-light")
            except:
                l=[['Max Output Power',Woutmax],['Output Power',outWout],['Input Power In watts',outWin],['Output Power In watts',outWout],['Motor Rpm',outRPM],['Static_Efficiency',outPctEff],['Volts_to_Motor',outVmotor],['Maximum_efficiency',PctEffmax],
                   ['Propeller Static RPM',outPropRpm],['Static Pitch Speed in km/h',outmpspeed],['Approx Full-Throttle duration ',outDuration],['Power System Weight +10% [g] ',outPowersysgr]]
                return render_template("outall.html",ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=f7,h=f8,i=f9,j=f10,k=f11,xmin1=xmin,xmax1=xmax,aa="Great",bb="Your Drone had Complete All Test for Flying",cc="alert alert-light")

#ANALYZE
@app.route('/index1')
@app.route('/analyze')
def analyze():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("analyze.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('analyze.html',a=d.username,b='/database')

@app.route('/analyze/motor')
def analyze_motor():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("analyze_motor.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('analyze_motor.html',a=d.username,b='/database')
@app.route('/prop')
@app.route('/analyze/propeller')
def analyze_propeller():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("analyze_propeller.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('analyze_propeller.html',a=d.username,b='/database')

@app.route('/analyze/propeller/output',methods = ["POST"])
def analyze_propeller_output():
    if request.method == "POST":
        session['ana_temp']=request.form['ana_temp']
        session['ana_tempunit']=request.form['ana_tempunit']
        if session['ana_tempunit']=='ana_fa':
            temp=float(session['ana_temp'])
            metric_temp=(temp-32)*5/9
        else:
            metric_temp=float(session['ana_temp'])
            temp=(metric_temp/(5/9))+32


        session['ana_att']=request.form['ana_att']
        session['ana_att_unit']=request.form['ana_att_unit']#ana_m,ana_oz
        if  session['ana_att_unit']=="ana_feet":
            alt=float(session['ana_att'])
            metric_alt=alt*0.3048
        else:
            metric_alt=float(session['ana_att'])
            alt=metric_alt/0.3048
        session['ana_dia']=float(request.form['ana_dia'])
        session['ana_diaunit'] = request.form['ana_diaunit']
        if session['ana_diaunit']=='ana_in':
            diameter=float(session['ana_dia'])
            metric_diameter=diameter*2.54
        else:
            metric_diameter=float(session['ana_diaunit'])
            diameter=metric_diameter/2.54
        session['ana_nof']=int(request.form['ana_nof'])

        try:
            session['ana_sv']=float(request.form['ana_sv'])
        except:
            session['ana_sv']=0
        try:
            session['ana_c']=float(request.form['ana_c'])
        except:
            session['ana_c']=0
        session['ana_rpm']=int(request.form['ana_rpm'])
        session['ana_tc']=float(request.form['ana_tc'])
        session['ana_pc']=float(request.form['ana_pc'])

        session['ana_pitch']=float(request.form['ana_pitch'])
        session['ana_pu']=request.form['ana_pu']
        if session['ana_pu']=='ana_p_in':
            pitch=float(session['ana_pitch'])
            metric_pitch=pitch*2.54
        else:
            metric_pitch=float(session['ana_pitch'])
            pitch=metric_pitch/2.54

        metric_baro = round(1013.25* (pow (1- (2.25577 * 0.00001* metric_alt),5.25588)))
        baro = round(10*metric_baro / 33.86388)/10
        #mbar=round(baro * 33.86388)
        tconst=session['ana_tc']
        pconst=session['ana_pc']
        blade=session['ana_nof']
        rpm=session['ana_rpm']
        volt=session['ana_sv']
        current=session['ana_c']
        effdiameter = diameter * pow(blade/2, .2)
        reqmetric_power = round(volt*current)
        reqpower = round(100*(reqmetric_power/745.699871582))/100
        pspeed = round(10*(rpm*pitch*.00094697))/10
        metric_pspeed = round(pspeed * 1.609344)
        fspeed = round(rpm*pitch * .0011364)
        metric_fspeed = round(fspeed * 1.609344)
        metric_power = round((metric_baro*100/(287.05*(273.15+1*metric_temp)))/1.225*pconst * pitch * pow(effdiameter,4) * pow(rpm,3.02)*5.33*pow(10,-15),1)
        power = round(100*(metric_power/745.699871582))/100
        eff = round(10*(metric_power/reqmetric_power)*100)/10
        thrust_metric = round((baro/29.92)*((460+59)/(460+1*temp)) * tconst * pitch * pow(effdiameter,3) * pow(rpm / 1000, 2.1) * 28.34952 * .858 / 10000)

        if pitch/diameter > .6:
            thrust_metric = round((baro/29.92)*((460+59)/(460+1*temp)) * tconst * diameter*.6 * pow(effdiameter,3) * pow(rpm / 1000, 2.1) * 28.34952 * .858 / 10000)
        thrust = round((thrust_metric/28.34952),1)
        tipspeed = diameter*3.1416/12*rpm*60/5280
        speedOfsound = pow(temp*1 + 460,.5)*33.4
        mspeed = round(tipspeed/speedOfsound,3)
        '''if mspeed > .92:
            print("Prop Tip MACH Speed exceeded!")'''
        #graph Part
        if rpm > 60 and rpm <= 4950:
            xmax = 5000
        if rpm > 4950 and rpm <= 9950:
            xmax = 10000
        if rpm > 9950 and rpm <= 14500:
            xmax = 15000
        if rpm > 14500 and rpm <= 19500:
            xmax = 20000
        if rpm > 19500 and rpm <= 29500:
            xmax = 30000
        if rpm > 29500 and rpm <= 39500:
            xmax = 40000
        if rpm > 39500 and rpm <= 49500:
            xmax = 5000
        if rpm > 49500:
            xmax = 100000
        xmin = 0
        f1=[]
        f2=[]
        f3=[]
        f4=[]
        f5=[]
        f6=[]
        #Thrust
        len1 = 100
        for i in range(xmin,len1+1):
            x1 = i / (len1) * (xmax - xmin) + xmin
            if (pitch/diameter < .6):
                thrust_value = (baro/29.92)*(460+59)/(460+1*temp) * tconst * pitch* pow(effdiameter,3) *  pow(x1 / 1000,2.1) * 28.34952 *.858 / 10000
            else:
                thrust_value = (baro/29.92)*(460+59)/(460+1*temp) * tconst * diameter *.6 *  pow(effdiameter,3) *  pow(x1 / 1000,2.1) * 28.34952 * .858 / 10000
            if (thrust_metric > 0):
                y1 = thrust_value
                f1.append([x1,y1])
                f4.append([x1, x1*0.01])
        #Absorbed Power
        len2 = 100
        li5=[]
        for i in range(0,len2):
            x1 = i / (len2) * (xmax - xmin) + xmin
            power_value = (baro/29.92)*(460+59)/(460+1*temp) * pconst * pitch * pow(effdiameter,4) * pow(x1,3.02)*5.33*pow(10,-15)
            if metric_power > 0:
                y2 = power_value
                f5.append([x1, y2])
                li5.append([y2, x1])
        x2 = rpm
        y2_1 = 0
        f2.append([x2, y2_1]);
        y2_2 = thrust_metric;
        f3.append([x2, y2_2])
        y2_3 = metric_power
        f6.append([x2, y2_3])
        try:
            maxabpow=max(li5)[0]/2
        except:
            maxabpow=0
        maxthrust=max(f1)[0]/2
        maxrpm=rpm/100
        l=[['Estimated Static Thrust in ounces ',thrust],['Supplied Power in horse power',reqpower],['Supplied Power in Watts',reqmetric_power],
           ['Propeller Absorbed Power in horse power',power],['Propeller Absorbed Power in watts',metric_power],['Static Efficiency : %',eff],
           ['Static Pitch Speed in mph',pspeed],['Appx. Level Flight Speed in mph',fspeed],['Prop Tip MACH Speed',mspeed]]
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template('analyze_propeller_out.html',ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=xmax,log="Log In",link="/login")
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('analyze_propeller_out.html',ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=xmax,log=d.username,link="/database")
    else:
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template('analyze_propeller_out.html',ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=xmax,log="log In",link="/login")
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('analyze_propeller_out.html',ls=l,a=f1,b=f2,c=f3,d=f4,e=f5,f=f6,g=xmax,log=d.username,link="/database")

@app.route('/analyze/ipa',methods = ["GET","POST"])
def analyze_ipa():
    if request.method == "POST":
        session['ipa_sps_unit']=request.form['ipa_sps_unit']
        if session['ipa_sps_unit']=='ipa_km':
            session['ipa_sps'] =float(request.form['ipa_sps'])
        elif session['ipa_sps_unit']=='ipa_mph':
            session['ipa_sps'] =float(request.form['ipa_sps'])
            session['ipa_sps']=float(session['ipa_sps'])*1.60934

        session['ipa_st_unit']=request.form['ipa_st_unit']
        if session['ipa_st_unit']=='ipa_mgr':
            session['ipa_st'] =float(request.form['ipa_st'])
        elif session['ipa_st_unit']=='hello_hai':
            session['ipa_st'] =float(request.form['ipa_st'])
            session['ipa_st']=float(session['ipa_st'])*28.3495

        session['ipa_eff'] =float(request.form['ipa_eff'])

        metric_thrust=session['ipa_st']
        metric_pitch=session['ipa_sps']
        eff=session['ipa_eff']
        power = round(metric_thrust*metric_pitch/(530*eff*.01))
        l=[[" Input Power needed :  ",power]]
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template("inputpower_out.html",a='Login/signup',b='/login',ls=l)
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('inputpower_out.html',a=d.username,b='/database',ls=l)
    else:
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template("inputpower_form.html",a='Login/signup',b='/login')
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('inputpower_form.html',a=d.username,b='/database')

@app.route('/analyze/stallspeed',methods = ["GET","POST"])
def analyze_stall():
    if request.method == "POST":

        session['ss_temp'] =float(request.form['ss_temp'])
        session['ss_tempunit']=request.form['ss_tempunit']
        if session['ss_tempunit']=='ss_fa':
            temp=float(session['ss_temp'])
            metric_temp=(temp-32)*5/9
        else:
            metric_temp=float(session['ss_temp'])
            temp=(metric_temp/(5/9))+32

        session['ss_att'] =float(request.form['ss_att'])
        session['ss_att_unit']=request.form['ss_att_unit']
        if  session['ss_att_unit']=="ss_feet":
            alt=float(session['ss_att'])
            metric_alt=alt*0.3048
        else:
            metric_alt=float(session['ss_att'])
            alt=metric_alt/0.3048
        metric_baro = round(1013.25* (pow (1- (2.25577 * 0.00001* metric_alt),5.25588)))
        baro = round(10*metric_baro / 33.86388)/10
        mbar=round(baro * 33.86388)
        airdensity = round(1000*metric_baro*100/(287.05*(273.15 + 1*metric_temp)))/1000


        session['ss_wing'] =float(request.form['ss_wing'])
        session['ss_wing_unit'] =request.form['ss_wing_unit']
        if session['ss_wing_unit']=='ss_in':
            area=float(session['ss_temp'])
            metric_area=round (10*(area*.0645))/10
        else:
            metric_area=float(session['ss_temp'])
            area=round (metric_area/.0645);

        session['ss_air'] =float(request.form['ss_air'])
        session['ss_air_unit'] =request.form['ss_air_unit']
        if session['ss_air_unit'] =='ss_moz':
            weight=session['ss_air']
            metric_weight=round(weight / .0353 )
        else:
            metric_weight=session['ss_air']
            weight=round (10*( metric_weight * .0353))/10
        session['ss_mlc'] =float(request.form['ss_mlc'])
        cl=session['ss_mlc']
        if weight > 0:
            metric_sspeed= round(3.6*pow((2*metric_weight*0.00980665)/(airdensity * cl * metric_area*0.01), 0.5) *10 )/10
        else:
            metric_sspeed = 0
        if weight > 0:
            sspeed = round(10*(metric_sspeed/1.609344))/10
        else:
            sspeed =0
        l=[['Stall Speed In mph',metric_sspeed],['Stall Speed In km/h',sspeed]]
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template("stall_out.html",a='Login/signup',b='/login',ls=l)
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('stall_out.html',a=d.username,b='/database',ls=l)

    else:
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template("stall_form.html",a='Login/signup',b='/login')
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('stall_form.html',a=d.username,b='/database')

@app.route('/analyze/all')
def analyze_all():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("analyze_drone.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('analyze_drone.html',a=d.username,b='/database')

#SUGGEST
@app.route('/suggest')
def suggest():
    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("design.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('design.html',a=d.username,b='/database')

@app.route('/suggest/motor',methods = ["GET","POST"])
def suggest_motor():
    """  Name                        Kv,       Rm,      Io,     Imaxc4,   Wgt5,    Pwr6,    Ki,    Krpm,    Rk,   Vo,"""
    motorarray = [
        ['Above All 2813-18',         1200,     .075,	 1.2,	 25,	 1.94,	 165,    1.55,   1.01,    60, 8.2],
        ['Align BL450S 1000Kv',       1000,     .23,	.45,	 14,	 1.7,	 144,    1.55,   1.0,     30,   8],
        ['Align BL450S 1500Kv',	      1500,     .115,	.5,	 15,     1.7,    144,    1.55,   1.0,     30,	8],
        ['ARC-20-27-80', 	      4447,     .153,	.57,     12,     1.02,    87,    1.55,	 1.1,     50,	8],
        ['ARC-20-34-110',	      3026,     .1155,  .55,     12,     1.38,   117,    1.55,	 1.1,     40,	8],
        ['ARC-20-34-130',	      4600,     .05,    .87,     20,     1.38,   117,    1.55,	 1.1,     60,	8],
        ['ARC-28-37-2',	              3789,     .0556,  1.1,     60,     2.93,   250,    1.5,	 1.05,    20,	8],
        ['ARC-28-37-3',	              2729,     .103,   .8,      35,     2.72,   230,    1.55,	 1.05,    20,	8],
        ['ARC-28-47-2',	              2258,     .0592,  .95,     25,     4.06,   345,    1.5,	 1.05,    20,	8],
        ['ARC-28-58-1',	              3165,     .0249,  1.4,     80,     5.4,    460,    1.54,	 1.1,    20, 12.5],

        ['Astro C035 #603',	      2765,     .04,     2.5,     30,     6.0,   510,    1.55,	 1.1,     60,	8],
        ['Astro C05 #605',	      2125,     .045,    2.5,     30,     7.5,   636,    1.55, 	 1.1,     60,	8],
        ['Astro C15 #615',	      1488,     .069,    2,       25,     8.0,   680,    1.55,	 1.1,     60,	8],
        ['Astro C25 #625',	       971,     .093,    2,       30,     11,    936,    1.55,	 1.1,     60,	8],
        ['Astro C40 #640',	       682,     .121,    2,       30,     13,    1100,   1.55,	 1.1,     60,	8],
        ['Astro C60P #661',	       347,     .103,    2.5,     30,     22,    1870,   1.55,	 1.1,     60,	8],

        ['Aveox 1005/2Y',	      6173,     .018,    1.5,    35,      3.1,   264,    1.45,	 1.1,     60,	8],
        ['Aveox 1005/3Y',             4115,     .041,    1,      25,      3.1,   264,    1.45,	 1.0,     60,	8],
        ['Aveox 1005/4Y',	      3086,     .073,    .7,     15,      3.1,   264,    1.45, 	 1.0,     60,	8],
        ['Aveox 1005/5Y',	      2469,     .114,    .6,     12,      3.1,   264,    1.55,	 1.0,     60,	8],
        ['Aveox 1010/1Y',             5955,     .006,    1.8,    74,      4.6,   390,    1.40,	 1.2,     60,	8],
        ['Aveox 1010/1.5Y',           3970,     .014,    1.2,    35,      4.5,   384,    1.50,	 1.05,    60,	8],
        ['Aveox 1010/2Y',	      2978,     .024,    .9,     30,      4.6,   390,    1.56,	 1.0,     60,	8],
        ['Aveox 1010/3Y',	      1985,     .054,    .6,     15,      4.6,   390,    1.58,	 1.06,    60,	8],
        ['Aveox 1010/4Y',             1489,     .096,    .44,    10,      4.6,   390,    1.43,	 1.0,     60,	8],
        ['Aveox 27/13/2',	      4686,     .018,    1.68,   30,      2.86,  240,    1.47,	 1.0,     60,	8],
        ['Aveox 27/13/3',	      3124,     .041,    1.12,   30,      2.86,  240,    1.55,	 1.0,     60,	8],
        ['Aveox 27/13/4',	      2343,     .073,    .84,    23,      2.86,  240,    1.55,	 1.0,     60,	8],
        ['Aveox 27/13/5',	      1874,     .114,    .67,    15,      2.86,  240,    1.58,	 1.0,     60,	8],
        ['Aveox 27/26/1',	      4686,     .006,    3,      90,      4.34,  369,    1.48,	 1.0,     60,	8],
        ['Aveox 27/26/1.5',	      3124,     .014,    2,      60,      4.34,  369,    1.51,	 1.3,     60,	8],
        ['Aveox 27/26/2',             2343,     .024,    1.5,    45,      4.34,  369,    1.57,	 1.1,     60,	8],
        ['Aveox 27/26/3',	      1562,     .054,    1,      30,      4.34,  369,    1.57,	 1.1,     60,	8],
        ['Aveox 27/26/4',	      1172,     .096,    .75,    23,      4.34,  369,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/1',	      3124,     .007,    2.3,    90,      5.7,   486,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/1.5',	      2083,     .016,    1.53,   60,      5.7,   486,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/2',	      1562,     .028,    1.15,   45,      5.7,   486,    1.55,	 1.1,     60,	8],
        ['Aveox 27/39/3',	      1041,     .063,    .77,    30,      5.7,   486,    1.55,	 1.0,     60,	8],
        ['Aveox 27/39/4',	       781,     .112,    .58,    23,      5.7,   486,    1.55,	 1.0,     60,	8],

        ['AXI 2203/40 VPP Gold Line V2', 2000,  .245,    .5,     10,      .67,    60,    1.5,	 1.1,     60,	8],
        ['AXI 2203/Race Gold Line V2', 2355,    .213,    .62,    10,      .67,    62,    1.5,	 1.1,     20,  7.6],
        ['AXI 2203/46 Gold Line V2',  1785,     .387,    .32,    9.5,     .71,    60,    1.5,	 1.1,     50,	7],
        ['AXI 2203/52 Gold Line V2',  1579,     .452,    .31,    8.0,     .71,    50,    1.5,	 1.1,     53,	7],
        ['AXI 2204/54 Gold Line V2',  1395,     .420,    .36,    8.5,     .97,    80,    1.5,	 1.1,     35,	8],
        ['AXI 2208/20 Gold Line V2',  1863,     .143,   1.05,    18,      1.54,  130,    1.5,	 1.1,     25,	8],
        ['AXI 2208/26 Gold Line V2',  1428,     .191,    .6,     13,      1.54,  130,    1.5,	 1.1,     22,	8],
        ['AXI 2208/34 Gold Line V2',  1090,     .274,    .4,     10,      1.54,  130,    1.5,	 1.1,     27,	8],
        ['AXI 2212/12 Gold Line V2',  2043,     .061,   1.28,    30,      1.98,  300,    1.5,	 1.1,     50, 7.2],
        ['AXI 2212/20 Gold Line V2',  1159,     .149,    .71,    18,      1.98,  170,    1.5,	 1.1,     25,  10],
        ['AXI 2212/26 Gold Line V2',  944,      .224,    .5,     14,      1.98,  170,    1.5,	 1.1,     50, 9.3],
        ['AXI 2212/34 Gold Line V2',  691,      .292,    .31,    12,      1.98,  170,    1.5,	 1.1,    100,   8],
        ['AXI 2217/12 Gold Line V2',  1454,     .067,   1.38,    32,      2.45,  330,    1.5,	 1.1,     12,   8],
        ['AXI 2217/16 Gold Line V2',  1011,     .100,    .78,    24,      2.45,  245,    1.5,	 1.1,     19,   8],
        ['AXI 2217/20 Gold Line V2',   848,     .165,    .6,     24,      2.45,  270,    1.5,	 1.1,     33,   8],
        ['AXI 2808/16 Gold Line V2',  1875,     .073,    1.4,    26,      2.72,  230,    1.5,	 1.1,     10,   7],
        ['AXI 2808/20 Gold Line V2',  1495,     .091,    .92,    26,      2.72,  230,    1.5,	 1.1,     11,   7],
        ['AXI 2808/24 Gold Line V2',  1225,     .118,    .97,    23,      2.72,  230,    1.5,	 1.1,     15,   7],
        ['AXI 2814/6D Gold Line V2',  2866,     .027,    4.5,    56,      3.78,  550,    1.5,	 1.1,     10,	6],
        ['AXI 2814/10 Gold Line V2',  1742,     .046,    2.1,    46,      3.78,  320,    1.5,	 1.1,     10,	7],
        ['AXI 2814/12 Gold Line V2',  1446,     .06,     1.6,    36,      3.78,  320,    1.5,	 1.1,     10,	7],
        ['AXI 2814/16 Gold Line V2',  1063,     .065,    1.1,    32,      3.78,  325,    1.5,	 1.1,     19,	8],
        ['AXI 2814/20 Gold Line V2',  824,      .097,    .81,    26,      3.78,  355,    1.5,	 1.1,     28, 9.2],
        ['AXI 2820/08 Gold Line V2',  1486,     .038,    3.2,    56,      5.22,  565,    1.5,	 1.1,     13,	7],
        ['AXI 2820/10 Gold Line V2',  1138,     .040,    2.3,    43,      5.22,  440,    1.5,	 1.1,     10,	8],
        ['AXI 2820/12 Gold Line V2',  992,      .049,    1.5,    38,      5.22,  440,    1.5,	 1.1,     10,  10],
        ['AXI 2820/14 Gold Line V2',  831,      .063,    1.2,    37,      5.22,  520,    1.5,	 1.1,     15,   9],
        ['AXI 2826/06 Gold Line V2',  1501,     .030,    3.2,    66,      6.25,  665,    1.5,	 1.1,     15, 7.2],
        ['AXI 2826/08 Gold Line V2',  1119,     .040,    2.3,    56,      6.25,  570,    1.5,	 1.1,     15,  10],
        ['AXI 2826/10 Gold Line V2',  925,      .055,    1.9,    43,      6.25,  530,    1.5,	 1.1,     15, 9.5],
        ['AXI 2826/12 Gold Line V2',  740,      .055,    1.4,    38,      6.25,  530,    1.5,	 1.1,     10,  10],
        ['AXI 2826/13 Gold Line V2',  710,      .065,    1.5,    40,      6.25,  530,    1.5,	 1.1,     10,   8],
        ['AXI 4120/14 Gold Line V2',  662,      .034,    2.4,    57,     11.12, 1000,    1.5,	 1.1,     10,  10],
        ['AXI 4120/18 Gold Line V2',  505,      .056,    1.3,    59,     11.12, 1500,    1.5,	 1.1,     18,  12],
        ['AXI 4120/20 Gold Line V2',  456,      .072,    1.7,    53,     11.12, 1160,    1.5,	 1.1,     20,  21],
        ['AXI 4130/16 Gold Line V2',  370,      .069,    1.4,    61,     14.47, 1780,    1.5,	 1.1,     21,  15],
        ['AXI 4130/20 Gold Line V2',  300,      .088,    1.1,    56,     14.47, 1650,    1.5,	 1.1,     50,  15],
        ['AXI 5320/18 Gold Line V2',  370,      .023,    1.3,    79,     18.18, 1850,    1.5,	 1.1,     20,  20],
        ['AXI 5320/18 3D Extreme V2', 370,      .023,    1.3,    79,     18.71, 1900,    1.5,	 1.1,     20,  20],
        ['AXI 5320/28 Gold Line V2',  235,      .091,    1.2,    65,     18.18, 1600,    1.5,	 1.1,     42,  25],
        ['AXI 5320/34 Gold Line V2',  192,      .124,    0.9,    50,     18.18, 1850,    1.5,	 1.1,     53,  25],
        ['AXI 5325/16 Gold Line V2',  350,      .026,    2.0,    86,     21.0,  2650,    1.5,	 1.1,     50,  20],
        ['AXI 5325/18 Gold Line V2',  308,      .032,    1.6,    81,     21.0,  2440,    1.5,	 1.1,     50,  20],
        ['AXI 5325/20 Gold Line V2',  280,      .037,    1.9,    79,     21.0,  2430,    1.5,	 1.1,     50,  30],
        ['AXI 5325/24 Gold Line V2',  232,      .045,    1.6,    76,     21.0,  2850,    1.5,	 1.1,     50,  30],
        ['AXI 5330/18 Gold Line V2',  255,      .038,    1.8,    76,     23.72, 2870,    1.5,	 1.1,     23,  25],
        ['AXI 5330/F3A Gold Line V2', 220,      .038,    1.3,    73,     23.72, 2780,    1.5,	 1.1,     37,  25],
        ['AXI 5330/24 Gold Line V2',  197,      .057,    1.4,    59,     23.72, 2220,    1.5,	 1.1,     50,  30],
        ['AXI 5345/14HD Gold Line V2', 225,     .027,    2.5,   112,     35.12, 4200,    1.5,	 1.1,     50,  30],
        ['AXI 5345/16HD Gold Line V2', 195,     .034,    2.0,    92,     35.12, 4195,    1.5,	 1.1,     50,  30],
        ['AXI 5345/18HD Gold Line V2', 171,     .042,    1.5,    77,     35.12, 3510,    1.5,	 1.1,     50,  30],
        ['AXI 5345/20HD Gold Line V2', 145,     .042,    1.5,    85,     35.12, 3870,    1.5,	 1.1,     50,  30],
        ['AXI 5360/18HD Gold Line V2', 125,     .058,    1.8,    75,     44.83, 2900,    1.5,	 1.1,     50,  30],
        ['AXI 5360/20HD Gold Line V2', 115,     .068,    1.8,    65,     44.83, 3000,    1.5,	 1.1,     50,  30],
        ['AXI 5360/24HD Gold Line V2',  95,     .082,    1.8,    65,     44.83, 3120,    1.5,	 1.1,     50,  30],

        ['Cobra C-2202/70',           1530,     .504,    .25,     6,      0.53,   45,    1.3,	 1.1,     40,   8],
        ['Cobra C-2203/46',           1720,     .220,    .40,     8,      0.62,   60,    1.3,	 1.1,     40,   8],
        ['Cobra C-2204/32',           1900,     .173,    .58,    12,      0.79,   90,    1.3,	 1.1,     40,   8],
        ['Cobra C-2208/20',           2000,     .096,    .80,    18,      1.64,  200,    1.3,	 1.05,    40,   8],
        ['Cobra C-2208/34',           1180,     .228,    .40,    12,      1.66,  130,    1.3,	 1.05,    40,   8],
        ['Cobra C-2213/12',           1957,     .077,    1.2,    30,      2.11,  330,    1.45,	 1.1,     40,   8],
        ['Cobra C-2213/18',           1350,     .102,    .68,    20,      2.15,  220,    1.3,	 1.1,     40,   8],
        ['Cobra C-2213/22',           1082,     .178,    .55,    17,      2.11,  190,    1.45,	 1.1,     40,   8],
        ['Cobra C-2213/26',            950,     .220,    .8,     14,      2.15,  150,    1.3,	 1.1,     40,  11],
        ['Cobra C-2217/8',            2300,     .042,   2.10,    40,      2.61,  300,    1.3,	 1.1,     20,   8],
        ['Cobra C-2217/12',           1540,     .086,   1.15,    32,      2.61,  230,    1.3,	 1.1,     20,   8],
        ['Cobra C-2221/8',            1850,     .049,   1.59,    45,      3.10,  500,    1.3,	 1.1,     20,   8],
        ['Cobra C-2221/10',           1500,     .055,   1.38,    38,      3.10,  420,    1.3,	 1.1,     20,  12],
        ['Cobra C-2221/12',           1250,     .075,   1.09,    32,      3.10,  360,    1.3,	 1.1,     20,  12],
        ['Cobra C-2221/16',            940,     .126,    .75,    25,      3.10,  280,    1.3,	 1.1,     40,  12],
        ['Cobra C-2808/16',           1780,     .056,   1.35,    30,      2.85,  330,    1.3,	 1.1,     20,   8],
        ['Cobra C-2808/22',           1330,     .084,    .82,    24,      2.85,  270,    1.3,	 1.1,     40,   8],
        ['Cobra C-2808/26',           1130,     .113,    .75,    22,      2.85,  240,    1.3,	 1.1,     40,   8],
        ['Cobra C-2808/30',           1000,     .144,    .53,    20,      2.85,  220,    1.3,	 1.1,     40,   8],
        ['Cobra C-2814/10',           1700,     .036,   2.06,    48,      3.84,  530,    1.3,	 1.1,     20,  10],
        ['Cobra C-2814/12',           1390,     .045,   1.44,    40,      3.84,  450,    1.3,	 1.1,     20,  10],
        ['Cobra C-2814/16',           1050,     .068,    .9,     30,      3.84,  330,    1.3,	 1.1,     40,  10],
        ['Cobra C-2814/20',            850,     .099,    .7,     25,      3.84,  280,    1.3,	 1.1,     40,  10],
        ['Cobra C-2820/8',            1450,     .030,   2.5,     55,      4.9,   610,    1.3,	 1.1,     20,  10],
        ['Cobra C-2820/10',           1170,     .041,   1.6,     45,      5.01,  490,    1.3,	 1.1,     20,  10],
        ['Cobra C-2820/12',            970,     .059,   1.3,     40,      4.87,  440,    1.3,	 1.1,     20,  10],
        ['Cobra C-2820/14',            840,     .071,   1.0,     36,      4.94,  400,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/6',            1470,     .027,   3.0,     65,      6.03,  720,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/8',            1130,     .038,   2.3,     55,      6.03,  610,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/10',            930,     .048,   1.3,     45,      6.03,  610,    1.3,	 1.1,     20,  10],
        ['Cobra C-2826/12',            760,     .068,   1.1,     42,      6.03,  460,    1.3,	 1.1,     20,  10],
        ['Cobra C-3510/16',           1200,     .042,   1.4,     42,      4.97,  460,    1.3,	 1.1,     20,  14],
        ['Cobra C-3510/20',           1000,     .060,   1.06,    32,      4.97,  350,    1.3,	 1.1,     20,  14],
        ['Cobra C-3510/24',            820,     .080,    .81,    26,      4.97,  480,    1.3,	 1.1,     40,  14],
        ['Cobra C-3515/12',           1100,     .036,   1.64,    45,      6.28,  500,    1.3,	 1.1,     20,  14],
        ['Cobra C-3515/14',            950,     .044,   1.39,    44,      6.28,  500,    1.3,	 1.1,     20,  14],
        ['Cobra C-3515/18',            740,     .065,   1.01,    36,      6.28,  530,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/10',            980,     .037,   1.84,    60,      7.41,  670,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/12',            820,     .039,   1.45,    56,      7.62,  650,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/14',            700,     .048,   1.33,    46,      7.62,  680,    1.3,	 1.1,     20,  14],
        ['Cobra C-3520/18',            550,     .075,    .93,    36,      7.62,  670,    1.3,	 1.1,     40,  14],
        ['Cobra C-3525/10',            780,     .035,   1.65,    62,      8.92,  760,    1.3,	 1.1,     20,  14],
        ['Cobra C-3525/12',            650,     .045,   1.48,    52,      8.92,  960,    1.3,	 1.1,     20,  20],
        ['Cobra C-3525/14',            560,     .055,   1.18,    45,      8.92,  670,    1.3,	 1.1,     20,  20],
        ['Cobra C-3525/18',            430,     .087,    .84,    38,      8.92,  700,    1.3,	 1.1,     40,  20],
        ['Cobra C-4120/12',            850,     .021,   2.74,    75,     10.34, 1110,    1.3,	 1.1,     20,  14],
        ['Cobra C-4120/14',            710,     .027,   1.99,    68,     10.34, 1260,    1.3,	 1.1,     20,  14],
        ['Cobra C-4120/16',            610,     .036,   1.51,    62,     10.34, 1150,    1.3,	 1.1,     20,  14],
        ['Cobra C-4120/18',            540,     .045,   1.5,     54,     10.23, 1200,    1.3,	 1.1,     20,  20],
        ['Cobra C-4120/22',            430,     .06,    1.14,    45,     10.23, 1000,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/12',            540,     .029,   1.85,    65,     14.04, 1440,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/14',            450,     .036,   1.46,    60,     14.11, 1330,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/16',            390,     .048,   1.12,    55,     13.97, 1220,    1.3,	 1.1,     20,  20],
        ['Cobra C-4130/20',            300,     .069,   .77,     52,     13.97, 1150,    1.3,	 1.1,     40,  20],
        ['Cobra CM-2204/28',          2300,     .126,   .66,     17,       .87,  125,    1.3,	 1.1,     30,   8],
        ['Cobra CM-2204/32',          1960,     .153,   .58,     13,       .87,   90,    1.3,	 1.1,     30,   8],
        ['Cobra CM-2208/20',          2000,     .114,   .77,     20,       1.56, 150,    1.3,	 1.1,     30,   8],
        ['Cobra CM-2208/34',          1200,     .265,   .36,     12,       1.56, 135,    1.3,	 1.1,     40,  10],
        ['Cobra CM-2213/26',           950,     .230,   .42,     12,       2.29, 155,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2213/36',           700,     .389,   .28,     11,       2.42, 120,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2217/20',           950,     .188,   .53,     20,       2.68, 220,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2217/26',           695,     .269,   .36,     16,       2.86, 175,    1.3,	 1.1,     40,  12],
        ['Cobra CM-2814/24',           700,     .142,   .55,     23,       4.09, 340,    1.3,	 1.1,     50,  12],
        ['Cobra CM-2814/36',           470,     .282,   .29,     17,       4.13, 330,    1.3,	 1.1,     50,  12],
        ['Cobra CM-2820/16',           740,     .111,   .92,     35,       5.15, 430,    1.3,	 1.1,     50,  15],
        ['Cobra CM-2820/24',           490,     .166,   .53,     27,       5.15, 500,    1.3,	 1.1,     50,  15],
        ['Cobra CM-2820/32',           350,     .300,   .33,     20,       5.15, 450,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3515/20',           650,     .087,   .78,     34,       7.02, 600,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3515/34',           385,     .200,   .38,     24,       7.02, 530,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3520/20',           480,     .104,   .68,     32,       8.25, 650,    1.3,	 1.1,     50,  15],
        ['Cobra CM-3520/28',           350,     .176,   .43,     26,       8.25, 575,    1.3,	 1.1,     50,  15],
        ['Cobra CM-4008/24',           600,     .086,   .72,     23,       3.74, 340,    1.3,	 1.1,     50,  12],
        ['Cobra CM-4008/36',           400,     .151,   .52,     18,       3.74, 400,    1.3,	 1.1,     50,  21],
        ['Cobra CM-4510/28',           420,     .087,   .68,     35,       7.44, 780,    1.3,	 1.1,     50,  20],
        ['Cobra CM-4510/40',           310,     .170,   .31,     22,       7.44, 490,    1.3,	 1.1,     50,  15],
        ['Cobra CM-4515/18',           435,     .051,   .95,     54,       9.63, 1200,   1.3,	 1.1,     50,  15],
        ['Cobra CM-4520/14',           400,     .048,  1.45,     60,      12.06, 1330,   1.3,	 1.1,     50,  21],
        ['Cobra CM-4520/18',           310,     .066,   .99,     45,      11.99, 1000,   1.3,	 1.1,     50,  21],

        ['Dualsky 2822-24',           1533,     .446,     .50,   10,     1.06,    90,    1.52,	 1.0,     20,   8],
        ['Dualsky 2826-15',           1208,     .211,     .60,   15,     1.55,   130,    1.52,	 1.0,     20,   8],
        ['Dualsky 450EP 2834-8',      3330,     .084,    2.60,   32,     2.40,   200,    1.52,	 1.0,     10, 9.3],
        ['Dualsky XM2826-18',         1012,     .345,     .40,   12,     1.55,   150,    1.35,	 1.05,    20,   7],
        ['Dualsky XM2830CA-10',       1168,     .179,    1.17,   20,     1.94,   165,    1.5,	 1.02,    10,12.2],
        ['Dualsky XM2834CA-9T',        971,     .125,     .7,    24,     2.47,   210,    1.5,	 1.02,    10,  10],
        ['Dualsky XM3530EA-13',        963,     .128,     .92,   19,     2.54,   215,    1.5,	 1.02,    15, 8.3],
        ['Dualsky XM3536CA-8',        1037,     .101,    1.24,   35,     3.64,   300,    1.50,	 1.1,     10,  12],
        ['Dualsky XM3542CA-7T',        789,    .0795,    1.64,   34,     4.84,   400,    1.50,	 1.1,     10,  10],
        ['Dualsky XM3548-5',          1124,    .0865,    1.6,    40,     5.82,   490,    1.50,	 1.05,    10,   8],
        ['Dualsky XM4240CA-12T',       984,    .0958,    1.15,   35,     4.48,   380,    1.45,	 1.1,     12,  10],

        ['E-flite Park 300 BL 1380',  1380, 	.33,	 .4,	 9,	  .8,     85,    1.5,    1.1,     60,  10],
        ['E-flite Park 370 BL 1080',  1080, 	.19,	 .7,	 10,	  1.6,   100,    1.5,    1.1,     60,  10],
        ['E-flite Park 370 BL 1360',  1360, 	.1,	 1.0,	 13,	  1.6,   125,    1.5,    1.1,     40,  10],
        ['E-flite Park 400 BL 740',    740, 	.26,	 0.55,	 10,	  2.0,   100,    1.5,    1.1,     40,  10],
        ['E-flite Park 400 BL 920',    920, 	.1,	 0.7,	 13,	  2.0,   140,    1.5,    1.1,     40,  10],
        ['E-flite Park 450 BL 890',    890, 	.2,	 .7,	 18,	  2.5,   175,    1.5,    1.1,     40,  10],
        ['E-flite Park 480 BL 910',    910, 	.08,	 .85,	 25,	  3.1,   250,    1.5,    1.1,     40,  10],
        ['E-flite Park 480 BL 1020',  1020, 	.06,	 1.1,	 28,	  3.1,   275,    1.5,    1.1,     40,  10],
        ['E-flite Power 10 BL',	      1100, 	.04,	 2.1,	 38,	  4.3,   375,    1.5,    1.1,     40,  10],
        ['E-flite Power 15 BL',	       950, 	.03,	 2.0,	 42,	  5.4,   425,    1.5,    1.1,     40,  10],
        ['E-flite Power 25 BL',	       870, 	.03,	 2.4,	 44,	  6.7,   550,    1.5,    1.1,     40,  10],
        ['E-flite Power 32 BL',	       770, 	.02,	 2.4,	 60,	  7.0,   700,    1.5,    1.1,     40,  10],
        ['E-flite Power 46 BL',	       670, 	.04,	 3.9,	 55,	 10.0,   800,    1.5,    1.1,     40,  15],
        ['E-flite Power 60 BL',	       400, 	.06,	 2.7,	 60,	 13.0,  1200,    1.5,    1.1,     40,  15],
        ['E-flite Power 110 BL',       295, 	.03,	 1.3,	 65,	 17.5,  1900,    1.5,    1.1,     40,  15],
        ['E-flite Power 160 BL',       260, 	.02,	 1.6,	 75,	 23.0,  2500,    1.5,    1.1,     40,  15],

        ['Electrifly RimFire 28-22-1380',1380,  .370,    .4,      9,      .96,    81,    1.25,	 1.1,     30, 7.4],
        ['Electrifly RimFire 28-26-1000',1000,  .165,    .7,     12,      1.45,  123,    1.25,   1.3,     30, 7.4],
        ['Electrifly RimFire 28-26-1300',1300,  .155,    .9,     15,      1.45,  123,    1.38,   1.02,    19, 7.4],
        ['Electrifly RimFire 28-26-1600',1600,  .098,    1.0,    17,      1.45,  123,    1.50,   1.02,    15, 7.4],
        ['Electrifly RimFire 28-30-750',  740,  .185,    .6,     10,      1.91,  162,    1.25,   1.3,     13, 7.4],
        ['Electrifly RimFire 28-30-950',  940,  .098,    .7,     14,      1.91,  162,    1.28,   1.35,    12, 7.4],
        ['Electrifly RimFire 28-30-1250',1250,  .120,    .9,     18,      1.91,  162,    1.50,   1.1,     13, 7.4],
        ['Electrifly RimFire 28-30-1450',1450,  .065,    1.07,   23,      1.91,  162,    1.55,   1.01,    13, 7.4],
        ['Electrifly RimFire 35-30-950',  940,  .065,    .8,     20,      2.51,  213,    1.45,   1.35,    15,  11],
        ['Electrifly RimFire 35-30-1250',1250,  .115,    1.2,    30,      2.51,  213,    1.40,   1.0,     15,  11],
        ['Electrifly RimFire 35-36-1000',1000,  .055,    1.4,    40,      3.6,   306,    1.45,   1.0,     13,  11],
        ['Electrifly RimFire 35-36-1200',1200,  .047,    1.8,    45,      3.6,   306,    1.48,   1.0,     13,  11],
        ['Electrifly RimFire 35-36-1500',1500,  .030,    2.6,    50,      3.6,   306,    1.25,   1.0,     13,  11],
        ['Electrifly RimFire 35-48-700',  670,  .025,    1.4,    35,      6.0,   510,    1.40,   1.4,     10, 14,8],

        ['Goldberg Turbo 550',        2528,     .085,    2,      60,      7.8,   663,    1.55,	 1.0,     60,	8],
        ['Graupner Sp280 6V',         2320,     1.12,    .28,    8,       1.5,   127,    1.50,	 1.1,     50,	6],
        ['Graupner Sp300 6V',         4833,     .214,    .7,     12,      1.8,   153,    1.55,	 1.1,     50,	8],
        ['Graupner Sp400 6V',         3000,     .303,    .7,     12,      2.6,   222,    1.55,	 1.15,    15,	6],
        ['Graupner Sp400 7.2V',       2277,     .450,    .5,     18,      2.6,   222,    1.55,   1.15,    28, 7.2],
        ['Graupner Sp480 7.2V',       2350,     .298,    1.1,    20,      3.7,   315,    1.40,	 1.16,    32, 7.2],
        ['Graupner Sp480 Race 7.2V',  2936,     .155,    2.0,    20,      3.7,   315,    1.53,	 1.05,    18, 7.2],
        ['Graupner Sp500 Race 7.2V',  2985,     .105,    2.5,    20,      3.7,   315,    1.55,	 1.05,    18, 7.2],
        ['Graupner Sp600 7.2V',       2437,     .112,    2.0,    25,      6.9,   585,    1.53,	 1.06,    15, 7.2],
        ['Graupner Sp600 8.4V',       1780,     .150,    1.8,    25,      7.8,   663,    1.55,	 1.05,    25, 8.4],
        ['Graupner Sp600 9.6V',       1470,     .201,    1.0,    30,      6.9,   585,    1.52,	 1.08,    40, 9.6],
        ['Graupner Sp700 Race 9.6V',  1875,     .120,    3.0,    25,      11.5,  978,    1.55,	 1.08,    60, 9.6],
        ['G. P. Goldfire',            2441,     .094,    2,      25,      7.6,   645,    1.55,	 1.0,      60,	8],
        ['G. P. Thrustmaster',        2168,     .18,     1.5,    25,      7.6,   645,    1.55,	 1.0,      60,	8],

        ['Hacker A05-10S',            4200,     .3,      .5,     5,       .265,   25,    1.5,    1.1,     26, 8.4],
        ['Hacker A05-13S',            3200,     .29,     .4,     5,       .265,   30,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-7L',             2200,     .11,     1.1,    8,       .71,    60,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-9L',             1700,     .18,     .72,    8,       .71,    60,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-12S',            2900,     .185,    1.0,    6,       .53,    45,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-13L',            1200,     .28,     .39,    9,       .71,    60,    1.5,    1.1,     26, 8.4],
        ['Hacker A10-15S',            2320,     .289,    .63,    6,       .53,    45,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-6XL 8Pole EVO',  3500,     .014,    3.4,    55,      2.75,  300,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-6XL 10Pole EVO', 2500,     .020,    3.4,    40,      2.75,  300,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-8XL EVO',        1500,     .026,    2.6,    35,      2.75,  300,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-12XL EVO',       1039,     .075,    1.2,    30,      2.75,  230,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-20L EVO',        1022,     .089,    .85,    19,      1.94,  165,    1.5,	 1.1,     30, 8.4],
        ['Hacker A20-20L',            1022,     .109,    .85,    19,      2.01,  210,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-22L EVO',         924,     .109,    .75,    17,      1.94,  165,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-22L',             924,     .089,    .75,    17,      2.01,  190,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-26M EVO',        1130,     .117,    .7,     15,      1.48,  126,    1.5,	 1.1,     26, 8.4],
        ['Hacker A20-26M',            1130,     .117,    .7,     15,      1.48,  150,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-30M',             980,     .174,    .6,     14,      1.48,  150,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-34S',            1500,     .147,    .75,    10,      1.02,  100,    1.5,    1.1,     26, 8.4],
        ['Hacker A20-50S',            1088,     .232,    .4,     8,       1.02,   80,    1.5,    1.1,     26, 8.4],
        ['Hacker A30-10L V3',         1185,     .023,    2.3,    40,      5.05,  500,    1.5,    1.1,     26, 8.4],
        ['Hacker A30-22S V3',         1440,     .041,    1.4,    28,      2.47,  275,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-10XL V4',         900,     .024,    1.9,    50,      6.25,  530,    1.5,    1.1,     26, 8.4],
        ['Hacker A30-12L V4',         1000,     .03,     1.8,    35,      5.05,  500,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-12XL V4',         700,     .034,    1.5,    37,      6.25,  600,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-14L V4',         800,      .036,    1.6,    35,      5.05,  800,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-16M V4',         1060,     .038,    1.6,    35,      3.67,  350,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-12M V4',         1370,     .022,    2.2,    35,      3.67,  350,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-22S V4',         1440,     .041,    1.4,    25,      2.47,  250,    1.5,    1.1,     50, 8.4],
        ['Hacker A30-28S V4',         1140,     .068,    1.1,    25,      2.47,  250,    1.5,    1.1,     50, 8.4],
        ['Hacker A50-12L Glider',      355,     .021,    1.5,    70,      17.8, 1500,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-12S V4',          480,     .016,    1.8,    55,     12.18, 1030,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-14L V4',          300,     .025,    1.0,    70,     15.71, 1330,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-14S V4',          425,     .021,    1.5,    55,     12.18, 1030,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-16S V4',          365,     .026,    1.4,    70,     12.18, 1030,    1.5,    1.1,     60, 8.4],
        ['Hacker A50-8S Tornado V3',   850,     .009,    4.1,    80,     12.28, 1040,    1.5,	 1.1,     60, 8.4],
        ['Hacker A50-10S Tornado V3',  690,     .011,    3.1,    80,     12.28, 1040,    1.5,	 1.1,     66, 8.4],
        ['Hacker A60-5XS V2',         3065,     .125,    .4,     12,      1.8,   153,    1.5,	 1.1,     26, 8.4],
        ['Hacker Q60-7M F3A',          210,     .025,   1.8,     90,     20.47, 1740,    1.5,	 1.1,     60, 8.4],

        ['Himax HC2808-0860',          860,     .255,    .36,    11,      1.83,  156,    1.55,   1.05,     26,	8],
        ['Himax HC2808-0980',          980,     .22,     .4,     12,      1.83,  156,    1.50,	 1.09,     26,	8],
        ['Himax HC2808-1160',         1160,     .15,     .6,     15,      1.83,  156,    1.55,	 1.05,     26,	8],
        ['Himax HC2812-0650',          650,     .285,    .36,    11,      2.26,  192,    1.55,	 1.05,     26,	8],
        ['Himax HC2812-0850',          850,     .169,    .6,     14,      2.26,  192,    1.55,	 1.05,     26,	8],
        ['Himax HC2812-1080',         1080,     .111,    .75,    15,      2.26,  192,    1.55,	 1.05,     26,	8],
        ['Himax HC2816-0890',          890,     .119,    .8,     18,      2.72,  230,    1.55,	 1.05,     40,	8],
        ['Himax HC2816-1220',         1200,     .071,    1.4,    25,      2.72,  230,    1.55,	 1.1,      30, 10],
        ['Himax HC3510-1100',         1100,     .055,    1.2,    30,      3.14,  267,    1.55,	 1.05,     50,	8],
        ['Himax HC3510-1540',         1540,     .029,    1.8,    42,      3.14,  267,    1.55,	 1.05,     50,	8],
        ['Himax HC3516-0840',          840,     .051,    1.5,    37,      4.73,  400,    1.55,	 1.05,     60,	8],
        ['Himax HC3516-1130',         1130,     .03,     1.8,    48,      4.73,  400,    1.55,	 1.05,     60,	8],
        ['Himax HC3516-1350',         1350,     .023,    2.3,    56,      4.73,  400,    1.55,	 1.05,     60,	8],
        ['Himax HC3522-0700',          700,     .049,    1.3,    40,      5.71,  486,    1.53,	 1.05,     60,	8],
        ['Himax HC3522-0990',          990,     .027,    2.2,    54,      5.71,  486,    1.53,	 1.05,     60,	8],
        ['Himax HC3528-0800',          800,     .031,    1.7,    54,      6.95,  590,    1.30,	 1.0,      60,	8],
        ['Himax HC3528-1000',         1000,     .02,     2.6,    68,      6.95,  590,    1.50,	 1.05,     60,	8],

        ['Hyperion Z-2205-34',        1500,     .34,     .5,      8,      1.04,   90,    1.52,	 1.0,      60,	8],
        ['Hyperion Z-2205-38',        1300,     .42,     .38,     7,      1.04,   90,    1.59,	 1.0,      40,	8],
        ['Hyperion Z-2209-26',        1100,     .170,    .65,    11,      1.47,  126,    1.57,	 1.0,      38,	8],
        ['Hyperion Z-2209-32',         900,     .240,    .55,    10,      1.47,  126,    1.52,	 1.05,     32,	8],
        ['Hyperion Z-2213-20',        1010,     .150,    .65,    14,      1.87,  159,    1.58,	 1.0,      32,	8],
        ['Hyperion Z-2213-24',         850,     .175,    .60,    12,      1.87,  159,    1.56,	 1.0,      28,	8],
        ['Hyperion Z-3007-26',        1228,     .085,    1.11,   28,      2.65,  150,    1.50,	 1.05,     16,	8],
        ['Hyperion Z-3007-30',        1033,     .095,    1.2,    25,      2.65,  150,    1.50,	 1.02,     16,	8],
        ['Hyperion Z-3013-14',        1080,     .048,    2.5,    40,      3.88,  330,    1.50,	 1.0,      23,	8],
        ['Hyperion Z-3013-16',         985,     .059,    2.0,    36,      3.88,  330,    1.50,	 1.05,     18,	8],
        ['Hyperion Z-3019-10',        1230,     .031,    2.42,   46,      5.01,  426,    1.51,	 1.02,     10,	8],
        ['Hyperion Z-3019-12',         900,     .034,    2.35,   42,      5.01,  426,    1.55,	 1.05,     10,	8],
        ['Hyperion Z-3025-08',         985,     .036,    4.8,    65,      6.56,  558,    1.50,	 1.05,     10,  10],
        ['Hyperion Z-3025-10',         815,     .025,    2.3,    46,      6.56,  558,    1.55,	 1.0,      60,	8],

        ['Jeti Phasor 15-3',          2300,     .025,    2.5,    35,      4.8,   408,    1.50,	 1.3,      60,	8],
        ['Jeti Phasor 15-4',          1800,     .042,    1.9,    32,      4.8,   408,    1.50,	 1.2,      60,	8],
        ['Jeti Phasor 30-3',          1200,     .034,    2.8,    35,      4.8,   408,    1.50,	 1.2,      60,	8],

        ['KDA20-34S',                 1850,     .330,    .72,     9,      1.06,   90,    1.50,	 1.05,    20,  11],
        ['KDA2217/20',                 875,     .195,    1.0,    22,      2.51,  213,    1.50,	 1.0,     20,12.4],
        ['KDA KB2835-35',             2350,     .190,    1.0,    20,      3.21,  270,    1.50,	 1.05,    20,   7],

        ['Kontronik FUN400-23',       2300,     .058,    .5,     30,      3.88,  330,    1.5,	 1.1,      60,	8],
        ['Kontronik FUN400-42',       4000,     .017,    2.0,    50,      3.88,  330,    1.40,	 1.1,      40,  7],
        ['Kyosho AP-29L',             4099,     .0907,   3.5,    30,      5.5,   468,    1.55,	 1.05,     60,	8],
        ['Kyosho AP-29L meas',        3914,     .034,    3.8,    35,      5,     426,    1.55,	 1.05,     60,	8],
        ['Kyosho Atomic Force',       3531,     .035,    2.94,   30,      6.3,   537,    1.55,	 1.05,     60,	8],
        ['Kyosho EndoPlasma',         3785,     .022,    2.5,    30,      6.3,   537,    1.55,	 1.05,     60,	8],
        ['Kyosho LeMans 480 Gold',    2500,     .076,    1.1,    30,      6.25,  530,    1.55,	 1.05,     60,	8],
        ['Kyosho LeMans DMC20BB',     4939,     .054,    .54,    30,      6.3,   537,    1.55,	 1.05,     60,	8],
        ['Kyosho Magnetic Mayhem',    2260,     .0667,   1.37,   30,       8,    680,    1.55,	 1.05,     60,	8],
        ['MEC Turbo 10 GT',           3400,     .038,    2.3,    35,       10,   852,    1.55,	 1.05,     60,	8],
        ['MEC Turbo 10 Plus',         4850,     .025,    3.4,    35,       11,   936,    1.55,	 1.05,     60,	8],

        ['Medusa MR-012-030-4000',    3940,     .386,     .3,     6,       .53,   45,    1.53,	 1.05,     20,	8],
        ['Medusa MR-012-030-5300',    5230,     .228,     .43,    7,       .53,   45,    1.53,	 1.01,     20,	8],
        ['Medusa MR-028-032-1200',    1200,     .185,     .35,   15,      2.47,  210,    1.48,	 1.05,     40,	8],
        ['Medusa MR-028-032-1500',    1490,     .118,    .5,     19,      2.47,  210,    1.50,   1.02,     30,	8],
        ['Medusa MR-028-032-1900',    1890,     .085,    .65,    23,      2.47,  210,    1.48,	 1.03,     40,	8],
        ['Medusa MR-028-032-2400',    2390,     .050,    .85,    28,      2.47,  210,    1.53,	 1.0,      30,	8],
        ['Medusa MR-028-032-2800',    2790,     .040,     1.0,   30,      2.47,  210,    1.52,	 1.05,     30,	8],

        ['Mega ACn 16-15-4',          2300,     .045,     1.1,   20,      2.7,   230,    1.5,	 1.1,      50,	8],
        ['Mega ACn 16-15-5',          1800,     .060,    .80,    20,      2.7,   230,    1.80,	 1.0,      50,	8],
        ['Mega ACn 16-15-6',          1500,     .112,    .79,    18,      2.7,   230,    1.80,	 1.0,      50,  12],
        ['Mega ACn 16-15-8',          1230,     .176,    .33,    15,      2.7,   230,    1.78,	 1.0,      50, 8.2],
        ['Mega ACn 22-20-4',          1550,     .055,    1.8,    50,      5.82,  495,    1.70,	 1.0,      60,  14],
        ['Mega ACn 22-30-3',          1300,     .042,    1.11,   70,      7.79,  660,    1.80,	 1.0,      60, 8.6],

        ['Mini AC 1215/16',	      3800,     .086,    1.4,    18,      1.7,   144,    1.55,	 1.3,      60,	8],
        ['Mini AC 1215/20',           3000,     .117,    1.1,    16,      1.73,  147,    1.55,	 1.4,      60,	8],
        ['Mini AC Extreme',           6370,     .045,    3.9,    28,      2.72,  231,    1.50,	 1.0,      60,	8],
        ['MP Jet AC 25/35-20',        3850,     .1,      1.34,   25,      2.54,  216,    1.55,	 1.0,      60,	8],

        ['Motrolfly DM 2205-1350',     1189,     .272,     .5,     9,       .99,  100,    1.2,	 1.2,      35,  10],
        ['Motrolfly DM 2205-1800',     1890,     .110,     .9,    12,       .99,  129,    1.2,	 1.2,      15, 7.0],
        ['Motrolfly DM 2205-2800',     2840,     .095,     .85,   22,       .99,  200,    1.2,	 1.2,      10, 7.0],
        ['Motrolfly DM 2210-1080',      993,     .172,     .51,   15,      1.52,  155,    1.2,	 1.2,      26, 7.0],
        ['Motrolfly DM 2210-1400',     1290,     .095,    1.033,  15,      1.52,  155,    1.2,	 1.2,      26, 7.0],
        ['Motrolfly DM 2210-1700',     1623,     .0621,   1.245,  20,      1.52,  180,    0.97,	 1.8,      10, 7.0],
        ['Motrolfly DM 2210-2200',     2190,     .032,    1.94,   25,      1.52,  250,    1.25,	 1.9,      10, 7.0],
        ['Motrolfly DM 2215-850',       731,     .1522,    .51,   17,      2.07,  162,    1.35,	 1.4,     100, 7.0],
        ['Motrolfly DM 2215-1150',     1080,     .086,     .92,   17,      2.07,  188,    1.35,	 1.7,      17, 7.0],
        ['Motrolfly DMH 2215-3100',    3165,     .078,    1.983,  29,      1.9,   265,    0.8,	 1.2,      10, 7.0],
        ['Motrolfly DMH 2215-3500',    3670,     .045,    2.11,   32,      1.9,   260,    0.9,	 1.5,      10, 6.0],

        ['Multiplex Permax BL-X22-13',1350,    .280,    .45,    12,      1.13,    96,    1.46,	 1.05,     20,  10],
        ['Multiplex Permax BL-X22-18',1790,    .195,    .75,    15,      1.13,    96,    1.44,	 1.05,     20,  10],
        ['Multiplex Permax BL-X22-23',2300,    .080,    .85,    18,      1.13,    96,    1.42,	 1.05,     20,  10],
        ['Multiplex Permax 280 7.2V', 2417,     .553,    .3,   4.5,      1.6,    135,    1.55,	 1.0,      40, 7.2],
        ['Multiplex Permax 280 BB',   4464,     .429,    .7,     8,       1.9,   160,    1.50,	 1.0,      40,	 8],
        ['Multiplex Permax 400 6V',   2946,     .357,    .73,    7,       2.6,   222,    1.55,	 .98,      40,	 6],
        ['Multiplex Permax 400 7.2V', 2268,     .473,    .70,    8,       2.6,   222,    1.55,	 .98,      40, 7.2],
        ['Multiplex Permax 450 Turbo',2189,     .138,    1.2,    25,      4.9,   417,    1.55,	 1.05,     60,	 8],
        ['Multiplex Permax 480 7.2V', 2459,     .312,    .92,    12,      3.3,   280,    1.50,	 1.02,     50, 7.2],

        ['PJS 550 E',                  802,     .1,     1.0,     15,      1.9,   160,    1.35,	 1.1,      40,	8],
        ['PJS 550 R',                 1225,     .22,    1.5,     12,      1.9,   160,    1.45,	 1.1,      40,	8],

        ['Plettenberg Freestyle 20',  1461,     .149,   .93,     12,      2.65,  225,   1.35,	 1.1,      50,	8],
        ['Plettenberg Freestyle 24',  1183,     .240,   .82,     10,      2.65,  225,   1.45,	 1.05,     50,	8],
        ['Plettenberg Freestyle XL',   942,     .095,   1.05,    15,      5.0,    425,    1.55,	 1.05,     60,	8],
        ['Plettenberg Orbit 10-22',   1080,     .064,   1.8,    35,       4.77,  400,    1.30,	 1.1,      60,  11],
        ['Plettenberg Orbit 15-14',   1100,     .035,   2.5,    55,       6.18,  525,    1.35,	 1.1,      60,  11],
        ['Plettenberg Orbit 20-14',    810,     .040,   1.8,    25,       7.59,  645,    1.53,	 1.06,     60,10.5],
        ['Plettenberg Typhoon 6-20',  1600,     .133,   .7,     12,       1.52,  130,    1.41,	 1.2,      60,	8],

        ['Scorpion S-1804-1650',      1700,     .8,     .25,     5,       .42,   33,    1.3,	 1.1,      20, 6.5],
        ['Scorpion S-1805-2250',      2250,     .41,    .25,     7,       .56,   45,    1.3,	 1.1,      20, 6.5],
        ['Scorpion SII-2205-1490',    1500,     .32,    .42,    10,       1.25,  110,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2208-1100',    1105,     .29,    .41,    12,       1.59,  133,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2208-1280',    1285,     .27,    .47,    14,       1.59,  155,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-885',      885,     .29,    .41,    13,       2.05,  192,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-960',      960,     .27,    .51,    13,       2.05,  192,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-1070',    1090,     .25,    .59,    15,       2.05,  222,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2212-1850',    1850,     .08,   1.31,    22,       2.05,  326,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2215-900',      920,     .27,    .52,    16,       2.42,  237,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2215-1127',    1127,     .1,     .73,    20,       2.42,  296,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-2215-1810',    1810,     .058,  1.35,    25,       2.42,  370,   1.3,	 1.1,      20,   9],
        ['Scorpion SII-3008-1090',    1105,     .117,   .79,    26,       3.35,  370,   1.3,	 1.1,     18, 9.15],
        ['Scorpion SII-3008-1220',    1105,     .0971,  .88,    26,       3.35,  425,   1.3,	 1.1,     16,    9],
        ['Scorpion SII-3014-830',      870,     .0732, 1.35,    30,       4.55,  550,   1.3,	 1.1,     15,   10],
        ['Scorpion SII-3014-1040',    1063,     .0589, 1.27,    40,       4.55,  600,   1.3,	 1.1,     15,  9.1],
        ['Scorpion SII-3014-1220',    1237,     .0503, 1.64,    46,       4.55,  640,   1.3,	 1.1,     10,    9],
        ['Scorpion SII-3020-780',      793,     .0598, 1.26,    40,       5.86,  800,   1.3,	 1.1,     17, 10.2],

        ['TowerPro TP2409_12D',       1600,     .071,   1.4,    25,       2.23,  190,    1.50,	 1.05,     40,   8],

        ['Turnigy 2020-3500',         3500,     .262,   .3,     10,       .39,   1.55,    1.5,  1.1,      60, 7.4],
        ['Turnigy C2222-2850',        2850,     .485,   .7,     10,       .53,   1.55,    1.5,  1.1,      60, 7.4],
        ['Turnigy C1826-2400',        2400,     .212,   .4,     10,       .64,   1.55,    1.5,  1.1,      60, 7.4],

        ['Turnigy C3542-1450 14p',    1400,     .044,   1.85,   55,       4.73,  400,    1.45,   1.0,      30, 7.1],
        ['Turnigy L2210C-1200',       1200,     .209,    0.95,  16,      1.69,   150,    1.45,   1.05,     40,  10],
        ['Turnigy 2213-20',            920,     .280,    .75,   19,       2.08,  180,    1.45,   1.05,     40,  12],
        ['Turnigy 2217-16',           1120,     .133,   1.15,   23,       2.51,  210,    1.45,   1.0,      40,11.5],
        ['Turnigy 2217-20',            940,     .190,    .94,   22,       2.51,  210,    1.45,   1.0,      40,12.4],
        ['Turnigy 2826-1650',         1570,     .163,    1.3,   16,       1.59,  135,    1.47,   1.05,     40,  11],
        ['Turnigy 2830-800',           960,     .245,    .86,   14,       2.01,  170,    1.50,   1.05,     10,  12],
        ['Turnigy 42-60 600',          620,     .085,    6.0,   50,       9.81,  830,    1.55,   1.0,      10,  15],
        ['Turnigy 50-45 890',          900,     .060,    2.0,   55,       9.18,  780,    1.55,   1.05,     10,   5],
        ['Turnigy 50-55A 400',         500,     .110,    2.7,   68,      10.59,  900,    1.50,   1.05,     10,  16],
        ['Turnigy 50-55B 600',         550,     .045,    5.0,   80,      10.59,  900,    1.45,   1.05,     10,18.5],
        ['Turnigy 80-100-A 180',       180,     .050,    3.5,  150,      55.41, 4710,    1.50,   1.07,     10,  20],


        ['Uberall Nippy 0508/73',      720,     .422,   .45,     5,       1.34,  115,    1.30,	 1.3,      40,	8],
        ['Uberall Nippy 0808/98',      970,     .255,   .7,      8,       1.4,   120,    1.30,	 1.4,      40,	8],
        ['Uberall Nippy 1208/180',    1700,     .195,   .5,     15,       2.4,   200,    1.30,	 1.4,      40,	8],
        ['Uberall Nippy 1812/100',    1020,     .064,   1.5,    25,       2.2,   190,    1.40,	 1.4,      40,	8],
        ['Uberall Nippy 2510/114',    1140,     .079,   2.0,    25,       2.2,   190,    1.50,	 1.0,      40,	8],

        ['XPWR 30CC',                  214,     .054,   1.2,    60,      18.92,  1600,   1.50,	 1.0,      20,8.4],
        ['XPWR 35CC',                  221,     .024,   2.1,    75,      27.32,  2300,   1.50,	 1.0,      20,8.4],
        ['XPWR 40CC',                  200,     .021,   2.2,    85,      30.75,  2600,   1.50,	 1.0,      20,8.4],
        ['XPWR 60CC',                  190,     .015,   3.0,   120,      41.23,  3500,   1.50,	 1.0,      20,8.4]
        ]
    li_1=[]
    if request.method == "POST":
        session['maxcurrent'] =float(request.form['maxcurrent'])
        session['maxpower'] =float(request.form['maxpower'])
        session['maxweight'] =float(request.form['maxweight'])
        try:
            for i in motorarray: #6power
                if i[6] >session['maxpower'] and i[5]>session['maxweight']/28.3495 and i[4]>session['maxcurrent']:
                    li_1.append(i)
            session['email']= request.cookies.get('email')
            session['pass']=request.cookies.get('pass')
            if session['email']==None:
                return render_template("suggest_motor.html",a='Login/signup',b='/login',ls=li_1)
            else:
                try:
                    d= user97.query.filter_by(email=session['email']).first()
                except:
                    flash("Error Came Try again")
                    return render_template('signup.html')
            return render_template('suggest_motor.html',a=d.username,b='/database',ls=li_1)
        except:
            flash("Enter values in input")
            return render_template("suggest_motor_form.html")

    else:
        session['email']= request.cookies.get('email')
        session['pass']=request.cookies.get('pass')
        if session['email']==None:
            return render_template("suggest_motor_form.html",a='Login/signup',b='/login')
        else:
            try:
                d= user97.query.filter_by(email=session['email']).first()
            except:
                flash("Error Came Try again")
                return render_template('signup.html')
            return render_template('suggest_motor_form.html',a=d.username,b='/database')

@app.route('/suggest/propeller',methods = ["GET","POST"])
def suggest_propeller():
    if request.method == "POST":
        ##var propArray = [ Tconst, 	Pconst,	Diam, 	Pich,   Blades,]
        d=[['Aeronaut 6x5 fixed E-prop',		.90,	.70,	6,	5,	2],
        ['Aeronaut 6.5x4 fixed E-prop',	        .84,	.68,	6.5,	4,	2],
        ['Aeronaut 7x7 fixed E-prop',	        .90,	.82,	7,	7,	2],
        ['Aeronaut 8.5x5 fixed E-prop',	        .66,	.53,	8.5,	5,	2],
        ['Aeronaut 8.5x6 fixed E-prop',	        .78,	.60,	8.5,	6,	2],
        ['Aeronaut 8.5x7 fixed E-prop',	        .89,	.70,	8.5,	7,	2],
        ['Aeronaut 9x5 fixed E-prop',	        1.1,	.98,	9,	5,	2],
        ['Aeronaut 9.5x5 fixed E-prop',	        .86,	.62,	9.5,	5,	2],
        ['Aeronaut 9.5x6 fixed E-prop',          .8,	.63,	9.5,	6,	2],
        ['Aeronaut 9.5x7 fixed E-prop',         .85,	.68,	9.5,	7,	2],
        ['Aeronaut 10x6 fixed E-prop',	        .78,	.62,	10,	6,	2],
        ['Aeronaut 10x7 fixed E-prop',	        .97,	.65,	10,	7,	2],
        ['Aeronaut 10x8 fixed E-prop',	        1.0,	.84,	10,	8,	2],
        ['Aeronaut 12x7 C Fold 42',	        .71,	.49,	12,	7,	2],
        ['Aeronaut 13x6.5 C Fold 42',	        .91,	.44,	13,   	6.5,	2],
        ['Aeronaut 13.5x7 C Fold 42',	        .73,	.44,	13.5,  	 7,	2],
        ['Aeronaut 14x7 C Fold 42',	        .74,	.62,	14,     7,	2],
        ['Aeronaut 8x5 CAM Fold 42',	        .81,	.72,	8,	5,	2],
        ['Aeronaut 9x5 CAM Fold 42',	        .77,	.70,	9,	5,	2],
        ['Aeronaut 9x7 CAM Fold 42',	        .80,	.81,	9,	7,	2],
        ['Aeronaut 9.5x5 CAM Fold 42', 	        .89,	.72,	9.5,	5,	2],
        ['Aeronaut 10x6 CAM Fold 42',	        .69,	.54,	10,	6,	2],
        ['Aeronaut 11x6 CAM Fold 42',	        .93,	.71,	11,	6,	2],
        ['Aeronaut 11x7 CAM Fold 42',	        .77,	.60,	11,	7,	2],
        ['Aeronaut 11x8 CAM Fold 42',	        .78,	.59,	11,	8,	2],
        ['Aeronaut 12x8 CAM Fold 42',	        .84,	.64,	12,	8,	2],
        ['Aeronaut 12x9 CAM Fold 42',	        .89,	.67,	12,	9,	2],
        ['Aeronaut 13x8 CAM Fold 42',	        .70,	.52,	13,	8,	2],
        ['Aeronaut 13x11 CAM Fold 42',	        .79,	.59,	13,    	11,	2],
        ['Aeronaut 14x8 CAM Fold 42',	        .94,	.74,	14,    	 8,	2],
        ['Align 5x3',			        .67,	.54,	5,	3,	2],
        ['Align 4.2x2',	       		       1.15,	.94,	4.2,	2,	2],
        ['APC E 4.1x4.1',      	               1.10,	.96,	4.1,  	4.1,	2],
        ['APC E 4.5x4.1',      	       	       1.09,	.94,	4.5,  	4.1,	2],
        ['APC E 4.7x4.2',			.95,	.81,	4.7,  	4.2,	2],
        ['APC E 4.75x4.5',		       1.05,	1.0,	4.75,  	4.5,	2],
        ['APC E 4.75x4.75',		        1.0,    .87,   	4.75, 	4.75,	2],
        ['APC E 4.75x5.5',		       1.05,    1.0,   	4.75,  	5.5,	2],
        ['APC E 5x5',			        .88,	.93,	5,	5,	2],
        ['APC E 5.25x4.75',		        .90,	.84,   	5.25, 	4.75,	2],
        ['APC E 5.5x4.5',     		        .87,	.85,   	5.5,   	4.5,	2],
        ['APC E 6x4',			        .88,	.73,	6,	4,	2],
        ['APC E 6x5.5',			        .98,	.84,	6,    	5.5,	2],
        ['APC E 7x4',	       		        .77,	.84,	7,	4,	2],
        ['APC E 7x5',	       		        1.1,	.83,	7,	5,	2],
        ['APC E 8x4',	       		       1.02,	.85,	8,	4,	2],
        ['APC E 8x6',	       		        1.1,   	1.02,	8,	6,	2],
        ['APC E 8x8',	       		       1.15,  	1.11,	8,	8,	2],
        ['APC E 9x4.5',	       		       1.01,	.78,	9,    	4.5,	2],
        ['APC E 9x6',			        .98,	.75,	9,	6,	2],
        ['APC E 9x7.5',			       1.08,	.95,	9,    	7.5,	2],
        ['APC E 9x9',			       1.03,	1.0,	9,    	9,	2],
        ['APC E 10x5',			        .97,	.74,   	10,     5,	2],
        ['APC E 10x7',          		.92,	.71,   	10,	7,	2],
        ['APC E 11x5.5',			.92,	.72,   	11,    	5.5,	2],
        ['APC E 11x7',	        		.88,	.69,   	11,	7,	2],
        ['APC E 11x8',          		.86,    .81,   	11,	8,	2],
        ['APC E 11x8.5',          		.90,   	.72,  	11,    	8.5,	2],
        ['APC E 12x6',			        .95,	.71,   	12,	6,	2],
        ['APC E 12x8',    			.87,	.67,   	12,	8,	2],
        ['APC E 12x12',    			.99,	.67,   	12,    	12,	2],
        ['APC E 13x4',         	       	       1.15,    .66,   	13,   	4,	2],
        ['APC E 13x6',         	        	.90,    .58,   	13,   	6,	2],
        ['APC E 13x6.5',       		        .92,    .67,   	13,    	6.5,	2],
        ['APC E 13x8',			        .87, 	.59,   	13,	8,	2],
        ['APC E 14x7',	        		.91,	.60,   	14,	7,	2],
        ['APC E 14x10',			        .88,	.63,   	14,     10,	2],
        ['APC E 15x8',			        .93,	.71,   	15,      8,	2],
        ['APC E 16x8',		               1.08,	.69,   	16,      8,	2],
        ['APC E 17x8',		        	.94,	.61,   	17,      8,	2],
        ['APC E 17x10',		        	.80,	.64,   	17,     10,	2],
        ['APC E 18x8',		       	       1.08,	.71,   	18,      8,	2],
        ['APC E 20x10',		        	.98,	.62,   	20,     10,	2],
        ['APC E 22x10',		        	.94,	.56,   	22,     10,	2],
        ['APC Sport 7x6',			1.0,	1.0,   	7,      6,	2],
        ['APC Sport 10x6',			.80,	.71,   	10,      6,	2],
        ['APC Sport 11x5',          		.98,	.68,   	11,	5,	2],
        ['APC Sport 11x6',	       		.88,	.72,   	11,	6,	2],
        ['APC Sport 11x8',          		.90,    .79,   	11,	8,	2],
        ['APC Sport 12x7',			.81,	.69,   	12,	7,	2],
        ['APC Sport 13x7',       		.84,    .62,   	13,     7,	2],
        ['APC Sport 15x8',      		.89,    .67,   	15,     8,	2],
        ['APC Sport 16x8',      		.95,    .68,   	16,     8,	2],
        ['APC Sport 16x10',      		.80,    .65,   	16,     10,	2],
        ['APC Sport 16x12',      		.85,    .67,   	16,     12,	2],
        ['APC Sport 18x6',             		1.12,   .65,   	18,      6,	2],
        ['APC SF 7x3.8',          		1.4,   1.55,     7,    3.8,	2],
        ['APC SF 7x4',          		1.03,   .95,     7,      4,	2],
        ['APC SF 7x5',          		1.07,   .95,     7,      5,	2],
        ['APC SF 7x6',          		1.25,   .93,     7,	 6,	2],
        ['APC SF 8x3.8',        		1.3,	1.17,   8,    	3.8,	2],
        ['APC SF 8x6',          		1.53,	1.45,   8,	6,	2],
        ['APC SF 9x3.8',        		1.3,	1.0,	9,    	3.8,	2],
        ['APC SF 9x4.7',        		1.1,    .85,    9,    	4.7,	2],
        ['APC SF 9x6',			        1.5,	1.25,   9,      6,	2],
        ['APC SF 10x3.8',			1.47,	1.17,  	10,    	3.8, 	2],
        ['APC SF 10x4.7',			1.4,	 .95,  	10,    	4.7,	2],
        ['APC SF 10x7',         		1.45,   1.3,   	10,      7,	2],
        ['APC SF 11x4.7',       		1.4,     .95,  	11,    	4.7,	2],
        ['APC SF 11x7',         		1.4,	1.07,  	11,      7,	2],
        ['APC SF 12x3.8',         		1.5,    1.18,  	12,    	3.8,	2],
        ['APC SF 12x6',         		1.48,    1.2,  	12,      6,	2],
        ['Dymond-E 15x8',      	        	.93,    .74,   	15,      8,	2],
        ['EM E-prop Metts 15x8',      		.90,    .70,   	15,      8,	2],
        ['EM E-prop Metts 16x7',      		.92,    .65,   	16,     7,	2],
        ['EM E-prop Metts 16x8',      		.99,    .68,   	16,      8,	2],
        ['GemFan 5x3',			        .72,	.65,	5,	3,	2],
        ['GemFan 5x4.5',		     	.90,	.65,	5,	4.5,	2],
        ['GemFan 6x3',			        .65,	.44,	6,	3,	2],
        ['Graupner CAM Speed 4.7x4.7',	       1.02,    1.1,  	4.7,   	4.7,	2],
        ['Graupner Nylon 5x2',	         	.22,    .88,    5,     	2,	2],
        ['Graupner CAM Speed 5.2x5.2',	        .96,	 .85,  	5.2,   	5.2,	2],
        ['Graupner CAM Speed 5.5x4.3',	        .82,	 .83,  	5.5,   	4.3,	2],
        ['Graupner Speed 5.5x5.5',	 	.95,	 .83,  	5.5,   	5.5,	2],
        ['Graupner Speed 6x5.5',	 	.91,	 .72,    6,   	5.5,	2],
        ['Graupner Speed 6x6',	 	        1.0,	 .74,    6,     6,	2],
        ['Graupner Speed 6.5x6.5',      	.82,     .71,  	6.5,   	6.5,	2],
        ['Graupner Speed 7x7',	 	         .8,	 .7,    7,     	7,	2],
        ['Graupner CAM Folding 8x6',	        .83,	 .75,   8,     	6,	2],
        ['Graupner CAM Folding 9x6',	 .88,	 .75,    	9,     	6,	2],
        ['Graupner CAM Folding 10x6',	 .77,	 .63,   	10,     	6,	2],
        ['Graupner CAM Folding 11x6',	 .8,	 .65,   	11,     	6,	2],
        ['Graupner CAM Folding 12x6',	 .81,	 .6,    	12,     	6,	2],
        ['Graupner CAM Folding 13x7',	 .81,	 .58,   	13,     	7,	2],
        ['Graupner CAM Folding 14x9.5',	 .85,	 .52,   	14,   	9.5,	2],
        ['Graupner CAM Folding 16x10',	 .61,	 .53,   	16,    	10,	2],
        ['Graupner Slim 8x4',		 .94,	 1.4,    	8,     	4,	2],
        ['Graupner Slim 8x6',		 .97,	 .77,    	8,     	6,	2],
        ['Graupner Slim 9x5',		 .82,	 .72,    	9,     	5,	2],
        ['Graupner Slim 10x6',		 1.01,	 .9,    	10,     	6,	2],
        ['Graupner Slim 10x8',	         	1.11,	 .95,   	10,     	8,	2],
        ['GWS 2.5x0.8',			 1.0,	 1.0,  	2.5,   	0.8,	2],
        ['GWS 2.5x1.0',			 .89,	 1.1,  	2.5,   	1.0,	2],
        ['GWS HD 3x2',			 1.15,	 1.5,    	3,     	2,	2],
        ['GWS HD 3x3',			 1.4,	 1.7,    	3,     	3,	2],
        ['GWS HD 4x2.5',	        		 0.92,	 1.0,    	4,   	2.5,	2],
        ['GWS HD 4x4',	                 	1.23,	 1.0,    	4,     	4,	2],
        ['GWS HD 4.5x3',	         		.94,	 .82,  	4.5,     	3,	2],
        ['GWS HD 4.5x4',	         		1.16,	 .75,  	4.5,     	4,	2],
        ['GWS HD 5x3',			 .79,	  .66,   	5,     	3,	2],
        ['GWS HD 5x4.3',		 	1.18,	  .72,   	5,   	4.3,	2],
        ['GWS HD 6x3',			 .84,	  .65,   	6,     	3,	2],
        ['GWS HD 6x3 3-Blade',		.76,	  .74,   	6,     	3,	3],
        ['GWS HD 7x3.5',	         		.65,	  .44,   	7,   	3.5,	2],
        ['GWS HD 7x3.5 3-Blade',	         	.69,	  .62,   	7,   	3.5,	3],
        ['GWS HD 8x4',			 .88,	  .62,   	8,     	4,	2],
        ['GWS HD 8x4 3-Blade pusher',	 .86,	  .9,   	8,     	4,	3],
        ['GWS HD 8x4 3-Blade tractor',	 .76,	  .75,   	8,     	4,	3],
        ['GWS HD 8x6',			 1.0,	  .82,   	8,     	6,	2],
        ['GWS HD 9x5',			 .95,	  .66,   	9,     	5,	2],
        ['GWS HD 10x6',			 .80,	  .57,  	10,     	6,	2],
        ['GWS HD 10x8',			 1.03,	  .75,  	10,     	8,	2],
        ['GWS HD 11x7',		         	.90,	  .60,  	11,     	7,	2],
        ['GWS RS 6x5',			 1.29,	  .96,   	6,     	5,	2],
        ['GWS RS 7x6',			 1.32,	  1.22,  	7,     	6,	2],
        ['GWS RS 8x4.3',		 	1.07,	   .76,  	8,   	4.3,	2],
        ['GWS RS 8x6',			 1.06,	  1.04,  	8,     	6,	2],
        ['GWS RS 9x4.7',		 	1.21,	   .89,  	9,   	4.7,	2],
        ['GWS RS 9x7',			 1.31,	   .96, 	9,     	7,	2],
        ['GWS RS 9x7 3-Blade',		 1.05,	   .9, 	9,     	7,	3],
        ['GWS RS 10x4.7',		 	1.38,	  1.1,  	10,   	4.7,	2],
        ['GWS RS 10x8',		 	1.39,	  1.1,  	10,     	8,	2],
        ['GWS RS 11x4.7',		 	1.42,	1.04,  	11,    	4.7,	2],
        ['Günter 4.9x4.3',		 	1.33,	  1.2,  	4.9,  	4.3,	2],
        ['Günter 5x4.3',		 	1.31,	  .74,    	5,  	4.3,	2],
        ['Günter 5.1x4.3',		 	1.47,	  .96,  	5.1,  	4.3,	2],
        ['Master Airscrew GF 8x4',		 .87,	  1.04,  	8,    	4,	2],
        ['Master Airscrew 8x5.5',		 1.04,	  1.64,  	8,   	5.5,	2],
        ['Master Air. electric 6x4 3-Blade',	 .8,	  1.06,  	6,    	4,	3],
        ['Master Airscrew electric 8x5.5',	 .95,	  1.3,    	8,   	5.5,	2],
        ['Master Airscrew electric 9x6',	 1.08,	  1.52,  	9,     	6,	2],
        ['Master Airscrew electric 10x6',	 1.23,	  1.68,  	10,     	6,	2],
        ['Master Airscrew electric 10x7',	 1.18,	  1.22,  	10,     	7,	2],
        ['Ramoser 15x12 3-Blade SG',	 1.45,	  1.24,  	15,     	12,	3],
        ['Ramoser 15x14 3-Blade SG',	 1.69,	  1.33,  	15,     	14,	3],
        ['Ramoser 15.2x15 5-Blade',	 	 .97,	  .77,  	15.2,     	15,	5],
        ['Ramoser 16.6x14 3-Blade',	 	 .75,	  .68,  	16.6,     	14,	3],
        ['Ramoser 16.6x14 4-Blade',	 	 .85,	  .71,  	16.6,     	14,	4],
        ['Ramoser 16.6x16 3-Blade',	 	 .86,	  .66,  	16.6,     	16,	3],
        ['Ramoser 16.6x16 4-Blade',	 	 .95,	  .74,  	16.6,     	16,	4],
        ['Zagi Carbon 5.1x4.9',		 1.11,	  1.14, 	5.1,  	4.9,	2]
        ]
        li_2=[]
        session['s_dia'] =float(request.form['s_dia'])
        session['s_pit'] = float(request.form['s_pit'])
        session['s_nob'] = float(request.form['s_nob'])
        if session['s_nob']=="" and session['s_pit']=="" and session['s_dia']=="":
            flash("Enter values in input")
            return render_template("suggest_Propeller_form.html")
        else:
            for i in d:
                if session['s_dia']<=i[-3] and session['s_pit']<=i[-2] and session['s_nob']<=i[-1]:
                    li_2.append(i)
            session['email']= request.cookies.get('email')
            session['pass']=request.cookies.get('pass')
            if session['email']==None:
                return render_template("suggest_Propeller.html",a='Login/signup',b='/login',ls=li_2)
            else:
                try:
                    d= user97.query.filter_by(email=session['email']).first()
                except:
                    flash("Error Came Try again")
                    return render_template('signup.html')
            return render_template('suggest_Propeller.html',a=d.username,b='/database',ls=li_2)

    session['email']= request.cookies.get('email')
    session['pass']=request.cookies.get('pass')
    if session['email']==None:
        return render_template("suggest_Propeller_form.html",a='Login/signup',b='/login')
    else:
        try:
            d= user97.query.filter_by(email=session['email']).first()
        except:
            flash("Error Came Try again")
            return render_template('signup.html')
        return render_template('suggest_Propeller_form.html',a=d.username,b='/database')
    return render_template('suggest_Propeller_form.html')
'''if __name__ == '__main__':
    db.create_all()
    app.run(host="192.168.43.206",debug = True)'''
if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)