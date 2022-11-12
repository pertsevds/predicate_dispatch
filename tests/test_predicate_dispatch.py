# Copyright 2015 Juraj Sebin <sebin.juraj@gmail.com>
# Copyright 2022 Dmitriy Pertsev <davaeron@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# type: ignore
# pylint: skip-file

from predicate_dispatch import predicate


@predicate()
def foo(v):
    return "foo-default"


@predicate(lambda v: v == 1)
def foo(v):
    return "f1"


@predicate(lambda v: v == 2)
def foo(v):
    return "f2"


@predicate(lambda v: v == 3)
def foo(v):
    return "f3"


@predicate(lambda x, y: x == 3 and y == 2)
def foo_multiple(x, y):
    return True


@predicate()
def foo_multiple(x, y):
    return False


@predicate(lambda x: x > 1)
def factorial(x):
    return x * factorial(x - 1)


@predicate()
def factorial(x):
    return x


@predicate(lambda x: x == 1)
def bar(x):
    return True


@predicate()
def baz():
    """baz-doc"""
    return "baz-default"


def test_predicate_factorial1():
    assert factorial(1) == 1


def test_predicate_factorial5():
    assert factorial(5) == 120


def test_predicate_foo_v1():
    assert foo(v=1) == "f1"


def test_predicate_foo1():
    assert foo(1) == "f1"


def test_predicate_foo2():
    assert foo(2) == "f2"


def test_predicate_foo3():
    assert foo(3) == "f3"


def test_predicate_foo_default():
    assert foo("x") == "foo-default"


def test_predicate_foo_4_5():
    assert foo_multiple(4, 5) == False


def test_predicate_foo_3_2():
    assert foo_multiple(3, 2) == True


def test_predicate_foo_x3_y3():
    assert foo_multiple(x=3, y=3) == False


def test_predicate_foo_3_y2():
    assert foo_multiple(3, y=2) == True


def test_predicate_no_default():
    try:
        bar(2)
        assert False, "Should throw TypeError exception"
    except TypeError as e:
        assert True


def test_predicate_only_default():
    assert baz() == "baz-default"


class TestClassA:
    @predicate()
    def foo(self):
        return "default-from-classA"


class TestClassB:
    @predicate()
    def foo(self):
        return "default-from-classB"


def test_predicate_two_classes_with_same_function_name():
    a = TestClassA()
    b = TestClassB()
    assert a.foo() == "default-from-classA"
    assert b.foo() == "default-from-classB"


@predicate(lambda x: isinstance(x, int))
def isint(x):
    return True


@predicate()
def isint(x):
    return False


def test_predicate_isint():
    assert isint(1) == True
    assert isint("a") == False
