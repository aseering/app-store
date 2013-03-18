from setuptools import setup, find_packages

setup(name='app_store',
      version=0.5,
      description="App Store for Vertica",
      zip_safe=False,
      author="Adam Seering",
      author_email="aseering@vertica.com",
      packages=find_packages(),
      include_package_data=True,
      install_requires=['django>=1.4',
                        'django-userena'],
      classifiers = ['Development Status :: 4 - Beta',
                     'Environment :: Web Environment',
                     'Framework :: Django',
                     'Intended Audience :: Developers',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python'],
)
