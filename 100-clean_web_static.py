#!/usr/bin/python3
"""
Deletes out-of-date archives
fab -f 100-clean_web_static.py do_clean:number=2 -i ssh-key -u ubuntu > /dev/null 2>&1
"""

import os
from fabric.api import *

env.hosts = ['100.27.2.72', '54.158.79.158']

def do_clean(number=0):
    """Delete out-of-date archives.
    Args:
        number (int): The number of archives to keep.
    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = 1 if int(number) == 0 else int(number)

    # Local cleanup
    local_archives = sorted(os.listdir("versions"))
    archives_to_delete = local_archives[:-number]
    
    with lcd("versions"):
        for archive in archives_to_delete:
            local("rm ./{}".format(archive))
    
    # Remote cleanup
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        archives_to_delete = remote_archives[:-number]
        
        for archive in archives_to_delete:
            run("rm -rf ./{}".format(archive))

