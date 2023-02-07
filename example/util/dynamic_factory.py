import logging
import importlib
import inflection
from typing import Any, Dict, Generic, List, Optional, TypeVar

from util.typings import (
    infer_class_generics,
    infer_list_element,
    inspect_init_param_type,
    required,
)

T = TypeVar("T")
K = TypeVar("K")


class DynamicFactory(Generic[T]):
    def create(self, convert_from: Dict[str, Any]) -> T:
        """
        Dict 型の convert_from を, models で定義された型として再帰的に instantiate する
        :param convert_from: 変換元となるデータ
        :return: instantiate された T

        See Also
        --------
        https://stackoverflow.com/a/27550113
        """
        # T として指定されたクラスの名前を取得する
        generic_class_name = infer_class_generics(self).__name__
        return self.__instantiate_recursively(
            # 名前空間 model から該当するクラスを import する
            getattr(importlib.import_module("model"), generic_class_name),
            convert_from,
        )

    def __instantiate_recursively(
        self, target_class: Optional[K], dict_from: Dict[str, Any]
    ) -> K:
        # Optional[X] 型だと後続の処理が面倒になるので、初めに X 型にしておく
        required_target_class = required(target_class)

        dict_to: Dict[str, Any] = {}
        for key, value in dict_from.items():
            if key is None:
                logging.warning(
                    f'Key for this value: {value} is None type, so it was ignored.',
                    {target_class: target_class, value: value},
                )
                continue

            key = inflection.underscore(key)

            # target_class における __init__ の引数のうち、key にマッチする名称の型を取得しておく
            target_type = inspect_init_param_type(required_target_class, key)
            if target_type is None:
                # target_class に存在しないプロパティが dict_from に定義されていた場合は無視する
                continue

            if isinstance(value, list):
                # List[X] から X の型を取得しておく
                element_type = infer_list_element(target_type)
                # value が List 型であるときは各要素について再帰的に処理する
                carry: List[Any] = []
                for element in value:
                    carry.append(
                        self.__internal(
                            element_type,
                            element,
                        )
                    )

                dict_to[key] = carry
                continue

            dict_to[key] = self.__internal(target_type, value)
        return required_target_class(**dict_to)

    def __internal(self, target_class, value):
        if isinstance(value, dict):
            # value が Dict 型であるときは型が定義されているとして instantiate して返す
            return self.__instantiate_recursively(target_class, value)

        # List, Dict いずれの型でないならば primitive な値であるとして instantiate せず、そのまま返す
        return value
