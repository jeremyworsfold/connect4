from dataclasses import dataclass
from typing import Dict, Callable, List, Any

@dataclass
class klass:
    thing1: str
    thing2: int
    dic: Dict

    def a_method(self, val: int, l: List[Any]) -> int:
        return self.thing2 + val


def func1(k: klass):
    k.dic['item']
    val2 = k.a_method(2)
    return int(k.thing1) + k.thing2 + val2


def func2(k):
    k.dic['item']
    k.dic['item']
    val2 = k.a_method(2)
    return int(k.thing1) + k.thing2 + val2