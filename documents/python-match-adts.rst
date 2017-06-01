.. Refs: https://mail.python.org/pipermail/python-ideas/2015-April/thread.html#32907

Background
==========

Several languages have a facility, derived from Prolog (via ML) of unifying expressions with other expressions. For example, in ocaml:

.. code-block:: ocaml

  let equal c = match c with 
      (x,x) -> true
    | (x,y) -> false;;

  let is_a_vowel c = match c with 
      'a' | 'e' | 'i' | 'o' | 'u' | 'y' -> true 
    | _ -> false ;; 

This is based on two concepts: *algebraic data types* and *unification* (also called pattern matching). Algebraic Data Types (ADTs) are built up as a disjunction (sum) or (Cartesian) product or atoms, for example:

.. code-block:: ocaml

  type http_response =
    | Response of int * string
    | Timeout
    | NetworkError of string ;;

Product types are similar to Python's ``typing.NamedTuple`` class, and sum types are similar to the functionality in the ``enum`` module.

Unification matches the structure of data types recursively, allowing matching up structural elements with free variables in another expression. Python has already developed several unification-like operations: \*unpacking, and tuple/list unpacking. For example:

.. code-block:: python

  (x, *_, y) = range(10)  # x=0, y=9



However, the following does not work:

.. code-block:: python

  class MyTuple(NamedTuple):
      foo : int
      bar : str

  MyTuple(foo=x, bar=_) = MyTuple(foo=1, bar='asdf')
  {1: x, **_} = {1: 2, 3: 4}

Strawman proposal for syntax
============================

Matchable patterns would follow something like the following grammar:


.. code-block:: python

  from typing import NamedTuple

  class Variable(NamedTuple):
      name : str

  class Pattern(NamedTuple):
      cls : type
      args : tuple
      kwargs : dict


To do a pattern match, the following syntax would be used:

.. code-block:: python

  match expression as pattern1:
      ...
  else as pattern2:
      ...
  else:
      ...


Classes which are unifiable / matchable would define an instance method called ``__unify__``

.. code-block:: python

  class MyClass:
      def __unify__(self, pattern: Union[Pattern, Variable, Any]) -> Dict[str, object]:
          ...

When an object's ``__unify__`` method returned something other than ``None``, the local namespace would be updated with its returned dict.

Examples
--------


.. code-block:: python

    x = 1
    match (x, 1) as (y, y):
        ...

This would pass ``Pattern(tuple, (Variable('y'), Variable('y')), {})`` to ``(x, 1).__unify__``.


.. code-block:: python

    match x as Foo(y, Bar(z), quux=_):
        ...


This would pass ``Pattern(Foo, (Variable('y'), Pattern(Bar, (Variable('z'), ), {})), {'quux': ANY})`` to ``x.__unify__``. The ``ANY`` sentinel can be repeated any number of times, and unifies with anything.

.. code-block:: python

    x = {1: 2, 3: 4}
    match x as {1: x, **rest}:
        ...

To avoid uniqueness issues, variables would only be allowed in values of dictionaries. TODO: how to represent ``rest`` in this case

Benefits & Use Cases
====================

What about PEPs 3103 and 275?
-----------------------------

Much of the discussion in the `python-ideas thread`_ centered around how useful match statements are, and whether they're just switch statements in another guise, an idea which was already rejected in `PEP 3103`_ and `PEP 275`_. There are several reasons to revisit those decisions as they apply to a ``match`` statement. 

First, PEP 3103 was rejected in 2006 with the note:

    A quick poll during my keynote presentation at PyCon 2007 shows this proposal has no popular support. I therefore reject it.

That's not a strong reason for rejecting it, especially considering the software world has changed substantially in the past 11 years. For example, new languages have come to the fore, notably `Rust`_ and `Swift`_, which implement pattern matching. Python usually attempts to be more readable and concise than lower-level systems languages, so this suggests that pattern matching would be a useful addition. 

Additionally, `many python libraries`_ have been independently introduced to try to achieve pattern matching with varying levels of alteration to the language, none of which has produced an elegant syntax without either extending the language (Coconut) or monkey-patching the parser (MacroPy). This suggests there is a strong perceived need in a subset of python developers, indluding developers of widely used frameworks like Matthew Rocklin (of pytoolz and Dask fame, who also developed ``unification`` and ``multipledispatch``). 

Developments within the Python core language have made pattern matching more appealing:

* The `attrs`_ library is becoming increasingly popular, yielding a good, usable template API to add algebraic datatypes to. In particular, any class using ``attr.s`` which does not transform its arguments could have a unification method added to it fairly easily. (For example, see `the unification logic`_ for ``__slots__`` objects in the unification library.)
* The introduction of the `typing`_ module and the `mypy`_ type checker afford much of the type logic required to make pattern matching genuinely useful.

Use cases
---------

Dict unpacking:

.. code-block:: python

    match x as {'key1': value1, 'key2': value2, **rest}:
        return do_something(value1, value2)
    else as {'key1': value1, **rest}:
        return something_else(value1)
    else:
        raise ValueError('key1 is required')

This sort of argument-checking code is quite common in Python and a bit awkward to do:

.. code-block:: python

    if 'key1' in x and 'key2' in x:
        return do_something(x['key1'], x['key2'])
    elif 'key1' in x:
        return something_else(x['key1'])
    else:
          raise ValueError('key1 is required')

Note that key1 and key2 are repeated in several places, and the most natural code to write does not give the values names.

---

.. code-block:: python

Process execution:

.. code-block:: python

    def execute_command_and_retry(retries=10):
        process = subprocess.POpen(...)
        stdout, stderr = process.communicate()
        match stdout, stderr, process.returncode as (_, '', 0):
            return process_output(stdout)
        else as (_, _, 0):
            raise CommandError('stderr=%r unexpectedly returned on successful execution' % stder)
        else as (_, _, 1):
            return execute_command_and_retry(retries=retries - 1)
        else as (_, _, _):
            raise 

Prior Art
=========

Many Python libraries attempt to add support for pattern matching to the language. We'll describe the syntax/solution, then describe why the features are inadequate or undesirable.

-------

Macropy_ provides a custom import hook to allow syntactic macros inside Python code. Pattern matching uses the following syntax:

.. code-block:: python

    @case
    class Nil():
        pass

    @case
    class Cons(x, xs):
        pass

    with switch(my_list):
        if Cons(x, Nil()):
            return x
        elif Cons(x, xs):
            return op(x, reduce(op, xs))

The syntax is a bit confusing, and ``case`` might be preferrable to match ``switch``. It's also not particularly explicit, since it gives multiple meanings to ``with`` and ``if``. The main issue with macropy is that it needs to define its own module loader. This is a pretty invasive thing to do to the Python runtime, and so isn't suitable for library code which might need to run in a variety of environments. Additionally 

.. _Macropy: https://github.com/lihaoyi/macropy
.. _python-ideas thread: https://mail.python.org/pipermail/python-ideas/2015-April/thread.html#32907
.. _PEP 3103: https://www.python.org/dev/peps/pep-3103/
.. _PEP 275: https://www.python.org/dev/peps/pep-0275/
.. _Rust: https://doc.rust-lang.org/book/patterns.html
.. _Swift: https://developer.apple.com/library/content/documentation/Swift/Conceptual/Swift_Programming_Language/Patterns.html
.. _attrs: https://github.com/python-attrs/attrs
.. _not a lot of value: https://mail.python.org/pipermail/python-ideas/2015-April/032912.html
.. _patterns: https://pypi.python.org/pypi/patterns
.. _py-pattern-matching: https://pypi.python.org/pypi/py-pattern-matching
.. _many python libraries: https://github.com/grantjenks/python-pattern-matching
.. _the unification logic: https://github.com/mrocklin/unification/blob/d3699fb5c029a63fc34b597bc4ce9ab66d638d86/unification/more.py#L115
.. _typing: https://docs.python.org/3/library/typing.html
.. _mypy: http://mypy-lang.org/
.. _A pattern-matching case statement for Python: http://stupidpythonideas.blogspot.com/2014/08/a-pattern-matching-case-statement-for.html
