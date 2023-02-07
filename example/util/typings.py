import inspect
import logging
from typing import List, Optional, TypeVar, Union, get_args, get_origin

T = TypeVar("T")
K = TypeVar("K")


def required(arg: Optional[T]) -> T:
    """
    Optional[T] を T に変換する

    See Also
    --------
    https://stackoverflow.com/a/58841311
    """
    if get_origin(arg) is Union and type(None) in get_args(arg):
        return get_args(arg)[0]
    return arg


def infer_list_element(arg: Optional[List[K]]) -> K:
    """
    List[T] または Optional[List[T]] を T に変換する

    See Also
    --------
    https://stackoverflow.com/a/50101934
    """
    return get_args(required(arg))[0]


def inspect_init_param_type(target_class, key: str):
    """
    target_class における __init__ 関数について、 key にマッチする名称の引数の型を返す
    """
    parameters = inspect.signature(required(target_class).__init__).parameters
    if parameters.get(key) is None:
        logging.warning(
            f'Property: {key} is not included in class: {target_class}, so it was ignored.',
            {target_class: target_class, key: key},
        )
        return None
    return parameters.get(key).annotation


def infer_class_generics(arg):
    """
    Class[T] を T に変換する

    See Also
    --------
    https://stackoverflow.com/a/61058180
    """
    return get_args(arg.__orig_class__)[0]
