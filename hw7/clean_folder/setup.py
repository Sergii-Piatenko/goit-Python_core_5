from setuptools import setup, find_namespace_packages

setup(
    name='clean',
    version='1',
    description='Folder parsing script',
    url='https://github.com/Sergii-Piatenko/goit-Python_core_5/tree/main/hw7/clean_folder',
    author='Serhii Piatenko',
    author_email='sergiy.pyatenko@gmail.com',
    license='MIT',
    entry_points={'console_scripts': [
        'clean-folder = useful.some_code:clean']}
)
