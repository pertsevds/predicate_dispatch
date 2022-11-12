# Predicate_dispatch

![Github Actions](https://github.com/pdm-project/pdm/workflows/Tests/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/pertsevds/predicate_dispatch/badge.svg?branch=main)](https://coveralls.io/github/pertsevds/predicate_dispatch?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

Predicative dispatch decorator for Python, based on the idea from [Functional Programming in Python](http://www.oreilly.com/programming/free/functional-programming-python.csp).

The module is providing means to specify conditions with a lambda function that determines which function is called.
The number of arguments in the condition function in the `@predicate` decorator must be equal to the number of arguments of the wrapped function.

## Installation

Predicate_dispatch requires Python 3.7 or higher.
```
pip install predicate_dispatch
```

## Basic usage

```python
from predicate_dispatch import predicate

@predicate(lambda x: x > 1)
def factorial(x):
  return x * factorial(x - 1)

@predicate()
def factorial(x):
  return x
        
factorial(5) == 120
```

`@predicate()` - is the default predicate. It is used when none of the other predicates resolves to True.

## Caching

### Types of cache in predicate_dispatch functions

| Decorator name | Cache type |
| ----------- | ----------- |
| `predicate` | Without cache |
| `predicate_cache` | Function choice is cached |
| `predicate_cache_result` | Function result is cached |

### `predicate` - without cache

You must use the `predicate` decorator if the result of the lambda function in the predicate for the same argument `x` changes over time. For example, if you compare `x` to the current time or execution count.

If you don't want to dig deeper into the quirks of caching just use the `predicate` decorator.

For example:

```python
def get_events(x):
    if x >= time.time():
        return database.getFutureEvents()
    if x < time.time():
        return database.getPastEvents()
    return []
```

To this:

```python
@predicate(lambda x: x >= time.time())
def get_events(x):
    return database.getFutureEvents()

@predicate(lambda x: x < time.time())
def get_events(x):
    return database.getPastEvents()

@predicate()
def get_events(x):
    return []
```

### `predicate_cache` - function choice is cached

You may use the `predicate_cache` decorator if the result of the lambda function in the predicate for the same argument `x` does not change over time, but the result from calling the real function will change. This decorator will cache what function was called previously for certain `x`. For example, if you have code like this:

```python
def get_logs(x):
    if x == 1:
        return database.getLogsForDog()
    if x == 2:
        return database.getLogsForCat()
    if x == 3:
        return database.getLogsForFox()
    return database.getLogsForOtherAnimal()
```

You may rewrite it to the `predicate_cache` decorator like this:

```python
@predicate_cache(lambda x: x == 1)
def get_logs(x):
    return database.getLogsForDog()

@predicate_cache(lambda x: x == 2)
def get_logs(x):
    return database.getLogsForCat()

@predicate_cache(lambda x: x == 3)
def get_logs(x):
    return database.getLogsForFox()

@predicate_cache()
def get_logs(x):
    return database.getLogsForOtherAnimal()
```

When you first call `get_logs(3)` internally it will compare `3` then to `1`, then `3` to `2`, then `3` to `3` and execute `db.getLogsForFox()`. When you call `get_logs(3)` again it will take the previous function choice from the cache and straightaway execute `db.getLogsForFox()`.

### `predicate_cache_result` - function result is cached

You may use the `predicate_cache_result` decorator if the result of the lambda function in the predicate for the same argument `x` does not change over time and the result from calling the real function does not change over time. This decorator will cache the previous result of calling the function with a certain `x`. A typical example would be when you want to use `predicate_dispatch` instead of many static ifs.

From this:

```python
def get_animal(x):
    if x == 1:
        return "dog"
    if x == 2:
        return "cat"
    if x == 3:
        return "fox"
    return "animal"
```

To this:

```python
@predicate_cache_result(lambda x: x == 1)
def get_animal(x):
    return "dog"

@predicate_cache_result(lambda x: x == 2)
def get_animal(x):
    return "cat"

@predicate_cache_result(lambda x: x == 3)
def get_animal(x):
    return "fox"

@predicate_cache_result()
def get_animal(x):
    return "animal"
```

When you first call `get_animal(3)` internally it will compare `3` then to `1`, then `3` to `2`, then `3` to `3` and then return result `"fox"`. When you call `get_animal(3)` again it will take the previous result from the cache and return it.


## Limitations

- The number of arguments in the condition function in the `@predicate` or `@predicate_cache` or `@predicate_cache_result` decorator must be equal to the number of arguments of the wrapped function.
- Only one function as an argument in the predicate.
- Only the last default predicate will be executed.

## License

```
Copyright 2015 Juraj Sebin <sebin.juraj@gmail.com>
Copyright 2022 Dmitriy Pertsev <davaeron@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Similar projects

- [plum](https://github.com/wesselb/plum)
- [multipledispatch](https://github.com/mrocklin/multipledispatch)
