from setuptools import find_packages, setup



setup(name='stdin_processor',
      version='0.0.48',
      description='String and Standard input manipulation CLI',
      author='midnight_repo',
      author_email='midnight_repo@protonmail.com',
      license='GPL-3.0',
      url='https://github.com/midnight-repo/stdin_processor',
      packages=find_packages(),
      entry_points = {'console_scripts': ['sp=stdin_processor.main:run'],},
      install_requires = ['typer']
      )
