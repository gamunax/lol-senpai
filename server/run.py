from flask import render_template, redirect, url_for, abort
from general import log
from app.flask import create_application, page_error
from app.senpai import Senpai
from flask.ext.babel import gettext, ngettext
import library.api.errors as errors

app = create_application(__name__)


@app.route('/')
def root():
    log.warn("Redirect / -> /lang")
    return redirect(url_for('main', lang='en'))


@app.route('/<lang>')
def main():
    title = gettext("Home")
    return render_template('main.html', **locals())


@app.route('/<lang>/about')
def about():
    title = gettext("About")
    return render_template('about.html', **locals())


@app.route('/<lang>/game/<region>/<username>')
def match(region, username):
    title = gettext("%(summoner)s's match", summoner=username)
    try:
        senpai = Senpai(region, username)
    except errors.SUMMONERS_NOT_FOUND:
        return page_error(title=gettext("Summoner not found"), message=gettext("This summoner doesn't exist in this region."), code=404)
    except errors.GAME_NOT_FOUND:
        return page_error(title=gettext("Game not found"), message=gettext("This summoner is not in game."), code=400)
    except errors.GAME_NOT_RANKED:
        return page_error(title=gettext("Game not compatible"), message=gettext("Lol-Senpai works only for ranked games."), code=400)
    except errors.SERVER_ERROR:
        return page_error(title=gettext("Server error"), message=gettext("Unable to connect to the Riot's API."), code=500)
    except errors.RATE_LIMIT_EXCEEDED:
        return page_error(title=gettext("Rate limit exceeded"),
                          message=gettext("Rate limit exceeded :(. Could you please try again in a few moments ?"), code=500)
    except errors.LoLSenpaiException:
        return page_error(title=gettext("Error Riot's API"), message=gettext("Error with the Riot's API."), code=500)
    except Exception as e:
        log.error("ERROR EXCEPTION: %s" % str(e), exc_info=1)
        return page_error(title=gettext("Internal server error"),
                          message=gettext("Unknown error :(. Could you please try again in a few moments ?"), code=500)
    return render_template('game.html', **locals())


if __name__ == '__main__':
    log.info("Start application...")
    app.run(debug=True)
