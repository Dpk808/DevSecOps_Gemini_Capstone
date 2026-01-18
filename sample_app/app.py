import subprocess

def insecure_command(user_input):
    subprocess.call(user_input, shell=True)
