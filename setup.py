from setuptools import find_packages, setup

setup(
    name='koob',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    author='norangebit',
    description='A CLI utility to extract information from Kobo db',
    entry_points={'console_scripts': ['koob = koob.main:main']}
)
