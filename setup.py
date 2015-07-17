from distutils.core import setup

VERSION = '0.0.1'

longdesc = """\
Chinchilla
==========

Chinchilla is a Python library for easy web page interaction.
Using an intuitive syntax to simulate user interaction, you can fill out forms and follow links.

Since chinchilla will use cookies, you can use it to access content that is protected by login.

Usage
=====

    from chinchilla import *
    visit("http://localhost:8000/login/")
    fill_in("username", "markus")
    fill_in("password", "secret")
    submit()
    click_link("Secret page")
    print page_content()
    print page_url()

Inspired by the ruby [capybara](https://github.com/jnicklas/capybara) testing framework.
"""
setup(name='chinchilla',
    version=VERSION,
    description='Python library for easy web page interaction',
    long_description=longdesc,
    url='https://git.persephone.casadelkrogh.dk/chinchilla.git/',
    author='Markus Krogh',
    author_email='markus@nordu.net',
    license='MIT',
    packages=['chinchilla'],
    install_requires=['beautifulsoup4'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

