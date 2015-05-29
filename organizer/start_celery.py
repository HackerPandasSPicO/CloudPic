if __name__ == '__main__':
    import subprocess
    command = "celery -A organizer worker -l info"
    subprocess.call(command.split(' '))
