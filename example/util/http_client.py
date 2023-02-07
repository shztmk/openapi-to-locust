from typing import Tuple

from jsons import JsonSerializable
from locust.contrib.fasthttp import (
    FastHttpSession,
    ResponseContextManager,
    FastResponse,
)
from util.dictionary import convert_key_to_camel_case


class HttpSession(FastHttpSession):
    def request(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        data: JsonSerializable = None,
        **kwargs,
    ) -> Tuple[ResponseContextManager | FastResponse, dict]:
        res = super().request(
            method=method,
            url=url,
            headers=headers,
            json=convert_key_to_camel_case(data.json),  # 型が一致していないが、実行時エラーにはならない
            **kwargs,
        )

        return res, res.json()
