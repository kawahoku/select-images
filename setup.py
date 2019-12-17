from setuptools import setup

setup(
    name='SelectImages',
    version='0.1',
    description='Awesome library',
    author='kawasaki',
    author_email='kawahokuhoku@gmail.com',
    keywords='sample setuptools development',
    data_files=["pyapp/config.json"],
    packages=[
        "pyscript",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
