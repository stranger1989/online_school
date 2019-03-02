# 環境

- Python: 3.7.2
- Django: 2.1.5
- DB:
  - Postgresql (Heroku Production)
  - SQlite (Local)

***

# 仕様

- レッスンジャンルの追加はadmin画面から追加
- 無料時間・割引ルールの変更もadmin画面から変更

***

# 本番ページ

- [本番トップページURL](https://web-system.herokuapp.com/onlineschool/)
- [本番アドミンページURL](https://web-system.herokuapp.com/admin/)

***

# DB設計

## Userテーブル
|Column|Type|Options|
|------|----|-------|
|name|string|null: false|
|sex|string|null: false|
|age|integer|null: false|

### Association
- has_many :lessonrecord


## Lessonテーブル
|Column|Type|Options|
|------|----|-------|
|name|string|null: false|
|basic_charge|integer|null: false|
|pay_per_charge|integer|null: false|
|free_time|integer|null: false|

### Association
- has_many :lessonrecord
- has_many :discount


## Lessonrecordテーブル
|Column|Type|Options|
|------|----|-------|
|user_name|integer|null: false, foreign_key: true|
|lesson_name|integer|null: false, foreign_key: true|
|lesson_date|date|null: false|
|lesson_hour|integer|null: false|
|lesson_charge|integer|null: false|


### Association
- belongs_to :user
- belongs_to :lesson


## Discountテーブル
|Column|Type|Options|
|------|----|-------|
|lesson_name|integer|null: false, foreign_key: true|
|limited_hour|integer|null: false|
|discount_price|integer|null: false|

### Association
- belongs_to :lesson
