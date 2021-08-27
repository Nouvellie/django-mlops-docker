__author__      =     "Rocuant Roberto"
__created__     =     "08/07/2021" # MM/DD/YYYY
__credits__     =     "Ávila Jorge (mlops app), Truly Cryce (authentication app)"
__copyright__   =     None
__email__       =     "roberto.rocuantv@gmail.com"
__maintainer__  =     "Rocuant Roberto"
__prod__        =     None
__structure__   =     "str(version) - str(date) - list(info) - bool(todo) - str(commit) - none-bool(prod)"
__version__     =     "0.25.0"
__logs__        =  {
    'version':      "0.25.0",
    'date':         "08/27/2021",
    'info':         [
        "Main readme updated.",
    ],
    'todo':         True,
    'commit':       "",
    "prod":         None,
}

TODO_TASKS = { # TASK-STATUS
    "DVC not implemented yet.": False,
    "Fix pipeline from_json.": False,
    "Text classification model. (get Vectorized input not str).": False,
    "CheckpointModelLoader not created yet.": False,
    "DEBUG for emails url.": False,
    "SignIn swagger redirect.": False,
    "Html/css for emails.": False,
}

full_info = {
    '__author__': __author__,
    '__created__': __created__,
    '__credits__': __credits__,
    '__copyright__': __copyright__,
    '__email__': __email__,
    '__logs__': __logs__,
    '__maintainer__': __maintainer__,
    '__prod__': __prod__,
    '__version__': __version__, 
}

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

info = dotdict(dict=full_info)['dict']