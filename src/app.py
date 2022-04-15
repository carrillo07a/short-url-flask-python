from flask import Flask, render_template, url_for, flash, request, redirect, jsonify
from flask_mysql_connector import MySQL
import shortuuid

# Init
app = Flask(__name__)

# Endpoint
endpoint = 'http://short.url'

# Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = 'shorturl'

# Init DB
mysql = MySQL(app)

# Key Secret
app.secret_key = "clv3rt64sjksfl"

# Path
@app.route('/', methods=['GET'])
def init():
    try:
        return render_template('index.html'), 200
    except:
        return render_template('404.html'), 404


@app.route('/generate', methods=['POST'])
def generate():
    try:
        if request.method == 'POST':
            # Get Url
            url = request.form['url']
            cursor = mysql.connection.cursor()
            # loop valid duplicate
            while True:
                url_short = shortuuid.ShortUUID().random(length=5)
                # Check db
                cursor.execute("SELECT * FROM tbl_url WHERE url_short = BINARY %s", (url_short,))

                if not cursor.fetchone():
                    break

                    # Valid Data
            cursor.execute("SELECT * FROM tbl_url WHERE url_short = BINARY %s", (url,))
            data_sql = cursor.fetchone()
            if data_sql:
                flash(endpoint + '/' + data_sql[0])
                return redirect(url_for('init')), 302

            # Insert Url
            cursor.execute("INSERT INTO tbl_url (url, url_short)VALUES (%s, %s)", (url, url_short))

            # save
            mysql.connection.commit()

            # Close
            cursor.close()

        flash(endpoint + '/' + url_short)
        return redirect(url_for('init')), 302
    except Exception as e:
        return render_template('404.html'), 404


@app.route('/<id>')
def get_url_id(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT url FROM tbl_url WHERE url_short = BINARY %s", (id,))
        data = cursor.fetchone()
        cursor.close()
        return render_template('ads.html', url=data[0]), 200
    except Exception as e:
        return render_template('404.html'), 404


# Run
if __name__ == "__main__":
    app.run(port=80, debug=True)
