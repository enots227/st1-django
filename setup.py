  
from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='st1-django',
    version='0.0.1',
    description='Common Django web framework functions shared between apps.',
    author='Stone Sommers',
    author_email='enots227@gmail.com',
    include_package_data=True,
    packages=find_packages(
        exclude=['tests.*', 'tests']
    ),
    install_requires=[
        'Django>=4.0.3',
        'djangorestframework>=3.12.4',
        'st1-logging>=0.0.1',
        'st1-voluptuous-serializable>=0.0.1',
    ]
)

