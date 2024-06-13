from setuptools import setup, find_packages

setup(
    name='typerush',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    dependency_links=[
        'git+https://github.com/GoncaloBranquinho/typerRush/#egg=typing_game-1.0',
    ],
    install_requires=[
        'curses-menu', 
    ],
    package_data={ '': ['sentences.json']},
    entry_points={
        'console_scripts': [
            'typerush = typing_1:main',  
        ],
    },
)
