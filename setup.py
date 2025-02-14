from setuptools import setup, find_packages

setup(
    name="blick",
    version="0.1.0",
    packages=find_packages(where="src/blick", include=["blick.*"]),
    # look in 'src' and include packages in 'blick' and its sub-packages
    package_dir={"": "src"},
)