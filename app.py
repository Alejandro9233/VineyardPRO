from flask import Flask, render_template
from db import load_hectares_from_db, load_weather, load_users_from_db, load_vineyards_from_db

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    users = load_users_from_db()
    vineyards = load_vineyards_from_db()
    hectare = load_hectares_from_db()
    temperature = load_weather()
    return render_template('index.html', users=users, vineyards=vineyards, hectare = hectare, temperature=temperature)

if __name__ == '__main__':
    app.run(debug = True)