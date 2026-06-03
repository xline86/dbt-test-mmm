## プロジェクト

Snowflake と dbt Core で、ranking JSON を RAW にロードし、staging と mart を作る学習用プロジェクトです。

RAW の日時型は `TIMESTAMP_NTZ` を使います。`TIMESTAMP_LTZ` は使いません。

RAW ロードは Python の PUT と SQL の COPY INTO に分けます。内部 stage は `raw.mmm_ranking_stage` を 1 つだけ使います。

## データ

`data/` には1200件以上、`data/player_ranking/` にも300件以上の大きな JSON があります。JSON 本体は直接読まないでください。

ファイル名だけ確認する場合は次を使います。

```sh
ls data/player_ranking | sort -r | head -n 5
ls data/guild_ranking | sort -r | head -n 5
```

データ構造は次を参照する
-  [docs/player_rankingデータ構造.md](docs/player_rankingデータ構造.md)
-  [docs/guild_rankingデータ構造.md](docs/guild_rankingデータ構造.md)

## チェック

通常の確認は次を使います。

```sh
make check
```

`make check` は `ruff check src tests`、`pyright`、`pytest` を実行します。

- コードを整形する場合は次を使う。
```sh
uv run ruff format .
```

- lintの自動修正が必要な場合は次を使う。
```sh
uv run ruff check . --fix
```

## Git / Commit
- コミットメッセージの形式: Conventional Commits に準拠する。
- 言語: コミットメッセージの要約および本文は日本語で記述する。
- 記述内容:
  - 1行目に変更内容の要約を書く。
  - 関連するIssueがある場合は、フッターに `Ref: #123` の形式でリンクを貼る。
  - Issueへのリンクがない場合や、複雑な変更の場合は、本文に変更の理由や背景を箇条書きで記述する。
- コミットの粒度: 
  - 「1コミット1機能（1アトミックコミット）」を徹底する。
  - そのコミット単体でビルドが通り、動作確認が可能な最小単位とする。
