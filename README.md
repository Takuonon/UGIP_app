# RailSentry

## 概要

監視カメラの映像から**車椅子の線路への侵入・転落を検出する AI**を搭載した、Web アプリケーション**RailSentry**を開発しました。立入禁止領域を設定することで、そこに立ち入った車椅子を検出することができます。

## 概観

![Alt Text](overview.gif)

## 基本的な構成

![Alt Text](Flowchart.jpg)

## アプリの起動の仕方

以下の順番に従って実行して下さい

1. python3.10 の仮想環境を作って立ち上げる

python3.8 ~ 3.10 で仮想環境を作ってください。これ以外のバージョンだとモジュールをインストールする際にエラーが発生してしまします。(python3.10 で動作確認済み)参考に自身の mac 上のコマンドを添付します。必要であれば、python3.10 がインストールすることを忘れないでください。[Python3.10.11 のダウンロードリンク](https://www.python.org/downloads/release/python-31011/)

```
$ python3.10 -m venv env_Railway
$ source env_Railway/bin/activate
```

2. 必要モジュールをインストールする

```
make install
```

することで必要モジュールを requirements.txt からダウンロード可能です。

3. 必要ファイルをインストールする

アプリを動作させる上で必要な best.pt、yolo4.weights はレポジトリに含まれていません。

```
make download
```

で適切な階層にダウンロード可能です。
もし上のコードで正しく動作しない場合は、以下のリンクから直接ダウンロードしてください。

- https://drive.google.com/drive/folders/1MheAP7o6INpj1pKUrp8CCwCZXJecN9ZQ?usp=sharing

その際は

- weights_folder/best.pt
- yolo/yolov4.weights

となるようにそれぞれ配置して下さい。

4. ローカル環境でアプリを立ち上げる

以下のコマンドでローカルホストが立ち上がります。

```
make run
```
