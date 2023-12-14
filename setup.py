import os

from setuptools import find_packages, setup

dir_path = os.path.dirname(__file__)

readme_file = 'README.md'
readme_path = os.path.join(dir_path, readme_file)
with open(readme_path, 'r') as file:
    long_description = file.read()

requirements_file = 'requirements.txt'
requirements_path = os.path.join(dir_path, requirements_file)
with open(requirements_path, 'r') as file:
    requirements = [line.removesuffix('\n') for line in file.readlines()]


setup(
    name='desmoscurves',
    version='0.0.1',
    description='Bezier curve editor and conversion to Desmos graph',
    python_requires='>=3.10',
    packages=find_packages(),
    entry_points={'console_scripts': ['desmoscurves = desmoscurves.gui:gui']},
    classifiers=[],
    install_requires=requirements,
    long_description=long_description,
)
