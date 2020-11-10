import os
from subprocess import check_output


def get_release_sha():
    path = package_dir = os.path.dirname(__file__)
    if not os.path.exists(os.path.join(path, ".git")):
        return None
    try:
        revision = check_output(["git", "rev-parse", "HEAD"], cwd=path, env=os.environ)
    except Exception:
        # binary didn't exist, wasn't on path, etc
        return None
    return revision.strip()

def get_plan_label(event):
    label = None
    for tag in event["tags"]:
        key, value = tag
        if key == "plan":
            label = value
            break

    return label