# openapi-to-locust

これは OpenAPI の定義から、Python で記述された Model ファイルと Api ファイルを自動生成するためのツールです  
自動生成された成果物は、 Locust で使用することを想定して作成しています

## 使い方

基本的に Docker で動かすことを想定しています  
Makefile にショートカットを定義してあるので、make コマンドを叩けると便利です

1. `make init` をして、`.env` と `node_modules` を用意します
1. `.env` に `openapi.yaml` のパスを（ファイル名を含めて）指定します
    1. openapi-generator-cli は相対パスを解釈できないので、`openapi.yaml` 1 ファイルに定義をすべてまとめた状態にする必要があります
1. `make generate-locust` で Model ファイルと Api ファイルを自動生成します
    1. OpenAPI に example を網羅的に定義しているのであれば `make generate-locust-example` で example ファイルもまた自動生成できます
1. `./dist/locust/api`, `./dist/locust.model` に成果物が格納されます
    1. `./example/util` にあるファイルも使用することを想定しているので、一緒にコピーしてください
    1. コピーされた `./example/util` にあったファイルは、プロジェクトの要求にあわせて書き換えられることを想定しています

## 妥協点

### 冗長な import

model モジュールにおいて、不要な import は消すことができたのですが、  
重複して冗長になっている import を消すことができなかったので、残ってしまっています

なお model モジュールにおいては `from model import *` と指定することはできません  
循環参照になってしまうためです

### 実装範囲

OpenAPI が表現できる定義すべてを変換できる、といったことは、いまのところ目指していません  
このツールを作成する目的となったプロジェクトで、最低限動く程度までしか実装していません

もし動かない部分があったら issue や PR などを雑に投げてください

### generator のバージョン

https://github.com/OpenAPITools/openapi-generator の最新 ( >= 6.2) を使いたかったのですが、  
`Unable to make field transient` といったエラーを避けたいので、ひとまず 6.1.0 にしています  
cf. https://github.com/OpenAPITools/openapi-generator/issues/11763  
cf. https://github.com/OpenAPITools/openapi-json-schema-generator/issues/3

### リテラルをラップしたオブジェクトの example

```yaml
    WrappedObject:
      title: WrappedObject
      type: integer
      maximum: 2
      minimum: 1
      example: 1
```

上記のような定義をしたとき、mustache になぜか example が降ってきません

ですので、実行時エラーが発生するようなファイルが自動生成されてしまいますが、  
ひとまず現時点では、逐一手動で直してもらうものとして妥協しています

## コンテナについて

- python3
    - 自動生成した Python のコードを整形するためのコンテナです
- node
    - openapi-generator-cli を実行するためのコンテナです
- locust
    - 開発用のもので、IDE のインタプリタとして指定するためのものです
        - ですので、このコンテナはビルドしておくだけで、コマンドの実行などは一切行いません

### メモ

- mustache ファイルに降ってくる変数を確認したいときは、`{{{this}}}` などとすると一通り dump されます
- locust のプロジェクトにおいて、logging パッケージなどを使用すると、worker コンテナの標準出力に書き出されます
