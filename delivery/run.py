__author__ = 'Dewep'

from flask import render_template, Flask, request, Response, abort
import os
import subprocess
from docker import Client

app = Flask(__name__)
root_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


SERVERS = [
    {
        "type": "python",
        "name": "python1",
        "ip": "127.0.0.1",
        "port": 5001
    },
    {
        "type": "python",
        "name": "python2",
        "ip": "127.0.0.1",
        "port": 5002
    }
]


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
            release["name"] = repo + ":" + tag
            release["created"] = time.ctime(image["Created"])
            release["size"] = "%.1f MB" % (image["VirtualSize"] / 1000000.0)
            release["is_used"] = False
            release["state"] = ""
            releases.append(release)
    for server in SERVERS:
        containers.append({
            "type": server["type"],
            "name": server["name"],
            "ip": server["ip"],
            "port": server["port"],
            "haproxy_weight": "?",
            "haproxy_state": "?",
            "container_id": "-",
            "container_image": "-",
            "container_status": "-",
            "has_image": False,
            "state": ""
        })
    for instance in c.containers():
        for container in containers:
            is_server = False
            for port in instance["Ports"]:
                if "PublicPort" in port and port["PublicPort"] == container["port"]:
                    is_server = True
            if is_server:
                for release in releases:
                    if instance["Image"] == release["name"]:
                        release["is_used"] = True
                container["container_id"] = instance["Id"][:12]
                container["container_image"] = instance["Image"]
                container["container_status"] = instance["Status"]
                container["has_image"] = True
    # State
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


@app.route('/execute/container/<server_name>/new/<image>/<api_key>')
def execute_container_new(server_name, image, api_key):
    instance_server = None
    for server in SERVERS:
        if server["name"] == server_name:
            instance_server = server
    if not instance_server:
        abort(404, "Server not found")
    if request.headers.get('accept') == 'text/event-stream':
        def start():
            c = Client()
            try:
                yield "data: Create container...\n\n"
                container = c.create_container(image=image, name="senpai-"+instance_server["name"], ports=[5000],
                                               environment={"API_KEY": api_key})
                yield "data: Start container...\n\n"
                c.start(container=container.get('Id'), port_bindings={5000: ('127.0.0.1', instance_server["port"])},
                        links=[("senpai-redis", "redis")])
                yield "data: RETURN_VALUE=0\n\n"
            except Exception as e:
                yield "data: Error: %s\n\n" % str(e)
                yield "data: RETURN_VALUE=1\n\n"
        return Response(start(), content_type='text/event-stream')
    return render_template('execute.html', path=request.path, command="docker start "+server_name+":"+image)


@app.route('/execute/container/<container_id>/remove')
def execute_container_remove(container_id):
    if request.headers.get('accept') == 'text/event-stream':
        def remove():
            c = Client()
            try:
                yield "data: Remove container...\n\n"
                c.remove_container(container=container_id, force=True)
                yield "data: RETURN_VALUE=0\n\n"
            except Exception as e:
                yield "data: Error: %s\n\n" % str(e)
                yield "data: RETURN_VALUE=1\n\n"
        return Response(remove(), content_type='text/event-stream')
    return render_template('execute.html', path=request.path, command="docker rm "+container_id)


if __name__ == '__main__':
    app.run(debug=True)
