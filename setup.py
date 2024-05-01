import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pexels-api",
    version="1.0.0",
    author="Attila Kis",
    author_email="attilakis33@gmail.com",
    description="Pexels API implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atosz33/pexels-api",
    keywords='pexels api images photos',
    install_requires=['requests', 'pydantic'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
