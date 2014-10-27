Dumpy
=====

A decorator and utility library.

Mostly a place to dump snippets of code though.

Installing
----------

```sh
python setup.py install
```

Testing
-------

```sh
pip install Mock
python setup.py test
```

Examples
--------

Most basic usage:

```python
from dumpy import retry

@retry(5)
def test_function():
    print('this is going to print 5 times')
    1 / 0

test_function()
```

You are also allowed to specify exceptions and a timeout:

```python
import time
from dumpy import retry

@retry(5, ZeroDivisionError, 0.02)
def test_function():
    print("if this test results in a ZeroDivisionError each time, this will "
          "repeat 5 times, as long as it doesn't take more than 0.02s to run.")
    time.sleep(0.05)
    1 / 0
```
