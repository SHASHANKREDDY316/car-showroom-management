from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

# ------------------ JSON STORAGE ------------------

DATA_FILE = "cars.json"

def load_cars():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_cars(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

cars = load_cars()

# ------------------ ROUTES ------------------

# 🔐 START → LOGIN PAGE
@app.route('/')
def root():
    return redirect(url_for('login'))


# 🏠 HOME PAGE
@app.route('/home')
def home():
    return render_template('home.html')


# ------------------ LOGIN ------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return jsonify({"status": "success"})
    return render_template('login.html')


# ------------------ ADD CAR ------------------

@app.route('/addcar', methods=['GET','POST'])
def addcar():
    if request.method == 'POST':
        cars.append({
            "name": request.form['name'],
            "model": request.form['model'],
            "price": request.form['price'],
            "owner": request.form['owner']
        })
        save_cars(cars)
        return redirect(url_for('viewcars'))

    return render_template('addcar.html')


# ------------------ VIEW CARS ------------------

@app.route('/viewcars')
def viewcars():
    query = request.args.get('search', '').lower()

    if query:
        filtered = [
            car for car in cars
            if query in car['name'].lower() or query in car['model'].lower()
        ]
    else:
        filtered = cars

    return render_template('viewcars.html', cars=filtered)


# ------------------ DELETE ------------------

@app.route('/delete/<int:index>')
def delete(index):
    if index < len(cars):
        cars.pop(index)
        save_cars(cars)
    return redirect(url_for('viewcars'))


# ------------------ EDIT ------------------

@app.route('/edit/<int:index>', methods=['GET','POST'])
def edit(index):
    car = cars[index]

    if request.method == 'POST':
        car['name'] = request.form['name']
        car['model'] = request.form['model']
        car['price'] = request.form['price']
        car['owner'] = request.form['owner']
        save_cars(cars)
        return redirect(url_for('viewcars'))

    return render_template('editcar.html', car=car)


# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)