# coding: utf-8

import os
import subprocess
from distutils import log
from distutils.cmd import Command
from setuptools import find_packages, setup


class InstallCythonCommand(Command):
  """ Custom command to install Cython via pip for use on xmake."""

  description = "command for use on xmake, run pip install cython"
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    assert os.environ.get("WORKSPACE"), "This command is only for use on xmake."
    command = [
      "{}/gen/out/venv/bin/python".format(os.environ["WORKSPACE"]),
      "{}/gen/out/venv/lib/python3.6/site-packages/pip".format(
        os.environ["WORKSPACE"]
      ),
      "install",
      "cython",
    ]
    self.announce("Running command: %s" % str(command), level=log.INFO)
    subprocess.check_call(command)


setup(
  author="SAP Conversational AI",
  author_email="hello@cai.tools.sap",
  description="SAP Conversational AI dataset translation",
  cmdclass={"install_cython": InstallCythonCommand},
  install_requires=open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'requirements.txt')), 'r').read().strip(),
  name="datasettranslation",
  entry_points={
      'console_scripts': [
        'dataset-translation  = dataset_translation.translation:main'
      ]
    },
  packages=find_packages(exclude=('tests', 'tests.*')),
  version=open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'version.txt')), 'r').read().strip(),
)
