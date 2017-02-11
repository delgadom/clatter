=========================================
clatter Data Management System
=========================================

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


clatter is a doctest-style testing tool for command-line applications. It wraps other testing suites and allows them to be tested in docstrings.

* Free software: MIT license
* Documentation: https://clatter.readthedocs.io.


Features
--------

* Test stuff


Usage
-----

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

Your app can be combined with other command-line utilities by adding
``SubprocessValidator`` engines:

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
    ... Pipes don't work, so we can't redirect this value into a file. But we can 
    ... write a file with python:
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

    >>> os.remove('tmp.txt')


.. code-block:: python

    >>> skipstr = '''
    ... 
    ... The following command will be skipped:
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ aws storage buckets list
    ... 
    ... '''

    >>> tester = Runner()
    >>> tester.call_engines['aws'] = SkipValidator()


    >>> noskip = '''
    ... 
    ... Unrecognized commands will raise an error, even if +SKIP is specified
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ nmake all # clitest: +SKIP
    ... 
    ... '''

    >>> with pytest.raises(ValueError):
    ...     tester.validate(noskip)


.. code-block:: python

    >>> teststr = r'''
    ... 
    ... Lines failing to match the command's output will raise an error
    ... 
    ... .. code-block:: bash
    ... 
    ...     $ echo "There, it moved!"
    ...     "No it didn't!"
    ...     <BLANKLINE>
    ... 
    ... '''

    >>> tester = Runner()
    >>> tester.call_engines['echo'] = SubprocessValidator()

    >>> with pytest.raises(ValueError):
    ...     tester.validate(teststr)


Installation
------------

``pip install clatter``


Requirements
------------

* pytest


Todo
----

See `issues <https://github.com/delgadom/clatter/issues>`_ to see and add to our todos.


Credits
---------

This package was created by `Justin Simcock <https://github.com/jgerardsimcock>`_ and `Michael Delgado <https://github.com/delgadom>`_ of the `Climate Impact Lab <http://impactlab.org>`_. Check us out on `github <https://github.com/delgadom>`_.

Major kudos to the folks at `PyFilesystem <https://github.com/PyFilesystem>`_. Thanks also to `audreyr <https://github.com/audreyr>`_ for the wonderful `cookiecutter <https://github.com/audreyr/cookiecutter-pypackage>`_ package, and to `Pyup <https://pyup.io>`_, a constant source of inspiration and our silent third contributor.
