__author__      =     "Rocuant Roberto"
__created__     =     "08/07/2021" # MM/DD/YYYY
__credits__     =     "Ávila Jorge (mlops app)"
__copyright__   =     None
__email__       =     "roberto.rocuantv@gmail.com"
__maintainer__  =     "Rocuant Roberto"
__prod__        =     None
__structure__   =     "str(version) - str(date) - list(info) - list(problems) - none-bool(fixed) - str(commit) - none-bool(prod)"
__version__     =     "0.7.0"
__logs__        =  {
    'version':      "0.7.0",
    'date':         "08/13/2021",
    'info':         ["Catsvsdogs TFLite model ready.", "Pip md updated.", "Postprocessing with binary results adapted. (argmax)", "Postprocessing results adapted for argmax/thresholds. (with/without binary results)", "Gettext _ added.", "Confidence output with math.floor.", "Image seek().", "Image erased after output."],
    'problems':     ["Preprocessing json problems.",],
    'fixed':        False,
    'commit':       "",
    "prod":         None,
}

# __logs__        =  {
#     'version':      "0.6.0",
#     'date':         "08/12/2021",
#     'info':         ["Imdb to imdb sentiment changed.", "Stackoverflow text model added on jupyter.", "Stackover flow TFLite ready.", "Stackoverflow hdf5json maybe ready.", "Pip md updated.", "Stackoverflow API View ready.",],
#     'problems':     ["Text classification model get Vectorized input not str.",],
#     'fixed':        False,
#     'commit':       "9f2a67e",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.5.0",
#     'date':         "08/12/2021",
#     'info':         ["Imdb predict from file ready.", "Model input fix. OK", "Imdb predict with text or file. (txt) OK"],
#     'problems':     ["Raise error if it is not a text file.",],
#     'fixed':        False,
#     'commit':       "5961ed1",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.4.0",
#     'date':         "08/12/2021",
#     'info':         ["Imdb APIView.", "Imdb pre-post adaptation.", "Imdb jupyter not ready yet. OK", "TFLite Imdb ready.", "Imdb jupyter fixed.", "Model input updated.",],
#     'problems':     ["Model input fix*.", "Imdb predict with text or file. (txt)*"],
#     'fixed':        True,
#     'commit':       "4543ca7",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.3.0",
#     'date':         "08/12/2021",
#     'info':         ["Pip requirements added.", "Virtualenv instead conda info.", "Jupyter fix.", "Ipykernel for new environ.", "Imdb notebook fix.", "Imdb model adapted. (tflite)", "Prediction OK on Imdb model.",],
#     'problems':     ["",],
#     'fixed':        None,
#     'commit':       "8556750",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.2.0",
#     'date':         "08/08/2021",
#     'info':         ["HDF5JSON not ready yet. OK", "TFLite threshold output fixed (views.py).", "Jupyter example fixed.", "Imdb jupyter added.", "Jupyter folder on media path now.",],
#     'problems':     ["Imdb jupyter not ready yet.*",],
#     'fixed':        True,
#     'commit':       "22f8f86",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.1.1",
#     'date':         "08/08/2021",
#     'info':         ["Output decoder not ready yet. OK", "Argmax and threshold adapted.", "FashionMnist TFLite View ready.", "Model updated.", "Url and APIView name changed.", "Commit added (fixed).",],
#     'problems':     ["",],
#     'fixed':        None,
#     'commit':       "959c309",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.1.0",
#     'date':         "08/08/2021",
#     'info':         ["Pipeline, preprocessing, model loader, file loader and model input ready for fashion mnist and generics models.", "Custom typing for some values.", "PEP8.", "The code was cleaned up.", "Example images added.",],
#     'problems':     ["Output decoder not ready yet.*", "HDF5JSON not ready yet.*", "DVC not implemented yet.", "Fix pipeline from_json."],
#     'fixed':        False,
#     'commit':       "ea35174",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.0.3",
#     'date':         "08/07/2021",
#     'info':         ["Pipeline py added.", "Pre processing py added.", "Media FashionMnist folder updated.", "Complete Pipeline class."],
#     'problems':     ["",],
#     'fixed':        None,
#     'commit':       "0bb56be",
#     "prod":         None,
# }

# __logs__        =  {
#     'version':      "0.0.2",
#     'date':         "08/07/2021",
#     'info':         ["Jupyter notebook for Fashion Mnist example.", "Converter from model to TFLite.", "Predict with both methods."],
#     'problems':     ["",],
#     'fixed':        None,
#     'commit':       "ec12892",
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