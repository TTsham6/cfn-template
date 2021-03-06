# CloudWathのログを検知してSNSからメール通知するサンプル

## フロー
1. EC2がロググループにログを送信
2. CloudWatchサブスクリプションフィルターがLambda関数を起動
3. Lambdaがログのメッセージを整形し、SNSに送信
4. SNSがメール通知

## ファイル構成
```
CloudWatch-to-SNS
    - alarm-email-flow.yml // CFnテンプレート
    - AmazonCloudWatch-AmazonLinux.json // CloudWatchエージェント設定用ドキュメント 
    - log_alart_lambda.py  // Lambda関数 
```

## 構成
![template1-designer](https://user-images.githubusercontent.com/37510144/153736741-1d4d4bfc-0993-4bb9-8eec-ed09667c2e06.png)
<br>

## スタック作成方法

### 1. log_alart_lambda.pyをZIP化してS3バケットにアップロードする

### 2. alarm-email-flow.ymlでスタックを作成する
```
パラメータ
・LambdaBucket：ZIPファイルを格納したS3バケット名
・PythonZip：Zipファイル名
・EmailAddress：SNSから送られるEメールアドレス
```

### 3. SNSからメールが送られてくるので、承認する
<br>

## ログ送信方法

### 1. EC2インスタンスにCloudWatch Agentをインストール

### 2. /var/log/messagesをamazonlinux-message.logロググループに送信するようにAgentを設定する
```
AmazonCloudWatch-AmazonLinux.jsonを利用してSSM経由で設定できます
```

## メールサンプル
### 件名
```
【Alert】amazonlinux-message.log_i-********************
```
### メール本文
```
ロググループ：
amazonlinux-message.log

ログファイル名：
log_i-********************

発生時刻：
2022-02-13 11:00:00

ログ内容
Feb 13 11:00:00 amazon-***** Error: error
```

### 参考
https://zenn.dev/supersatton/articles/a2110223767a2c
