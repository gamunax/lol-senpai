__author__ = 'Dewep'

from flask import render_template, Flask, request, Response
import os
import subprocess

app = Flask(__name__)
root_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def args_to_command(args):
    from shlex import quote
    return " ".join([quote(arg) for arg in args])


def execute_command(args):
    p = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        yield "data: %s\n\n" % line
    yield "data: RETURN_VALUE=%d\n\n" % p.wait()


def get_latest_git_revision():
    out = subprocess.check_output(['git', "-C", root_directory, 'rev-parse', '--short', 'HEAD'])
    return out.decode("utf-8")[:7]


@app.route('/')
def root():
    latest_git_revision = get_latest_git_revision()
    releases = list()
    containers = list()
    is_used = False  # si il y a des containers qui
    state = "danger"
    if "27c3a0c" == latest_git_revision:
        state = "success"
    elif is_used:
        state = "warning"
    releases.append({
        "image_id": "64698ee0dfe3",
        "repository": "senpai",
        "tag": "27c3a0c" + (" (latest)" if "27c3a0c" == latest_git_revision else ""),
        "created": "2 hours ago",
        "size": "786.6 MB",
        "is_used": is_used,
        "state": state
    })
    state = "success"
    has_image = False
    containers.append({
        "name": "python1",
        "haproxy_weight": 0,
        "haproxy_state": "Disabled",
        "container_id": "-",
        "container_image": "-",
        "container_status": "-",
        "has_image": has_image,
        "state": state
    })
    return render_template('index.html', **locals())


@app.route('/execute/git/fetch')
def execute_git_fetch():
    args = ["git", "-C", root_directory, "fetch"]
    if request.headers.get('accept') == 'text/event-stream':
        return Response(execute_command(args), content_type='text/event-stream')
    return render_template('execute.html', path=request.path, command=args_to_command(args))


if __name__ == '__main__':
    app.run(debug=True)
