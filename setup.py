import os, setuptools
from setuptools.command.build_py import build_py

class with_pth(build_py):

    def run(self):
        super().run()
        pthfile = 'zwspy.pth'
        outfile = os.path.join(self.build_lib, pthfile)
        self.copy_file(pthfile, outfile, preserve_mode=0)

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setuptools.setup(
    name='zwspy',
    version='0.1.0',
    author='jakovsch',
    url='https://github.com/jakovsch/zwspy',
    description='Convert and run Python files with nonstandard indentation characters',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['zwspy', 'zwspy.codec'],
    cmdclass={'build_py': with_pth},
)
