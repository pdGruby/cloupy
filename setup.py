import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.0'
DESCRIPTION = 'The package allows to download, process and visualize climatological data from reliable sources'
README = (HERE / 'README.md').read_text()

setup(
    name='cloupy',
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    author='Kamil Grala',
    author_email='kamil.grala32466@gmail.com',
    url='https://github.com/pdGruby/cloupy',
    license='MIT',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'pandas==1.1.4',
        'matplotlib==3.3.2',
        'requests==2.24.0',
        'beautifulsoup4==4.9.3',
        'numpy==1.19.4'
    ],
    tests_require=[
        'pytest==6.2.5',
        'mock==4.0.3'
    ],
    package_data={
        'src': [
            'scraping/imgw_coordinates.csv',
            'scraping/wmo_ids_and_coords.csv'
        ]
    }
)
