from typing import Any, Dict, Optional, TypedDict

import os
import threading


class HeaderArgs(TypedDict, total=False):
    """
    RequestHeaderSingleton.get() の optional なキーワード引数の型

    See Also
    --------
    https://qiita.com/tktk0430/items/40f80dfba8fa8e3366b1
    """

    content_type: Optional[str]
    api_key: Optional[str]
    any_version: Optional[str]


class RequestHeaderSingleton(object):
    """
    リクエストヘッダの情報を保持するシングルトン

    See Also
    --------
    https://python-patterns.guide/gang-of-four/singleton/

    Fix Me
    --------
    次の値はリクエストヘッダの例であり、任意に修正されることを期待している
    - X-ANY-KEY     ... リクエストに必要な固定文字列
    - X-ANY-VERSION ... サーバにデプロイされたソースコードのバージョンを表す値
    - X-ANY-ID      ... リクエストのたびにサーバがインクリメントする値（多重リクエストされたときキャッシュを返すなどの目的）
    - X-ANY-TOKEN   ... 認証されたとき受け取るトークン
    """

    __instance = None
    __lock = threading.Lock()
    __x_any_token: Optional[str] = None
    __x_any_id: int = 0

    def __new__(cls):
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super(RequestHeaderSingleton, cls).__new__(cls)

        return cls.__instance

    def set_api_token(self, api_token: str) -> None:
        """
        ログイン状態を維持するためのトークンをセットする

        サインアップ、サインインしたレスポンスを受け取ったとき、コールされることを期待している
        """
        self.__x_any_token = api_token

    def get(
        self,
        *,
        content_type: Optional[str] = None,
        any_key: Optional[str] = None,
        any_version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        リクエストヘッダを取得する

        この関数がコールされるたびに X-ANY-ID の値がインクリメントされる
        したがってリクエストするたびにこの関数がコールされることを期待しており、
        一度リクエストヘッダとして使用した返り値は、異なるリクエストで使いまわしてはならない
        """

        self.__x_any_id += 1
        header = {
            "Content-Type": content_type or "application/json",
            "X-ANY-KEY": any_key or os.getenv("ANY_KEY"),
            "X-ANY-ID": str(self.__x_any_id),
        }

        if self.__x_any_token is not None:
            header["X-ANY-TOKEN"] = self.__x_any_token
        if any_version is not None:
            header["X-ANY-VERSION"] = any_version

        return header
