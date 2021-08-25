# About Anaume-app

[第2回 学力向上アプリコンテスト](https://www.gakuryokuup.com/) 応募作品  
タイトル: Anaume-app  

名目: 英文記憶補助アプリ  
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
ホーム画面からアカウントを作成して、最初の英文帳を作成して下さい。

[comment]: <> (## 開発後記)

[comment]: <> (このアプリの開発には2か月以上を要し、実用的なアプリを目指して開発することの大変さを学びました。)

[comment]: <> (経験の浅いWebアプリ開発が難しいのはもちろん、 デザインと機能面の両方を考えながら一人で開発をすると、どうしても手が回らず実装できない部分が出てしまいます。  )

[comment]: <> (同時に、世に出回っている便利なツールには、多くの人の努力があることを実感しました。)

[comment]: <> (しかし、既に存在するアプリと同じ完成度のものを  )

[comment]: <> (考案・開発: 坂本 俊一朗 &#40;早稲田大学高等学院 1年&#41;)