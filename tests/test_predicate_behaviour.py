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

from predicate_dispatch import predicate, predicate_cache, predicate_cache_result

"""This a test how every type of `predicate_dispatch` decorators should behave"""


@predicate(lambda x: x == FN_COUNT)
def get_value(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT + 1


@predicate(lambda x: x < FN_COUNT)
def get_value(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT + 3


@predicate()
def get_value(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT * 2


def test_predicate_dispatch():
    """
    For the same execution of `get_value` with
    the same argument
    result must be different and
    real function executed every time.
    """
    global FN_COUNT
    FN_COUNT = 0
    assert get_value(0) == 2
    assert get_value(0) == 5
    assert FN_COUNT == 2


# cache


@predicate_cache(lambda x: x == 0)
def get_value_cache(x):
    global FN_COUNT
    FN_COUNT += 1
    return x + FN_COUNT


@predicate_cache(lambda x: x > 2)
def get_value_cache(x):
    global FN_COUNT
    FN_COUNT += 1
    return x + FN_COUNT


@predicate_cache()
def get_value_cache(x):
    global FN_COUNT
    FN_COUNT += 1
    return x + FN_COUNT


def test_this_predicate_cache_should_work_fine():
    """
    For the same execution of `get_value_cache` with
    the same argument
    result must be different and
    same real function executed every time.
    """
    global FN_COUNT
    FN_COUNT = 0
    assert get_value_cache(0) == 1
    assert get_value_cache(0) == 2
    assert FN_COUNT == 2


@predicate_cache(lambda x: x == FN_COUNT)
def get_value2(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT + 1


@predicate_cache(lambda x: x < FN_COUNT)
def get_value2(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT + 3


@predicate_cache()
def get_value2(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT * 2


def test_this_predicate_cache_should_break():
    """
    Here i'm using the same code as for `@predicate` decorator.
    Results in predicate lambda function will change over time.
    And when we try to use it with `@predicate_cache` we will get wrong results as it
    will take previous function choice for argument `x == 0` from cache
    and try to call function under `@predicate_cache(lambda x: x == FN_COUNT)`.
    """
    global FN_COUNT
    FN_COUNT = 0
    assert get_value2(0) == 2
    assert get_value2(0) != 5
    assert FN_COUNT == 2


# cache result


@predicate_cache_result(lambda x: x > 0)
def get_value_cache_result(x):
    global FN_COUNT
    FN_COUNT += 1
    return "1 > 0"


@predicate_cache_result(lambda x: x > 2)
def get_value_cache_result(x):
    global FN_COUNT
    FN_COUNT += 1
    return "x > 2"


@predicate_cache_result()
def get_value_cache_result(x):
    global FN_COUNT
    FN_COUNT += 1
    return "x < 0"


def test_this_predicate_cache_result_should_work_fine():
    """
    For the same execution of `get_value_cache_result`
    result must be the same and
    real function executed only first time,
    second time and after - result must be exctracted from cache.
    """
    global FN_COUNT
    FN_COUNT = 0
    assert get_value_cache_result(1) == "1 > 0"
    assert get_value_cache_result(1) == "1 > 0"
    assert get_value_cache_result(1) == "1 > 0"
    assert FN_COUNT == 1


@predicate_cache_result(lambda x: x == FN_COUNT)
def get_value3(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT + 1


@predicate_cache_result(lambda x: x < FN_COUNT)
def get_value3(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT + 3


@predicate_cache_result()
def get_value3(x):
    global FN_COUNT
    FN_COUNT += 1
    return FN_COUNT * 2


def test_this_predicate_cache_should_break():
    """
    And again i'm using the same code as for `@predicate` decorator.
    Results in predicate lambda function will change over time.
    And when we try to use it with `@predicate_cache_result` we will get wrong results as it
    will take previous result for argument `x == 0` from cache.
    And only execute real function once.
    """
    global FN_COUNT
    FN_COUNT = 0
    assert get_value3(0) == 2
    assert get_value3(0) != 5
    assert FN_COUNT != 2
