import json
from flask import Flask, render_template, request

app = Flask(__name__)


def get_users():
    with open('users.json', 'r', encoding='utf-8') as fp:
        return json.load(fp)


USERS = get_users()


@app.route('/')
def index():
    return render_template('index.html', users=USERS, title="Все пользователи")


@app.route('/search/', methods=['GET'])
def search():
    name = request.args.get('name', '').lower()
    results = [] if not name else [user for user in USERS if name in user['name'].lower()]
    return render_template('search.html', users=results, title="Поиск")


@app.route('/add_user/', methods=['GET', 'POST'])
def add_user():
    new_user = {}
    if request.method == 'POST':
        name = request.form.get('name', '')
        age = request.form.get('age', '')
        disabled = request.form.get('disabled', '')
        unblock_date = request.form.get('unblock_date', '')
        if name:
            new_user['name'] = name
        if age:
            new_user['age'] = age
        if disabled == 'on':
            new_user['is_blocked'] = True
            if unblock_date:
                new_user['unblock_date'] = unblock_date
        USERS.append(new_user)
    return render_template('add_user.html', user=new_user, title="Добавить")


if __name__ == '__main__':
    app.run()
