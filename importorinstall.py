import pip
def package(name):
    try:
        __import__(name)
    except ImportError:
        pip.main(['install', name])