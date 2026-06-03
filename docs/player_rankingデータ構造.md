
`data/player_ranking`にはプレイヤーのランキング情報が記述されている
ランキング(rankings)は次の8種類
- bp
- rank
- quest
- tower
- tower_red
- tower_greem
- tower_blue
- tower_yellow

いずれも配列で、先頭ほど上位とされる。
bpとrankは50位までのランキング情報、それ以外は20位までのランキング情報がある。

`player_info`にはプレイヤー情報が詳細に記述されている
ランキングに登場した全てのプレイヤー情報が網羅されている

```json
{
    "datetime": "2025-02-20T06:32:49",
    "datatype": "player_ranking",
    "world_id": 1099,
    "data": {
        "world_id": 1099,
        "rankings": {
            "bp": [
                {
                    "id": 679520283099,
                    "name": "Yama ",
                    "bp": 1187954998
                },
                {
                    "id": 293160749099,
                    "name": "moka珈琲",
                    "bp": 957186736
                }
            ],
            "rank": [
                {
                    "id": 293160749099,
                    "name": "moka珈琲",
                    "rank": 601
                },
                {
                    "id": 807888550099,
                    "name": "　",
                    "rank": 590
                }
            ],
            "quest": [
                {
                    "id": 679520283099,
                    "name": "Yama ",
                    "quest_id": 1319
                },
                {
                    "id": 368864860099,
                    "name": "こばと",
                    "quest_id": 1197
                }
            ],
            "tower": [
                {
                    "id": 293160749099,
                    "name": "moka珈琲",
                    "tower_id": 1593
                },
                {
                    "id": 679520283099,
                    "name": "Yama ",
                    "tower_id": 1593
                }
            ],
            "tower_red": [
                {
                    "id": 293160749099,
                    "name": "moka珈琲",
                    "tower_id": 1079
                },
                {
                    "id": 368864860099,
                    "name": "こばと",
                    "tower_id": 1059
                }
            ],
            "tower_green": [
                {
                    "id": 679520283099,
                    "name": "Yama ",
                    "tower_id": 1148
                },
                {
                    "id": 293160749099,
                    "name": "moka珈琲",
                    "tower_id": 1129
                }
            ],
            "tower_blue": [
                {
                    "id": 679520283099,
                    "name": "Yama ",
                    "tower_id": 1099
                },
                {
                    "id": 807888550099,
                    "name": "　",
                    "tower_id": 1079
                }
            ],
            "tower_yellow": [
                {
                    "id": 293160749099,
                    "name": "moka珈琲",
                    "tower_id": 1077
                },
                {
                    "id": 807888550099,
                    "name": "　",
                    "tower_id": 949
                }
            ]
        },
        "player_info": {
            "679520283099": {
                "id": 679520283099,
                "name": "Yama ",
                "bp": 1187954998,
                "rank": 580,
                "quest_id": 1319,
                "tower_id": 1593,
                "icon_id": -9223372036854775735,
                "guild_id": 199652669099,
                "guild_name": "サリンジャー",
                "guild_join_time": 1727300186207,
                "guild_position": 5,
                "prev_legend_league_class": 2
            },
            "293160749099": {
                "id": 293160749099,
                "name": "moka珈琲",
                "bp": 957186736,
                "rank": 601,
                "quest_id": 1117,
                "tower_id": 1593,
                "icon_id": 105,
                "guild_id": 592017867099,
                "guild_name": "にゃんCAFE",
                "guild_join_time": 1739823693697,
                "guild_position": 3,
                "prev_legend_league_class": 1
            },
            "807888550099": {
                "id": 807888550099,
                "name": "　",
                "bp": 942363994,
                "rank": 590,
                "quest_id": 1063,
                "tower_id": 1399,
                "icon_id": -9223372036854775789,
                "guild_id": 482173199099,
                "guild_name": "黒魔女のお茶会",
                "guild_join_time": 1739828636852,
                "guild_position": 2,
                "prev_legend_league_class": 1
            },
            "368864860099": {
                "id": 368864860099,
                "name": "こばと",
                "bp": 893654067,
                "rank": 574,
                "quest_id": 1197,
                "tower_id": 1561,
                "icon_id": -9223372036854775740,
                "guild_id": 719463286099,
                "guild_name": "ウロボロス鎮魂歌",
                "guild_join_time": 1739828035492,
                "guild_position": 2,
                "prev_legend_league_class": 2
            }
        }
    }
}
```
