from setuptools import setup, find_packages

setup(
    name='jira-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'requests>=2.26.0',
    ],
    entry_points={
        'console_scripts': [
            'jira-cli=jira_cli.cli:cli',
        ],
    },
    python_requires='>=3.7',
)
