__author__ = 'Dewep'


from flask import Flask, render_template, request, g, abort
from flask.ext.babel import Babel
from general import log


def page_error(error=None, code=400, title=None, message=None):
    if not title:
        if error:
            title = str(error)
            if title[:5] == ("%d: " % code):
                title = title[5:]
        else:
            title = "Error"
    if message:
        pass
    elif error and 'message' in error.description:
        message = error.description['message']
    elif code == 404:
        message = "Page not found... Fiddlestick got lost! :("
    else:
        message = title
    return render_template('error.html', **locals()), code


def create_application(root):
    app = Flask(root)
    babel = Babel(app)

    @app.before_request
    def before_request():
        g.lang = 'en'
        if request.view_args and 'lang' in request.view_args:
            g.lang = request.view_args['lang']
            if g.lang not in ('en', 'fr'):
                g.lang = 'en'
                return abort(404, {'message': "Language not found."})
            request.view_args.pop('lang')
        if request.view_args and 'region' in request.view_args:
            region = request.view_args['region']
            from library.api.constants import REGIONAL_ENDPOINTS
            if region not in REGIONAL_ENDPOINTS:
                return abort(404, {'message': "Region not found."})

    @babel.localeselector
    def get_locale():
        log.info("Language: " + g.get('lang', 'en'))
        return g.get('lang', 'en')

    def page_errors(error):
        try:
            code = int(str(error)[:3])
        except:
            code = 503
        return page_error(error, code)

    for error_code in [400, 403, 404, 503, 509]:
        app.register_error_handler(error_code, page_errors)

    return app
