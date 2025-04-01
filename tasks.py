from invoke import task

@task
def start(c):
    c.run("python3 src/index.py", pty=True)