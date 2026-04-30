import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # جيب البيانات من الفورم
        name  = request.form.get("name")
        month = request.form.get("month")
        day   = request.form.get("day")

        # التحقق من الإدخال
        if not name or not month or not day:
            return redirect("/")

        # أضف في قاعدة البيانات
        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)",
            name, month, day
        )

        return redirect("/")

    else:
        # جيب كل أعياد الميلاد
        birthdays = db.execute("SELECT * FROM birthdays ORDER BY month, day")
        return render_template("index.html", birthdays=birthdays)

@app.route("/delete/<int:id>")
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/") 

