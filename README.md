# RailSentry

## 概要

監視カメラの映像から**車椅子の線路への侵入・転落を検出する AI**を搭載した、Web アプリケーション**RailSentry**を開発しました。立入禁止領域を設定することで、そこに立ち入った車椅子を検出することができます。

## 概観

![Alt Text](overview.gif)

## 基本的な構成

![Alt Text](Flowchart.jpg)

## その他

### 必要ファイルについて

アプリを動作させる上で必要な best.pt、yolo4.weights はレポジトリに含まれていません。

```
make download
```

で適切な階層にダウンロード可能です。
もし動作しない場合はは以下のリンクから直接ダウンロードしてください。

- https://drive.google.com/drive/folders/1MheAP7o6INpj1pKUrp8CCwCZXJecN9ZQ?usp=sharing

また、

- weights_folder/best.pt
- yolo/yolov4.weights

となるようにそれぞれ配置して下さい。

### 必要モジュールについて

仮想環境中で

```
make install
```

することで必要モジュールを requirements.txt からダウンロード可能です。

### アプリの実行について

アプリを実行する際は

```
make start
```

で localhost が立ちます
