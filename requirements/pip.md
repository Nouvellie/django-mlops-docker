# PYTHON LIBS
- Install python 3.9

## Install virtualenv

```sh
$ pip3 install virtualenv
```

## Create environ

```sh
$ virtualenv djangotflite
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
$ pip install django==3.2.6 djangorestframework==3.12.4 django-environ==0.4.5 tensorflow==2.6.0 mysqlclient==2.0.3 pillow==8.3.1 matplotlib==3.4.2 jupyterlab==3.1.4 ipykernel==6.0.3 graphviz==0.17 pydot==1.4.2
```

## Tensorflow GPU

```
$ pip install tensorflow-gpu==2.6.0
```

## Add environ to jupyter kernell

```sh
$ python -m ipykernel install --user --name=djangotflite
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