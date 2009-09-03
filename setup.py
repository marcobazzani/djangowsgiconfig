from setuptools import setup, find_packages

setup(
    name = 'djangowsgiconfig',
    version = '0.1.1',
    description = 'a buildout recipe to create apache vhost config based on djangorecipe settings',
    author='Marco Bazzani',
    author_email='pypi@marcobazzani.name',
    license = 'MIT',
    entry_points = {'zc.buildout' : ['default = djangowsgiconfig:DjangoWsgiConfig']},
    install_requires=[
            'djangorecipe',
          ],
    package_dir = {'':'.'},
    packages = find_packages('.'),
    )
