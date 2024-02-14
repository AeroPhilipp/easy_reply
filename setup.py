# setup.py
from setuptools import setup
from setuptools import find_packages

# list dependencies from file
with open('requirements_docker.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setup(name='movie_recom',
      description="package description",
      packages=find_packages(), # NEW: find packages automatically
      install_requires=requirements) # NEW
