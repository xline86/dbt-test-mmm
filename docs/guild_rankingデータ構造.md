# guild_ranking データ構造

`data/guild_ranking`にはプレイヤーのランキング情報が記述されている
ランキング(rankings)は次の3種類
- bp
- level
- stock

いずれも配列で、先頭ほど上位とされる。
全て20位までのランキング情報がある。

`guild_info`にはギルド情報が詳細に記述されている
ランキングに登場した全てのギルド情報が網羅されている

```json
{
    "datetime": "2025-02-20T06:32:49",
    "datatype": "guild_ranking",
    "world_id": 1099,
    "data": {
        "world_id": 1099,
        "rankings": {
            "bp": [
                {
                    "id": 394114239099,
                    "name": "REsKend",
                    "bp": 11461711536
                },
                {
                    "id": 719463286099,
                    "name": "ウロボロス鎮魂歌",
                    "bp": 10458333847
                }
            ],
            "level": [
                {
                    "id": 394114239099,
                    "name": "REsKend",
                    "level": 20
                },
                {
                    "id": 494634944099,
                    "name": "凛として時雨",
                    "stock": 3640
                },
            ],
            "stock": [
                {
                    "id": 494634944099,
                    "name": "凛として時雨",
                    "stock": 3640
                },
                {
                    "id": 196765134099,
                    "name": "メメ温泉99番地",
                    "stock": 2690
                }
            ]
        },
        "guild_info": {
            "394114239099": {
                "id": 394114239099,
                "name": "REsKend",
                "bp": 11461711536,
                "level": 20,
                "stock": 1030,
                "exp": 2716300,
                "num_members": 45,
                "leader_id": 560049957099,
                "leader_name": "48のシバ",
                "policy": 0,
                "description": "☆加入希望者は個チャお願いします☆ 一緒に戦ってくれる仲間を募集中です！",
                "free_join": false,
                "bp_requirement": 50000000
            },
            "719463286099": {
                "id": 719463286099,
                "name": "ウロボロス鎮魂歌",
                "bp": 10458333847,
                "level": 20,
                "stock": 1430,
                "exp": 2587180,
                "num_members": 50,
                "leader_id": 636854845099,
                "leader_name": "貌",
                "policy": 0,
                "description": "モチベ高くアクティブな方なら初心者大歓迎です！\n2日間インない方は除名対象。\n検討される方は50埋まっててもまずメッセを",
                "free_join": false,
                "bp_requirement": 500000
            },
            "494634944099": {
                "id": 494634944099,
                "name": "凛として時雨",
                "bp": 9600498152,
                "level": 20,
                "stock": 3640,
                "exp": 2680710,
                "num_members": 50,
                "leader_id": 887185644099,
                "leader_name": "澪燯",
                "policy": 0,
                "description": "よろしくお願いします(⁠◍⁠•⁠ᴗ⁠•⁠◍⁠)✿",
                "free_join": false,
                "bp_requirement": 77777777
            },
            "196765134099": {
                "id": 196765134099,
                "name": "メメ温泉99番地",
                "bp": 8678838469,
                "level": 20,
                "stock": 1980,
                "exp": 2676690,
                "num_members": 49,
                "leader_id": 866321964099,
                "leader_name": "創世メガネ",
                "policy": 0,
                "description": "温泉の聖地メメ街のお宿。理想の温泉地を求め今日もギルバト♪加入希望の方お気軽に個チャ下さいね！",
                "free_join": false,
                "bp_requirement": 46490
            }
        }
    }
}
```
