# django-dify-flow-app

DIFYのフローを実行するDjangoアプリです。

## 前提条件

DIFY上で**インシデント分析.yml**を使ってインシデント分析フローを作成していること。

上記DIFYのフローは、インプットとして以下の4つのフィールドを与える構成になっています。

- category（カテゴリ）
- subcategory(サブカテゴリ）
- details（詳細内容）
- query(質問内容）

## 動作確認環境

- Python: 3.11.5
- Django: 5.1.1

## 起動手順

0. リポジトリのクローン or Download

   ```
   git clone https://github.com/sinjorjob/django-dify-flow-app.git
   ```


1. 仮想環境の作成と有効化
   ```
   python -m venv <仮想環境名>
   <仮想環境名>\scripts\activate
   ```

2. 依存関係のインストール
   ```
   pip install -r requirements.txt
   ```

3. プロジェクトディレクトリに移動
   ```
   cd pandasai-django-app\source
   ```

4. データベースのセットアップ
   ```
   python manage.py makemigrations dify_app
   python manage.py migrate
   ```

5. 管理者ユーザーの作成
   ```
   python manage.py createsuperuser
   ```

6. サーバーの起動
   ```
   python manage.py runserver
   ```

7. ブラウザで `http://127.0.0.1:8000/` にアクセスして動作確認

## 初期データの登録（カテゴリ、サブカテゴリ）

以下のコマンドを実行して 初期データを登録します：  

```
python manage.py load_initial_data
```

