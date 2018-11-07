from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='pNarrative',
      version='0.1',
      description='A python module to estimate the narrative arcs in literature',
      url='',
      author='Arian Barakat',
      long_description=long_description,
      author_email='arianbarakat@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_dir={'pNarrative': 'pNarrative'},
      package_data={'pNarrative': ['data/lexicons/afinn/*.txt','data/lexicons/bing/*.txt']},
      #data_files=[('pNarrative', ['pNarrative/data/AFINN-sv-165.txt'])],
      include_package_data=True,
      #install_requires=['re','numpy','matplotlib'],
      zip_safe=False)
