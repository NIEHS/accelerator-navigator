from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    install_requires = [line.strip() for line in f if line.strip()]

setup(
    name="accelerator_navigator",
    version="0.1.0",
    description="accelerator navigator support",
    author="",
    author_email="",
    url="https://github.com/NIEHS/accelerator-navigator",
    packages=find_packages(),
    install_requires=[open("requirements.txt").read()],
    license="BSD 3-Clause",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9"
)
