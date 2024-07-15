#!/usr/bin/python3
"""
This module contains the function do_pack that generates a .tgz archive
from the contents of the web_static folder (fabric script).
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    The function creates a 'versions' directory if it does not exist, 
    generates a timestamped archive of the web_static folder, 
    and returns the path to the created archive.

    Returns:
    str: The path to the created .tgz archive.
    """
    # Create versions directory if it does not exist
    local("mkdir -p versions")

    # Generate a timestamp string for the archive name
    t = datetime.now()
    t_str = t.strftime('%Y%m%d%H%M%S')

    # Create the .tgz archive
    archive_path = f'versions/web_static_{t_str}.tgz'
    local(f'tar -cvzf {archive_path} web_static')

    # Get the size of the created archive
    archive_size = os.path.getsize(archive_path)

    # Print details about the created archive
    print(f'web_static packed: {archive_path} -> {archive_size}Bytes')

    # Return the path to the created archive
    return archive_path
