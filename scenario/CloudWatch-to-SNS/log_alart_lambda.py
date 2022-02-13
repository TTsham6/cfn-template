import base64
import json
import zlib
import os
import boto3
import datetime

print('Loading function')


def lambda_handler(event, context):
    """
    AWS Lambdaのハンドラ

    Parameters
    ----------
    event : str
        Subscription filterのイベント(エンコード済み)

    context : 
        コンテキスト
    """

    # イベント取得
    data = zlib.decompress(base64.b64decode(
        event['awslogs']['data']), 16 + zlib.MAX_WBITS)
    data_json = json.loads(data)

    log_event_list = data_json['logEvents']
    log_group_name = data_json['logGroup']
    log_file_name = data_json['logStream']

    for log_event in log_event_list:
        # 件名
        subject_msg = '【Alert】' + log_group_name + '_' + log_file_name

        # 本文
        log_group_msg = 'ロググループ：' + '\n' + log_group_name
        log_file_msg = 'ログファイル名：' + '\n' + log_file_name
        time_msg = '発生時刻：' + '\n' + convert_unix_to_jst(log_event['timestamp'])
        log_msg = 'ログ内容' + '\n' + log_event['message']
        msg = log_group_msg + '\n\n' + \
            log_file_msg + '\n\n' + \
            time_msg + '\n\n' + \
            log_msg

        # SNSへ通知
        try:
            sns = boto3.client('sns')

            sns.publish(
                TopicArn=os.environ['SNS_TOPIC_ARN'],
                Subject=subject_msg,
                Message=msg
            )

        except Exception as e:
            print(e)


def convert_unix_to_jst(timestamp_unix):
    """
    UNIXをJSTに変換する

    Parameters
    ----------
    timestamp_unix : int
        UNIX時刻のタイムスタンプ

    Returns
    -------
    datetime_jst : str
        JST時刻の文字列 YYYY/mm/dd HH:MM:SS
    """
    datetime_utc = timestamp_unix / 1000.0
    datetime_utc = datetime.datetime.fromtimestamp(datetime_utc)  # タイムスタンプ読み込み
    datetime_jst = datetime_utc + datetime.timedelta(hours=9)  # JSTに変換
    datetime_jst = datetime_jst.strftime('%Y/%m/%d %H:%M:%S')  # 文字列に変換
    return datetime_jst
