# About Anaume-app

[第2回 学力向上アプリコンテスト](https://www.gakuryokuup.com/) 応募作品  
タイトル: Anaume-app  
名目: 英文記憶補助アプリ  
テーマ: 穴埋め式の記憶法で効率的に学習!  
使用言語: HTML5, CSS, Javascript, jQuery(3.6.0), Python(3.7.2)  
フレームワーク: Django3.2.6

HerokuApp: [https://anaume-app.herokuapp.com/](https://anaume-app.herokuapp.com/)    

## ローカル環境での起動方法
```sh
git clone https://github.com/mongesan/Anaume-app
```
\EnglishApp上で
```sh
pip install -r requirements.txt
```
データベースのマイグレーション
```sh
python manage.py migrate
```
スーパーユーザーの作成
```sh
python manage.py createsuperuser
```
起動
```sh
python manage.py runserver
```
localhost:8000 からアクセスが可能になる

## 構造
