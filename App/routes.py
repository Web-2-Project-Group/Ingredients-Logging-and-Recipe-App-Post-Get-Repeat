from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy user data for demonstration
users = {"testuser": "password123"}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/daily-recipes")
def daily_recipes():
    return render_template("daily_recipes.html")

@app.route("/my-recipes")
def my_recipes():
    return render_template("my_recipes.html")

@app.route("/my-ingredients")
def my_ingredients():
    return render_template("my_ingredients.html")