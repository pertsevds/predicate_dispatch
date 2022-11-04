# Predicate_dispatch

![Github Actions](https://github.com/pdm-project/pdm/workflows/Tests/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/pertsevds/predicate_dispatch/badge.svg?branch=main)](https://coveralls.io/github/pertsevds/predicate_dispatch?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

Predicative dispatch decorator for Python, based on idea from [Functional Programming in Python](http://www.oreilly.com/programming/free/functional-programming-python.csp).

Module is providing means to specify condition with lambda function that determine which function is called.
Number of arguments in condition function in @predicate decorator must be equal to number of arguments of wrapped function.

## Installation

Predicate_dispatch requires Python 3.7 or higher.
```
pip install predicate_dispatch
```

## Usage

```
from predicate_dispatch import predicate

@predicate(lambda x: x > 1)
def factorial(x):
  return x * factorial(x - 1)

@predicate()
def factorial(x):
  return x
        
factorial(5) == 120
```

@predicate() - is a default predicate. It is used when none of other predicates resolves to True.

## Limitations

- Only one function as an argument in predicate.
- Only last one default predicate will be executed.

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
