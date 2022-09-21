from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3
from hashids import Hashids


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ewmjqoieuhwquoi423125fs'

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


@app.route('/', methods =['GET', 'POST'])
def index():
    connection = get_db_connection()

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