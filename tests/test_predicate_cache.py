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

from predicate_dispatch import predicate_cache

# def get_logs(x):
#     if x == 1:
#         return database.getLogsForDog()
#     if x == 2:
#         return database.getLogsForCat()
#     if x == 3:
#         return database.getLogsForFox()
#     return database.getLogsForOtherAnimal()


class Database:
    def getLogsForDog(self):
        global FN_COUNT
        return f"access from dog-{FN_COUNT}"

    def getLogsForCat(self):
        global FN_COUNT
        return f"access from cat-{FN_COUNT}"

    def getLogsForFox(self):
        global FN_COUNT
        return f"access from fox-{FN_COUNT}"

    def getLogsForOtherAnimal(self):
        global FN_COUNT
        return f"access from other-animal{FN_COUNT}"


db = Database()


@predicate_cache(lambda x: x == 1)
def get_logs(x):
    global db, FN_COUNT
    FN_COUNT += 1
    return db.getLogsForDog()


@predicate_cache(lambda x: x == 2)
def get_logs(x):
    global db, FN_COUNT
    FN_COUNT += 1
    return db.getLogsForCat()


@predicate_cache(lambda x: x == 3)
def get_logs(x):
    global db, FN_COUNT
    FN_COUNT += 1
    return db.getLogsForFox()


@predicate_cache()
def get_logs(x):
    global db, FN_COUNT
    FN_COUNT += 1
    return db.getLogsForOtherAnimal()


def test_predicate_cache():
    global FN_COUNT
    FN_COUNT = 0
    x = get_logs(1)
    y = get_logs(1)
    assert x != y
    assert FN_COUNT == 2


# test Exception


@predicate_cache(lambda x: x == 3)
def get_logs2(x):
    return db.getLogsForFox()


def test_predicate_cache_no_default():
    try:
        get_logs2(1)
        assert False, "Should throw TypeError exception"
    except TypeError as e:
        assert True
