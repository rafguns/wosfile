from setuptools import setup

long_description = open("README.md", encoding="utf-8").read()

setup(
    name="wosfile",
    version="0.5",
    url="http://github.com/rafguns/wosfile",
    license="New BSD License",
    author="Raf Guns",
    tests_require=["pytest", "pytest-cov"],
    author_email="raf.guns@uantwerpen.be",
    description="Handle Web of Science export files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["wosfile"],
    platforms="any",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
)
