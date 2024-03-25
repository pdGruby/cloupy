from setuptools import setup, find_packages

VERSION = '2.0.0'
DESCRIPTION = 'The package allows to download, process and visualize climatological data from reliable sources'
README = open('README.md', 'r', encoding='utf8').read()

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
    packages=['cloupy'],
    install_requires=[
        'pandas>=1.3.3,<=1.3.5',
        'matplotlib>=3.4.3,<=3.5.1',
        'requests>=2.26.0,<=2.27.1',
        'beautifulsoup4>=4.9.3,<=4.10.0',
        'numpy>=1.21.4,<=1.22.1',
        'pyshp==2.1.3',
        'pyproj>=3.2.1,<=3.3.0',
        'scipy>=1.7.2,<=1.7.3',
        'Pillow>=8.4.0,<=9.0.0',
        'cycler==0.11.0'
    ],
    tests_require=[
        'pytest>=6.2.5',
        'mock>=4.0.3'
    ],
    package_data={
        'cloupy': [
            'data_processing/*',
            'maps/*',
            'maps/world/*',
            'scraping/*',
            'diagrams/*',
            'test/test_integration/*',
            'test/test_unit/*',
        ],
                  },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Framework :: Matplotlib',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Visualization'
    ]
)
