=======================================
Clatter Command Line Application Tester
=======================================

.. image:: https://img.shields.io/pypi/v/clatter.svg
        :target: https://pypi.python.org/pypi/clatter

.. image:: https://travis-ci.org/delgadom/clatter.svg?branch=master
        :target: https://travis-ci.org/delgadom/clatter?branch=master

.. image:: https://coveralls.io/repos/github/delgadom/clatter/badge.svg?branch=master
        :target: https://coveralls.io/github/delgadom/clatter?branch=master

.. image:: https://readthedocs.org/projects/clatter/badge/?version=latest
        :target: https://clatter.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/delgadom/clatter/shield.svg
     :target: https://pyup.io/repos/github/delgadom/clatter/
     :alt: Updates

.. image:: https://api.codacy.com/project/badge/Grade/2c2af36490c04543b925edafc0d66842
    :target: https://www.codacy.com/app/delgadom/clatter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=delgadom/clatter&amp;utm_campaign=Badge_Grade


clatter is a doctest-style testing tool for command-line applications. It wraps other testing suites and allows them to be tested in docstrings.

* Free software: MIT license
* Documentation: https://clatter.readthedocs.io.


Features
--------

* Bring testing best practices to your command line apps
* Extensible - subclassing CommandValidator is trivial using any cli testing suite

Downsides
---------

* Security. CLI commands are dangerous, and we make no attempt to protect you. Use at your own risk.


Usage
-----

Test command line utilities and applications by whitelisting them with app-specific testing engines:

.. code-block:: python

    >>> teststr = r'''
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ echo 'Pining for the fjords'
    ...     Pining for the fjords
    ...     <BLANKLINE>
    ... '''
    >>>
    >>> tester = Runner()
    >>> tester.call_engines['echo'] = SubprocessValidator()
    >>> tester.validate(teststr)

Click applications
~~~~~~~~~~~~~~~~~~

Integrate your command line app:

.. code-block:: python

    >>> @click.command()
    ... @click.argument('name')
    ... def hello(name):
    ...     click.echo('Hello %s!' % name)

This can now be tested in docstrings:

.. code-block:: python

    >>> teststr = '''
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ hello Polly
    ...     Hello Polly!
    ...     <BLANKLINE>
    ... 
    ...     $ hello Polly Parrot
    ...     Usage: hello [OPTIONS] NAME
    ...     <BLANKLINE>
    ...     Error: Got unexpected extra argument (Parrot)
    ...     <BLANKLINE>
    ... 
    ...     $ hello 'Polly Parrot' # clitest: +NORMALIZE_WHITESPACE
    ...     Hello Polly Parrot!
    ... 
    ... '''

Click applications can be tested with a ``ClickValidator`` engine:

.. code-block:: python

    >>> tester = Runner()
    >>> tester.call_engines['hello'] = ClickValidator(hello)

    >>> tester.validate(teststr)


Mixed applications
~~~~~~~~~~~~~~~~~~

Your app can be combined with other command-line utilities by adding multiple engines:

.. code-block:: python

    >>> teststr = r'''
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ hello Polly
    ...     Hello Polly!
    ...     <BLANKLINE>
    ... 
    ...     $ echo 'Pining for the fjords'
    ...     Pining for the fjords
    ...     <BLANKLINE>
    ... 
    ... Pipes/redirects don't work, so we can't redirect this value into a file.
    ... But we can write a file with python:
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ python -c \
    ...     >     "with open('tmp.txt', 'w+') as f: f.write('Pushing up daisies')"
    ... 
    ...     $ cat tmp.txt
    ...     Pushing up daisies
    ... 
    ... '''

    >>> tester.call_engines['echo'] = SubprocessValidator()
    >>> tester.call_engines['python'] = SubprocessValidator()
    >>> tester.call_engines['cat'] = SubprocessValidator()

    >>> tester.validate(teststr)

Suppressing commands
~~~~~~~~~~~~~~~~~~~~

Commands can be skipped altogether with a ``SkipValidator``:

.. code-block:: python

    >>> skipstr = '''
    ... .. code-block:: bash
    ... 
    ...     $ aws storage buckets list
    ... 
    ... '''

    >>> tester = Runner()
    >>> tester.call_engines['aws'] = SkipValidator()

Illegal commands
~~~~~~~~~~~~~~~~

Errors are raised when using an application you haven't whitelisted:

.. code-block:: python

    >>> badstr = '''
    ... 
    ... The following block of code should cause an error:
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ rm tmp.txt
    ... 
    ... '''

    >>> tester.validate(badstr)
    Traceback (most recent call last):
    ...
    ValueError: Command "rm" not allowed. Add command caller to call_engines to whitelist.

Unrecognized commands will raise an error, even if +SKIP is specified

.. code-block:: python

    >>> noskip = '''
    ... .. code-block:: bash
    ... 
    ...     $ nmake all # clitest: +SKIP
    ... 
    ... '''
    >>> tester.validate(badstr)
    Traceback (most recent call last):
    ...
    ValueError: Command "nmake" not allowed. Add command caller to call_engines to whitelist.

Error handling
~~~~~~~~~~~~~~

Lines failing to match the command's output will raise an error

.. code-block:: python

    >>> teststr = r'''
    ... .. code-block:: bash
    ... 
    ...     $ echo "There, it moved!"
    ...     "No it didn't!"
    ...     <BLANKLINE>
    ... 
    ... '''
    
    >>> tester = Runner()
    >>> tester.call_engines['echo'] = SubprocessValidator()
    
    >>> tester.validate(teststr)
    Traceback (most recent call last):
    ...
    ValueError: Clatter test failed. There, it moved! != No it didn't!
    
    + There, it moved!
    
    - No it didn't!


Installation
------------

``pip install clatter``


Requirements
------------

* pytest


Todo
----

See `issues <https://github.com/delgadom/clatter/issues>`_ to see and add to our todos.

