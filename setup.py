from setuptools import setup
setup(
    name='CS',
    version='1.0',
    install_requires=['setuptools', 'GitPython', 'termcolor', 'requests'],
    scripts=['scripts/cs'],
    packages={'cs', 'cs.plugins'},
    package_dir={'cs': 'cs'}
)