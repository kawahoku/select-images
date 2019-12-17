from setuptools import setup

setup(
    name='SelectImages',
    version='0.1',
    description='Awesome library',
    author='kawasaki',
    author_email='kawahokuhoku@gmail.com',
    keywords='sample setuptools development',
    url="https://github.com/kawahoku/select-images",
    data_files=[("pyapp", ["pyapp/config.json"])],
    packages=[
        "SelectImagesGUI",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
