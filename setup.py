from setuptools import setup, find_packages

VERSION = '1.0.0'
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
    packages=find_packages(),
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
        'cloupy': [
            'scraping/*',
            'diagrams/*',
            'test/test_integration/*',
            'test/test_unit/*'
        ],
                  },
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Framework :: Matplotlib',
        'Topic :: Scientific/Engineering :: Atmospheric Science'
    ]
)