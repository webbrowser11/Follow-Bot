import scratchattach as attach
import time
import os

def handler(request, response):
    print("Creating session")

    username = os.environ.get("SCRATCH_USERNAME")
    password = os.environ.get("SCRATCH_PASSWORD")

    if not username or not password:
        return response.status(500).send("Missing credentials")

    session = attach.login(username, password)
    print("Connecting studio")
    studio = session.connect_studio("35292763")

    off = 14640
    index = 10

    for _ in range(2):
        print(f"Fetching projects with offset of {off}")
        projects = studio.projects(limit=5, offset=off)
        for project_info in projects:
            index += 1
            project = session.connect_project(vars(project_info)['id'])
            project.author().follow()
            print(f"{index}: Followed author {project.author()} from project {project.title}")
            time.sleep(1)
        off += 20
        time.sleep(1)

    return response.json({"status": "done", "followed": index})
