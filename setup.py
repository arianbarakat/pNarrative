from setuptools import setup

setup(name='pNarrative',
      version='0.1',
      description='A python module to estimate the narrative arcs in literature',
      url='',
      author='Arian Barakat',
      author_email='arianbarakat@gmail.com',
      license='MIT',
      packages=['pNarrative'],
      install_requires=[
          're',
          'numpy',
          'inspect',
          'matplotlib.pyplot'
      ],
      zip_safe=False)
