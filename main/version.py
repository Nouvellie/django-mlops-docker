__author__      =     "Rocuant Roberto"
__created__     =     "08/07/2021" # MM/DD/YYYY
__credits__     =     "Ávila Jorge (mlops app)"
__copyright__   =     None
__email__       =     "roberto.rocuantv@gmail.com"
__maintainer__  =     "Rocuant Roberto"
__prod__        =     None
__structure__   =     "str(version) - str(date) - list(info) - list(problems) - none-bool(fixed) - str(commit) - none-bool(prod)"
__version__     =     "0.1.1"
__logs__        =  {
    'version':      "0.1.1",
    'date':         "08/08/2021",
    'info':         ["Output decoder not ready yet. OK", "Argmax and threshold adapted.", "FashionMnist TFLite View ready.", "Model updated.", "Url and APIView name changed."],
    'problems':     ["",],
    'fixed':        None,
    'commit':       "",
    "prod":         None,
}

# __logs__        =  {
#     'version':      "0.1.0",
#     'date':         "08/08/2021",
#     'info':         ["Pipeline, preprocessing, model loader, file loader and model input ready for fashion mnist and generics models.", "Custom typing for some values.", "PEP8.", "The code was cleaned up.", "Example images added.",],
#     'problems':     ["Output decoder not ready yet.*", "HDF5 not ready yet.", "DVC not implemented yet.", "Fix pipeline from_json."],
#     'fixed':        False,
#     'commit':       "",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.0.3",
#     'date':         "08/07/2021",
#     'info':         ["Pipeline py added.", "Pre processing py added.", "Media FashionMnist folder updated.", "Complete Pipeline class."],
#     'problems':     ["",],
#     'fixed':        None,
#     'commit':       "",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.0.2",
#     'date':         "08/07/2021",
#     'info':         ["Jupyter notebook for Fashion Mnist example.", "Converter from model to TFLite.", "Predict with both methods."],
#     'problems':     ["",],
#     'fixed':        None,
#     'commit':       "",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.0.1",
#     'date':         "08/07/2021",
#     'info':         ["Base project created."],
#     'problems':     ["",],
#     'fixed':        None,
#     'commit':       "610d7c2",
#     "prod":         None,
# }


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