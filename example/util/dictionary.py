from typing import List
import inflection


def reject_by_key(target: dict, keys: List[str]) -> dict:
    return {k: v for k, v in target.items() if k not in keys}


def convert_key_to_camel_case(target: dict) -> dict:
    converted: dict = {}
    for k, v in target.items():
        converted_key = inflection.camelize(k, False)
        if isinstance(v, dict):
            converted[converted_key] = convert_key_to_camel_case(v)
        else:
            converted[converted_key] = v

    return converted


def ignore_none_type_key(target: dict) -> dict:
    converted: dict = {}
    for k, v in target.items():
        if k is None:
            continue

        if isinstance(v, dict):
            converted[k] = ignore_none_type_key(v)
        else:
            converted[k] = v

    return converted
