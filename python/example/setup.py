try:
    from py_backwards_packager import setup
except ImportError:
    from setuptools import setup
setup(name='example',
      version='0.1',
      description='example',
      author='x',
      packages=['example'],
      zip_safe=True,
      py_backwards_targets=['2.7', '3.5'],      
)
