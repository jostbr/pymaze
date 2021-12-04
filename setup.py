from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="pymaze",
    description="A maze generator, solver and visualizer for Python.",
    license="MIT",
    packages=find_packages(include="pymaze"),
    install_requires=requirements,
)
