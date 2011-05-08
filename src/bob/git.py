import os
import sys
import shutil
import dulwich.repo
import dulwich.client

def clone(local, remote):
    
    client, host_path = dulwich.client.get_transport_and_path(remote)

    if not os.path.exists(local):
        os.makedirs(local)

    r = dulwich.repo.Repo.init(local)

    remote_refs = client.fetch(host_path, r,
        determine_wants=r.object_store.determine_wants_all,
        progress=sys.stdout.write)

    r["HEAD"] = remote_refs["HEAD"]


def pull(local, remote):
    
    cwd = os.getcwd()
    os.chdir(local)
    os.system('git pull {0}'.format(remote))
    os.chdir(cwd)


def checkout(local, branch):
    
    cwd = os.getcwd()
    os.chdir(local)
    os.system('git checkout {0}'.format(branch))
    os.chdir(cwd)
