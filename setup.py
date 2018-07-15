from setuptools import setup
setup(
    name = "gift_exchange",
    version = "0.1.0",
    packages = ["gift_exchange"],
    test_suite="tests",
    entry_points = {
        "console_scripts": [
            "gift_exchange = gift_exchange.__main__:main"
        ]
    })