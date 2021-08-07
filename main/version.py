__author__      =     "Rocuant Roberto"
__created__     =     "08/07/2021" # MM/DD/YYYY
__credits__     =     None
__copyright__   =     None
__email__       =     "roberto.rocuantv@gmail.com"
__maintainer__  =     "Rocuant Roberto"
__prod__        =     None
__structure__   =     "str(version) - str(date) - list(info) - list(problems) - none-bool(fixed) - str(commit) - none-bool(prod)"
__version__     =     "0.0.1"
__logs__        =  {
    'version':      "0.0.1",
    'date':         "08/07/2021",
    'info':         ["Base project created."],
    'problems':     ["",],
    'fixed':        None,
    'commit':       "",
    "prod":         None,
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