from setuptools import setup, find_packages

setup(
    name='tetris_gym',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'gymnasium',
        'numpy',
        'keyboard',
    ],
    author='Jules',
    author_email='',
    description='A Tetris environment for Gymnasium',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/your_repository', # Replace with your URL
)
