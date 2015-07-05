from distutils.core import setup

setup(
    name='nfogen',
    version='0.0.1',
    author='Boris Babic',
    author_email='boris.ivan.babic@gmail.com',
    packages=['nfogen'],
    include_package_data=True,
    url='template url',
    entry_points={
            'console_scripts': [
                'nfogen = nmanager:main',
            ],
        },
    install_requires=[
        "tvdb_api",
        ],
    description='Generate tvshow.nfo files for tv shows',
    long_description=open('README.txt').read(),
)
