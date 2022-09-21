from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
from hashids import Hashids
import os.path
import init_db 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")


def get_db_connection():
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ewmjqoieuhwquoi423125fs'

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


@app.route('/', methods =['GET', 'POST'])
def index():
    connection = get_db_connection()
    print(connection)
    print(db_path)

    if request.method == 'POST':
        url = request.form['url']
        url_data = connection.execute('INSERT INTO urls (original_url) VALUES (?)', (url,))
        connection.commit()
        connection.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid 

        return render_template('index.html', short_url = short_url)
    
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(debug=True)
    init_db.run()