from setuptools import setup, find_packages

setup(
    name="mle-training1",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "scikit-learn"
        # Add any other dependencies here
    ],
    python_requires=">=3.6",
    author="Raushan Kumar",
    author_email="raushan.kumar@tigeranalytics.com",
    description="A library for data manipulation and modeling",
    url="https://github.com/raushan.kumar/mle-training1",
)
