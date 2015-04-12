from flask import render_template, redirect, url_for, abort
from general import log
from app.flask import create_application
from app.senpai import Senpai

app = create_application(__name__)


@app.route('/')
def root():
    log.warn("Redirect / -> /lang")
    return redirect(url_for('main', lang='en'))


@app.route('/<lang>')
def main():
    title = "Home"
    return render_template('main.html', **locals())


@app.route('/<lang>/game/<region>/<username>')
def match(region, username):
    title = username + "'s match"
    senpai = Senpai(region, username)
    # try:
    # except Exception as e:
    #     abort(503, {'message': "Internal server error: %s" % str(e)})
    return render_template('game.html', **locals())


if __name__ == '__main__':
    log.info("Start application...")
    app.run(debug=True)
