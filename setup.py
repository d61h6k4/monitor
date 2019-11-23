from setuptools import setup, find_packages

setup(
    name='monitor',
    version='0.0.1',
    description='',
    author='Danil Petrov',
    author_email='ddbihbka@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.7',
    ],
    keywords='monitoring',
    packages=find_packages(include=['monitor']),
    entry_points={
        'console_scripts': [
            'monitor=bin:main'
        ]
    }
)
