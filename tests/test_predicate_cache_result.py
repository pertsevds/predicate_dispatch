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

from predicate_dispatch import predicate_cache_result

# def get_animal(x):
#     if x == 1:
#         return "dog"
#     if x == 2:
#         return "cat"
#     if x == 3:
#         return "fox"
#     return "animal"


@predicate_cache_result(lambda x: x == 1)
def get_animal(x):
    global FN_COUNT
    FN_COUNT += 1
    return "dog"


@predicate_cache_result(lambda x: x == 2)
def get_animal(x):
    global FN_COUNT
    FN_COUNT += 1
    return "cat"


@predicate_cache_result(lambda x: x == 3)
def get_animal(x):
    global FN_COUNT
    FN_COUNT += 1
    return "fox"


@predicate_cache_result()
def get_animal(x):
    global FN_COUNT
    FN_COUNT += 1
    return "animal"


def test_predicate_cache_result():
    global FN_COUNT
    FN_COUNT = 0
    assert get_animal(1) == "dog"
    assert get_animal(1) == "dog"
    assert FN_COUNT == 1


# test Exception


@predicate_cache_result(lambda x: x == 3)
def get_animal2(x):
    return "fox"


def test_predicate_cache_result_no_default():
    try:
        get_animal2(1)
        assert False, "Should throw TypeError exception"
    except TypeError as e:
        assert True
