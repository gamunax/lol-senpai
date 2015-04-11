__author__ = 'Dewep'


from flask import Flask, render_template, request, g, abort
from flask.ext.babel import Babel
from general import log


def create_application(root):
    app = Flask(root)
    babel = Babel(app)

    @app.before_request
    def before_request():
        if request.view_args and 'lang' in request.view_args:
            g.lang = request.view_args['lang']
            if g.lang not in ('en', 'fr'):
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

    def page_error(error, code):
        title = str(error)
        if title[:5] == ("%d: " % code):
            title = title[5:]
        message = error.description['message'] if 'message' in error.description else title
        return render_template('error.html', **locals()), code

    for error_code in [400, 403, 404, 503, 509]:
        @app.errorhandler(error_code)
        def page_not_found(error):
            try:
                code = int(str(error)[:3])
            except:
                code = 503
            return page_error(error, code)

    return app
