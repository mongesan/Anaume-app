# About Anaume-App

[第2回 学力向上アプリコンテスト](https://www.gakuryokuup.com/) 応募作品  
タイトル: Anaume-App  

名目: 英文学習補助アプリ  
テーマ: 穴埋め式の記憶法を使った効率的暗記  
使用言語: HTML5, CSS, Javascript, jQuery(3.6.0), Python(3.7.2)  
フレームワーク: Django3.2.6  
CSS補助: Bootstrap5

HerokuApp: [https://anaume-app.herokuapp.com/](https://anaume-app.herokuapp.com/)    

## ローカル環境での起動方法
```sh
git clone https://github.com/mongesan/Anaume-app
```
pythonのモジュールをまとめてインストール
```sh
pip install -r requirements.txt
```
以後、ホームディレクトリにて実行  
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
localhost:8000 からのアクセスが可能になります

## 使い方
参考動画  
[https://www.youtube.com/watch?v=MjxqplKpwmQ](https://www.youtube.com/watch?v=MjxqplKpwmQ)


考案・開発: 坂本 俊一朗 (早稲田大学高等学院 1年)
