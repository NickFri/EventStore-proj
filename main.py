from flask import Flask, request, render_template, redirect, url_for, session
from esdbclient import EventStoreDBClient, NewEvent, StreamState
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Setup your EventStoreDBClient here
client = EventStoreDBClient(uri="esdb://localhost:2113?Tls=false")

# Example of logging an event
stream_name = str(uuid.uuid4())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you should implement your authentication logic
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('select_food'))
        return 'Invalid credentials!'
    return render_template('login.html')


@app.route('/select-food', methods=['GET', 'POST'])
def select_food():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        food_choice = request.form['food']

        username = session['username']
        event = NewEvent(
            type='FoodSelected',
            data=f'{{"user": "{username}", "food": "{food_choice}"}}'.encode()
        )
        client.append_to_stream(stream_name, current_version=StreamState.NO_STREAM, events=[event])

        return redirect(url_for('select_drink'))

    return render_template('select_food.html')


@app.route('/select-drink', methods=['GET', 'POST'])
def select_drink():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        drink_choice = request.form['drink']

        username = session['username']
        event = NewEvent(
            type='FoodSelected',
            data=f'{{"user": "{username}", "food": "{drink_choice}"}}'.encode()
        )
        client.append_to_stream(stream_name, current_version=StreamState.NO_STREAM, events=[event])

        return 'Order completed!'

    return render_template('select_drink.html')


if __name__ == '__main__':
    app.run(debug=True)
