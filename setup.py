from setuptools import setup, find_packages

setup(
    name = "django-mongosearch",
    version = "1.0",
    url = 'http://github.com/jacobian/django-mongosearch',
    license = 'BSD',
    description = "A short URL handler for Django apps.",
    author = 'Gaurav Kapoor',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
