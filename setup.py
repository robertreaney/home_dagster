from setuptools import find_packages, setup

setup(
    name="etl",
    packages=find_packages(exclude=["etl_tests"]),
    install_requires=[
        "dagster",
        "python-dotenv",
        "pandas",
        "requests",
        "twilio"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "coverage"]},
)
