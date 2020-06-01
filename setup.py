from setuptools import setup, find_packages


setup(
    name='Advanced System Design',
    version='0.1.0',
    author='Zeevi Iosub',
    description='Advanced System Design project - "man-machine inerface".',
    packages=find_packages(),
    install_requires = ['virtualenv', 'click', 'flask', 'redis', 'pika', 'pillow', 'google', 'protobuf', 'matplotlib']
    tests_require=['pytest', 'pytest-cov'],
)
