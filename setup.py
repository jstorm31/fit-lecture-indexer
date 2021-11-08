import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='fit-lecture-indexer',
      version='0.2.0',
      description='A tool for extracting timestamps of slide transitions from a video lecture',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/jstorm31/fit-lecture-indexer',
      author='Jiří Zdvomka',
      author_email='zdvomka.j@gmail.com',
      license='MIT',
      packages=find_packages(exclude=("tests",)),
      include_package_data=True,
      install_requires=['tqdm', 'imagehash', 'strsimpy', 'opencv-python-headless', 'pytesseract'],
      classifiers=[
          'Programming Language :: Python :: 3.8',
      ])
