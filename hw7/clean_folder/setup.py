from setuptools import setup, find_namespace_packages

setup(
    name='clean',
    version='1',
    description='Folder parsing script',
    url='http://github.com/dummy_user/useful',
    author='Serhii Piatenko',
    author_email='sergiy.pyatenko@gmail.com',
    license='MIT',
    entry_points={'console_scripts': [
        'clean-folder = useful.some_code:clean']}
)
