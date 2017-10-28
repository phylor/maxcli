from setuptools import setup

setup(
    name='MaxSmart CLI',
    version='1.0',
    py_modules=['maxcli'],
    install_requires=[
        'Click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        maxcli=maxcli:cli
    ''',
)
