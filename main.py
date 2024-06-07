# -*- coding: UTF-8-*-

from flask import Flask, request, flash, redirect, url_for, render_template, jsonify
from datetime import datetime
import webbrowser
from modules import *


# create Flask app
app = Flask(__name__)
app._static_folder = "./templates/static"
app.secret_key = "your_secret_key"


# main page
@app.route("/")
def index():
    return render_template("index.html")


# routing "addUser" function
@app.route("/newuser", methods=["POST"])
def new_user():
    name = request.form.get("name")
    birthday = request.form.get("birthday")
    gender = request.form.get("gender")
    height = request.form.get("height")

    # 檢查日期格式
    if not birthday:
        flash("請輸入有效的日期格式 (yyyy-mm-dd)", "error")
        return redirect(url_for("index"))

    try:
        birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
        if birthday_date > datetime.today().date():
            flash("日期不能超過今天", "error")
            return redirect(url_for("index"))

    except ValueError:
        flash("請輸入有效的日期格式 (yyyy-mm-dd)", "error")
        return redirect(url_for("index"))

    try:
        height = float(height)  # type: ignore
        if height < 0 or height > 300:  # 金氏世界紀錄最高身高的紀錄272cm
            flash("請輸入有效的身高", "error")
            return redirect(url_for("index"))
    except ValueError:
        flash("身高僅能輸入數字", "error")
        return redirect(url_for("index"))

    addUser(name, birthday_date, gender, height)  # 確保存儲浮點數
    return redirect(url_for("index"))


# routing "addHealthData" function
@app.route("/newhealthdata", methods=["POST"])
def new_health_data():
    user_id = request.form.get("user_id")
    weight = request.form.get("weight")
    bpc = request.form.get("blood_pressure_c")
    bpr = request.form.get("blood_pressure_r")
    bs = request.form.get("blood_sugar")
    date = datetime.now().strftime("%Y-%m-%d")

    # check weight value
    try:
        weight = float(weight)  # type: ignore
        if weight <= 0:
            flash("請輸入有效的體重", "error")
            return redirect(url_for("index"))
    except ValueError:
        flash("請輸入有效的體重", "error")
        return redirect(url_for("index"))

    # check blood pressure value
    try:
        bpc = float(bpc)  # type: ignore
        bpr = float(bpr)  # type: ignore

        if bpc <= bpr:
            flash("舒張壓高於收縮壓", "error")
            return redirect(url_for("index"))
    except ValueError:
        flash("請輸入有效的血壓值", "error")
        return redirect(url_for("index"))

    # check blood sugar value
    try:
        bs = float(bs)  # type: ignore
        if bs <= 0:
            flash("請輸入有效的血糖值", "error")
            return redirect(url_for("index"))
    except ValueError:
        flash("請輸入有效的血糖值", "error")
        return redirect(url_for("index"))

    addHealthData(user_id, date, weight, bpc, bpr, bs)
    removeOldPicture()
    return redirect(url_for("index"))


# routing "delUser"
@app.route("/deleteuser/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    delUser(user_id)
    return redirect(url_for("index"))


# routing "healthHistory" function
@app.route("/healthhistory", methods=["POST"])
def health_history():
    user_id = request.form.get("user_id")

    healthHistory(user_id)
    return redirect(url_for("index"))


# routing "userList" function
@app.route("/userlist", methods=["GET"])
def get_user_list():
    users = userList()
    user_list = [
        {
            "id": user[0],
            "name": user[1],
            "birthday": user[2],
            "gender": user[3],
            "height": user[4],
        }
        for user in users
    ]
    return jsonify(user_list)


if __name__ == "__main__":
    tableChecker()
    removeOldPicture()
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
