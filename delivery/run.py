__author__ = 'Dewep'

from flask import render_template, Flask, request, Response, abort
import os
import subprocess
from docker import Client

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
    import time
    latest_git_revision = get_latest_git_revision()
    c = Client()
    releases = list()
    containers = list()
    for image in c.images():
        repo = None
        tag = None
        for repo_tag in image["RepoTags"]:
            _repo, _tag = repo_tag.split(":")
            if _repo == "senpai" and _tag != "latest":
                repo = _repo
                tag = _tag
        if repo and tag:
            release = dict()
            release["image_id"] = image["Id"][:12]
            release["repository"] = repo
            release["tag"] = tag + (" (latest)" if tag == latest_git_revision else "")
            release["created"] = time.ctime(image["Created"])
            release["size"] = "%.1f MB" % (image["VirtualSize"] / 1000000.0)
            release["is_used"] = True  # TODO
            release["state"] = "success"  # TODO
            releases.append(release)
    # TODO: containers
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


@app.route('/execute/release/new/<revision>')
def execute_release_new(revision):
    args = ["git", "-C", root_directory, "checkout", revision]
    p = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return_code = int(str(p.wait()))
    if return_code:
        abort(404, "Revision not found")
    if request.headers.get('accept') == 'text/event-stream':
        def build():
            import json
            c = Client()
            for line in c.build(path=root_directory, rm=True, tag='senpai:'+revision):
                obj = json.loads(line.decode("utf-8"))
                if "stream" in obj:
                    yield "data: %s\n\n" % obj["stream"]
            yield "data: RETURN_VALUE=0\n\n"
        return Response(build(), content_type='text/event-stream')
    return render_template('execute.html', path=request.path, command="docker build senpai:"+revision)


if __name__ == '__main__':
    app.run(debug=True)
