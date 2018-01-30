from setuptools import setup, find_packages


setup(name='ncdoublescrape',
      version='0.0.1',
      packages=find_packages(),
      author='Hannah Cushman',
      license='BSD',
      url='https://github.com/hancush/march_sadness/ncdoublescrape',
      description='scrape stuff for college bball',
      entry_points='''[console_scripts]
ncds = ncdoublescrape.__main__:main''',
      install_requires=[
          'requests',
          'lxml',
      ]
)