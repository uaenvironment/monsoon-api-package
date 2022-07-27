from setuptools import setup

setup(
    name='clipack',
    version='0.0.1',
    py_modules=['clipack'],
    install_requires=['Click','Pandas'], 
    entry_points= {'clipack':['clipack = clipack:cli']})