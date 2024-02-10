from setuptools import find_packages, setup

setup(
    name="etl",
    # packages=find_packages(exclude=["etl_tests"]),
    packages=find_packages(),
    install_requires=[
        "dagster",
        "python-dotenv",
        # "pandas",
        "requests",
        "boto3"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "coverage"]},
)
