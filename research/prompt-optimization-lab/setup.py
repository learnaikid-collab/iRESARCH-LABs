"""
Setup script for the Advanced Prompt Optimization System.
"""

from setuptools import setup, find_packages
import os


# Read README for long description
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


setup(
    name='prompt-optimization-lab',
    version='0.1.0',
    author='iRESARCH-LABs',
    author_email='contact@iresearch-labs.org',
    description='Advanced Prompt Optimization System for LLMs',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/learnaikid-collab/iRESARCH-LABs',
    project_urls={
        'Documentation': 'https://github.com/learnaikid-collab/iRESARCH-LABs/tree/main/research/prompt-optimization-lab/docs',
        'Source': 'https://github.com/learnaikid-collab/iRESARCH-LABs',
        'Tracker': 'https://github.com/learnaikid-collab/iRESARCH-LABs/issues',
    },
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.4.0',
            'isort>=5.12.0',
        ],
        'docs': [
            'sphinx>=7.0.0',
            'sphinx-rtd-theme>=1.3.0',
        ],
        'all': [
            'wandb>=0.15.0',
            'chromadb>=0.4.0',
            'pinecone-client>=2.2.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'prompt-optimize=src.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.yaml', '*.json', '*.txt'],
    },
    zip_safe=False,
    keywords=[
        'prompt engineering',
        'prompt optimization',
        'llm',
        'large language models',
        'reinforcement learning',
        'evolutionary algorithms',
        'chain-of-thought',
        'rag',
        'retrieval augmented generation',
    ],
)
