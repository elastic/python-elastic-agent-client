from setuptools import setup, find_packages
setup(
    name='es_agent_client',
    version='0.0.1',
    description='A python implementation of an Elastic Agent Client',
    url='https://github.com/elastic/python-elastic-agent-client',
    author='Sean Story',
    author_email='sean.story@elastic.co',
    license='Elastic v2',
    packages=find_packages(),
    install_requires=[
        'grpcio>=1.62',
        'protobuf>=4.25',
    ],
)