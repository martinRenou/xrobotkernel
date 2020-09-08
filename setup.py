from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='xrobotkernel',
    version='0.1',
    packages=['xrobotkernel'],
    description='RobotFramework kernel for Jupyter',
    long_description=readme,
    author='QuantStack',
    url='https://github.com/martinRenou/xrobotkernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
)
