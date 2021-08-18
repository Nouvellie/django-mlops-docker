# PYTHON LIBS
- Install python 3.9

## Install virtualenv

```sh
$ pip3 install virtualenv
```

## Create environ

```sh
$ virtualenv djangomlopsdocker
```

## Open environ

```sh
$ source djangotflite/bin/activate
```

## Install libs (auto)

```
$ pip install -r requirement.txt
```

## Install libs (manual)

```
$ pip install django==3.2.6 djangorestframework==3.12.4 django-environ-2==2.1.0 tensorflow==2.6.0 mysqlclient==2.0.3 pillow==8.3.1 matplotlib==3.4.3 jupyterlab==3.1.7 ipykernel==6.2.0 graphviz==0.17 pydot==1.4.2 beautifulsoup4==4.9.3 lxml==4.6.3 drf_yasg==1.20.0 pyyaml==5.4.1 gunicorn==20.1.0
```

## Tensorflow GPU

```
$ pip install tensorflow-gpu==2.6.0
```

## Add environ to jupyter kernell

```sh
$ python -m ipykernel install --user --name=djangomlopsdocker
```

## Remove environ from jupyter kernell
```sh
$ jupyter kernelspec uninstall djangotflite
```

## Graphviz
#### Ubuntu:

```sh
$ sudo apt install graphviz
```

#### MacOS:

```sh
$ brew install graphviz
```