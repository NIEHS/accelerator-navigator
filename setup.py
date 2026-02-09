from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="accelerator_navigator",
    version="0.1.0",
    description="accelerator navigator support",
    url="https://github.com/NIEHS/accelerator-navigator",
    packages=find_packages(),
    install_requires=requirements,
    license="BSD 3-Clause",
    python_requires=">=3.9",
)
