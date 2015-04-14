from flask import render_template, redirect, url_for, abort
from general import log
from app.flask import create_application, page_error
from app.senpai import Senpai
import library.api.errors as errors

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
    try:
        senpai = Senpai(region, username)
    except errors.SERVER_ERROR:
        return page_error(title="Server error", message="Unable to connect to the Riot's API.", code=500)
    except errors.RATE_LIMIT_EXCEEDED:
        return page_error(title="Rate limit exceeded", message="Rate limit exceeded. :( Could you please try again in a few moments?", code=500)
    except errors.LoLSenpaiException:
        return page_error(title="Error Riot's API", message="Error with the Riot's API.", code=500)
    except Exception:
        return page_error(title="Internal server error", message="Unknown error. :( Could you please try again in a few moments?", code=500)
    return render_template('game.html', **locals())


if __name__ == '__main__':
    log.info("Start application...")
    app.run(debug=True)
