from flask import Flask, render_template, request, redirect, url_for
import os, json, base64

app = Flask(__name__)
DATA_FILE = 'passwords.json'

def load_passwords():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_passwords(passwords):
    with open(DATA_FILE, 'w') as f:
        json.dump(passwords, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    passwords = load_passwords()
    if request.method == 'POST':
        site = request.form['site']
        username = request.form['username']
        password = request.form['password']
        passwords[site] = {
            'username': username,
            'password': base64.b64encode(password.encode()).decode()
        }
        save_passwords(passwords)
        return redirect(url_for('index'))
    return render_template('index.html', passwords=passwords)

@app.route('/view/<site>')
def view_password(site):
    passwords = load_passwords()
    entry = passwords.get(site)
    if not entry:
        return 'No encontrado', 404
    pwd = base64.b64decode(entry['password']).decode()
    return render_template('view.html', site=site, username=entry['username'], password=pwd)

@app.route('/edit/<site>', methods=['GET', 'POST'])
def edit_password(site):
    passwords = load_passwords()
    if site not in passwords:
        return 'No encontrado', 404

    if request.method == 'POST':
        new_site = request.form['site']
        username = request.form['username']
        password = request.form['password']
        if new_site != site:
            passwords.pop(site)
        passwords[new_site] = {
            'username': username,
            'password': base64.b64encode(password.encode()).decode()
        }
        save_passwords(passwords)
        return redirect(url_for('index'))

    entry = passwords[site]
    pwd = base64.b64decode(entry['password']).decode()
    return render_template('edit.html', site=site, username=entry['username'], password=pwd)

@app.route('/delete/<site>', methods=['POST'])
def delete_password(site):
    passwords = load_passwords()
    if site in passwords:
        passwords.pop(site)
        save_passwords(passwords)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
