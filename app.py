from flask import Flask, render_template, request
import numpy as np
import pickle
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__)

# dialect+driver://username:password@host:port/database

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://username:Password1@hostip/databasename?driver=SQL+Server'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Workers(db.Model):
    __tablename__ = 'tablename'  # Case sensitive.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    Age = db.Column(db.Integer)
    MaritalStatus = db.Column(db.Integer)
    OverTime = db.Column(db.Integer)
    NumCompaniesWorked = db.Column(db.Integer)
    YearsAtCompany = db.Column(db.Integer)
    MonthlyIncome = db.Column(db.Integer)
    TotalWorkingYears = db.Column(db.Integer)
    YearsInCurrentRole = db.Column(db.Integer)
    StockOptionLevel = db.Column(db.Integer)
    YearsWithCurrManager = db.Column(db.Integer)


def databaseQuery(_name, _surname):

    calledworker = Workers.query.filter_by(name=_name, surname=_surname).first()


    workername = calledworker.name
    workersurname = calledworker.surname


    age = calledworker.Age
    MaritalStatus = calledworker.MaritalStatus
    OverTime = calledworker.OverTime
    NumCompaniesWorked = calledworker.NumCompaniesWorked
    YearsAtCompany = calledworker.YearsAtCompany
    MonthlyIncome = calledworker.MonthlyIncome
    TotalWorkingYears = calledworker.TotalWorkingYears
    YearsInCurrentRole = calledworker.YearsInCurrentRole
    StockOptionLevel = calledworker.StockOptionLevel
    YearsWithCurrManager = calledworker.YearsWithCurrManager

    data_list = [age, MaritalStatus, OverTime, NumCompaniesWorked, YearsAtCompany,
                 MonthlyIncome, TotalWorkingYears, YearsInCurrentRole, StockOptionLevel,
                 YearsWithCurrManager]

    return workername, workersurname, data_list


def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 10)
    loaded_model = pickle.load(open("simplifiedmodel.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route("/")
def girisEkrani():
    return render_template("girisekrani.html")




@app.route("/veritabanisorgulama")
def veritabaniSorgulama():
    return render_template("veritabanisorgulama.html")


@app.route("/veritabanisonuc", methods=['POST'])
def veritabaniSonuc():
    if request.method == 'POST':
        global textcolor
        global bcolor
        name_surname = request.form.to_dict()
        name_surname = list(name_surname.values())
        # name_surname = list(map(int, name_surname))
        name, surname, datos = databaseQuery(name_surname[0], name_surname[1])
        datos = list(map(int, datos))
        result = ValuePredictor(datos)
        if int(result) == 1:
            prediction = 'Yıpranmışlık Tahmini: POZİTİF'
            bcolor = "#800000"  # Dark Red.
            textcolor = "#ffffff"  # White
        else:
            prediction = 'Yıpranmışlık Tahmini: NEGATİF'
            bcolor = "#7CFC00"  # LawnGreen
            textcolor = "#000000"  # Black

        return render_template("veritabanisonuc.html", prediction = prediction, name = name, surname = surname, datos = datos , color = textcolor, bcolor = bcolor)



# Bilgileri manual girerek sorgulama

@app.route("/manualsorgulama")
def manualSorgulama():
    return render_template("manualsorgulama.html")


@app.route("/manualsonuc", methods=['POST'])
def manualSonuc():
    global textcolor
    global bcolor
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        if int(result) == 1:
            prediction = 'Yıpranmışlık Tahmini: POZİTİF'
            bcolor = "#800000"  # Dark Red.
            textcolor = "#ffffff"  # White

        else:
            prediction = 'Yıpranmışlık Tahmini: NEGATİF'
            bcolor = "#7CFC00"  #LawnGreen
            textcolor = "#000000" # Black

        return render_template("manualsonuc.html", prediction = prediction, color = textcolor, bcolor = bcolor)


if __name__ == '__main__':
    app.run()
