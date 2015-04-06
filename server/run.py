from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    title = "Home"
    return render_template('main.html', **locals())


@app.route('/match/<username>')
def match(username):
    title = username + "'s match"
    return render_template('match.html', **locals())


if __name__ == '__main__':
    app.run(debug=True)
