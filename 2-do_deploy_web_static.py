#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers.
"""

from fabric.api import put, run, env
from os.path import exists

env.use_ssh_config = True
env.hosts = ['54.226.6.30', '52.91.160.169']


def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{no_ext}/')
        run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')
        run(f'rm /tmp/{file_n}')
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')

        return True
    except Exception:
        return False
