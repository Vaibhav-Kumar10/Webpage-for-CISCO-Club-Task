from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


users = {}


@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')  


@app.route('/', methods=['GET'])
def signin_page():
    return render_template('signin.html')  


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    
    if username in users:
        return jsonify({'status': 'error', 'message': 'User already exists'}), 400

   
    users[username] = password
    return jsonify({'status': 'success', 'message': 'User signed up successfully'}), 201


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')


    if username in users and users[username] == password:
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
