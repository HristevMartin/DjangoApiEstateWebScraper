import os

def get_env_variable(var_name, default=None):
    return os.environ.get(var_name, default)