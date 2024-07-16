#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
env.use_ssh_config = True
from os.path import exists

env.hosts = ['54.226.6.30', '52.91.160.169']

def do_deploy(archive_path):
    """Distributes an archive to the web servers."""
    if not exists(archive_path):
        print(f"Archive {archive_path} does not exist.")
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"

        print(f"Uploading {archive_path} to /tmp/")
        put(archive_path, '/tmp/')
        print(f"Creating directory {path}{no_ext}/")
        run(f'mkdir -p {path}{no_ext}/')
        print(f"Extracting /tmp/{file_n} to {path}{no_ext}/")
        run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')
        run(f'rm /tmp/{file_n}')
        print(f"Moving files from {path}{no_ext}/web_static/* to {path}{no_ext}/")
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        print("Removing current symlink")
        run('rm -rf /data/web_static/current')
        print(f"Creating new symlink /data/web_static/current -> {path}{no_ext}/")
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')

        print("Deployment successful.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
