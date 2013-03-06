from fabric.api import local, task, run

@task
def deploy():
    push_to_heroku()

@task
def push_to_heroku():
    local('git push heroku master')