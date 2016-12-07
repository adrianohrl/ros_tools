import sys

from setuptools import find_packages, setup

# Setup installation dependencies
install_requires = [
    'osrf-pycommon > 0.1.1',
    'catkin-pkg > 0.2.9',
    'rospkg > 1.0.0',
    'setuptools',
]
if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
    install_requires.append('argparse')

setup(
    name='rosorm',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'docs']),
    # package_data={'rosorm': []},
    # data_files=get_data_files(prefix),
    install_requires=install_requires,
    author='Adriano H. R. Leite, Ricardo E. Julio, UNIFEI Expertinos Team',
    author_email='adrianohrl@unifei.edu.br, ricardoej@gmail.com, expertinos.unifei@gmail.com',
    maintainer='Adriano H. R. Leite, Ricardo E. Julio, UNIFEI Expertinos Team',
    maintainer_email='adrianohrl@unifei.edu.br, ricardoej@gmail.com, expertinos.unifei@gmail.com',
    url='https://github.com/Expertinos',
    keywords=['rosorm', 'ROS', 'database', 'ORM'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    description="Command line tools for working with ...",
    long_description="Provides command line tools for working with ...",
    license='Apache 2.0',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'rosorm = rosorm.commands.rosorm:main',
        ],
        'rosorm.commands.rosorm.verbs': [
            'build = rosorm.verbs.rosorm_build:entry_point_data',
            'convert = rosorm.verbs.rosorm_convert:entry_point_data',
            'generate = rosorm.verbs.rosorm_generate:entry_point_data',
        ],
    },
)
