"""
setup for bookworms
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    
    name='bookworms',  # Required
    version='0.1',  # Required
    description='Social Network based Book Recommendation System',  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.gatech.edu/hlu82/bookworms',  # Optional
    author='GTCSE6242SP18Group02',  # Optional
    author_email='kchu41@gatech.edu',  # Optional

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
    ],

    keywords='book recommendation',  # Optional
    
    
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
    
    install_requires=['flask', 'numpy'],  # Optional
    
    package_data={  # Optional
        'bookworms': ['sample_data/*'],
    },
    include_package_data=True,
    
)
