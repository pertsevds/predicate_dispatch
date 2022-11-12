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

"""Predicate dispatch"""

from functools import lru_cache
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple

ConditionFunction = Callable[[Any], bool]
CodeFunction = Callable[[Any], Any]
PredicateTuple = Tuple[ConditionFunction, CodeFunction]
CallableList = List[PredicateTuple]


def _default_condition(*_: Any, **__: Any) -> bool:
    return True


class _PredicatesList:
    """Class for a list of predicate functions (lambda condition) and original code functions"""

    __slots__: Tuple[str, str] = ("_list", "_default_func_tuple")

    def __init__(self) -> None:
        self._list: CallableList = []
        self._default_func_tuple: Optional[PredicateTuple] = None

    def add(self, condition: ConditionFunction, func: CodeFunction) -> None:
        """Add predicate function (lambda condition) and original code function to the list"""
        if condition is not _default_condition:
            self._list.append((condition, func))
        else:
            self._default_func_tuple = condition, func

    def __iter__(self) -> Iterator[PredicateTuple]:
        for x in self._list:
            yield x
        if self._default_func_tuple is not None:
            yield self._default_func_tuple


_conditional_callables: Dict[str, _PredicatesList] = {}


def _get_qualname(func: CodeFunction) -> str:
    return func.__module__ + func.__qualname__


def _add_callable(condition: ConditionFunction, func: CodeFunction) -> None:
    qual_name: str = _get_qualname(func)
    _conditional_callables.setdefault(qual_name, _PredicatesList()).add(condition, func)


def _resolve_callable(
    func: CodeFunction, *args: Any, **kwargs: Any
) -> Optional[CodeFunction]:
    qual_name: str = _get_qualname(func)
    callable_iterator = (
        cc[1] for cc in _conditional_callables[qual_name] if cc[0](*args, **kwargs)
    )
    return next(callable_iterator, None)


@lru_cache(maxsize=None, typed=True)
def _resolve_callable_cached(
    func: CodeFunction, *args: Any, **kwargs: Any
) -> Optional[CodeFunction]:
    qual_name: str = _get_qualname(func)
    callable_iterator = (
        cc[1] for cc in _conditional_callables[qual_name] if cc[0](*args, **kwargs)
    )
    return next(callable_iterator, None)


def predicate(condition: ConditionFunction = _default_condition) -> CodeFunction:
    """Predicate decorator function"""

    def wrapper(func: CodeFunction) -> CodeFunction:
        _add_callable(condition, func)

        def wrapped(*args: Any, **kwargs: Any) -> Any:
            resolved_callable: Optional[CodeFunction] = _resolve_callable(
                func, *args, **kwargs
            )
            if resolved_callable is not None:
                return resolved_callable(*args, **kwargs)
            raise TypeError(
                f"Default predicate for '{_get_qualname(func)}' is not found"
            )

        return wrapped

    return wrapper


def predicate_cache(condition: ConditionFunction = _default_condition) -> CodeFunction:
    """Predicate decorator function that cache choosen function for argument"""

    def wrapper(func: CodeFunction) -> CodeFunction:
        _add_callable(condition, func)

        def wrapped(*args: Any, **kwargs: Any) -> Any:
            resolved_callable: Optional[CodeFunction] = _resolve_callable_cached(
                func, *args, **kwargs
            )
            if resolved_callable is not None:
                return resolved_callable(*args, **kwargs)
            raise TypeError(
                f"Default predicate for '{_get_qualname(func)}' is not found"
            )

        return wrapped

    return wrapper


def predicate_cache_result(
    condition: ConditionFunction = _default_condition,
) -> CodeFunction:
    """Predicate decorator function that cache result"""

    def wrapper(func: CodeFunction) -> CodeFunction:
        _add_callable(condition, func)

        @lru_cache(maxsize=None, typed=True)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            resolved_callable: Optional[CodeFunction] = _resolve_callable(
                func, *args, **kwargs
            )
            if resolved_callable is not None:
                return resolved_callable(*args, **kwargs)
            raise TypeError(
                f"Default predicate for '{_get_qualname(func)}' is not found"
            )

        return wrapped

    return wrapper
