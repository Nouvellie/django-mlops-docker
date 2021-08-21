__author__      =     "Rocuant Roberto"
__created__     =     "08/07/2021" # MM/DD/YYYY
__credits__     =     "Ávila Jorge (mlops app)"
__copyright__   =     None
__email__       =     "roberto.rocuantv@gmail.com"
__maintainer__  =     "Rocuant Roberto"
__prod__        =     None
__structure__   =     "str(version) - str(date) - list(info) - bool(todo) - str(commit) - none-bool(prod)"
__version__     =     "0.19.0"
__logs__        =  {
    'version':      "0.19.0",
    'date':         "08/21/2021",
    'info':         [
        'New versioning info struct.',
        '',
    ],
    'todo':         True,
    'commit':       "",
    "prod":         None,
}

TODO_TASKS = { # TASK-STATUS-VERSION
    'DVC not implemented yet.': False,
    'Fix pipeline from_json.': False,
    'Raise error if it is not a text file.': False,
    'Text classification model get Vectorized input. (not str).': False,
    'CheckpointModelLoader not created yet.': False,
    'DEBUG for emails url.': False,
    'ML models muted.': False,
    'Html/css for emails.': False,
    'Mlops input serializer.': False, 
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