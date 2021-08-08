# YoutubeAPI_liveChatBans

環境設定ファイルで指定したチャンネルIDを「非表示のユーザー」に登録する。

## 実行環境

- Ubuntu 20.04.2で確認。
- Docker, docker-composeインストール済み。

## 実行準備

1. YouTube Data APIがOAuth 2.0 クライアント認証で実行できる状態にする。
    - 下記2ファイルを配置。
        - ```app/config/client_secret.json```
            - Google Cloud Platformの認証情報-OAuth2.0クライアントIDから取得したファイル
        - ```app/config/app.py-oauth2.json```
            - 上記のファイルを認証した際に生成されるファイル
    - 参考：[GoogleAPI_OAuth_init_setting:SampleUser0001:Github](https://github.com/SampleUser0001/GoogleAPI_OAuth_init_setting)
2. ```app/sample.env``` をコピーし、```app/.env```ファイルを作成する。
3. ```app/.env```ファイルを編集する。
    - video_id
        - 動画ID。
            - 「https://www.youtube.com/watch?v=fEvM-OUbaKs」などのURLの「fEvM-OUbaKs」の部分を記載。
            - 配信中の動画のみ指定可能。
    - channel_id
        - BANするユーザのチャンネルID。
            - BAN対象のユーザのチャンネルURLが「https://www.youtube.com/channel/UC_x5XG1OV2P6uZZ5FSM9Ttw」であれば、「UC_x5XG1OV2P6uZZ5FSM9Ttw」を指定。
            - 本来は[GetYoutubeLiveComment](https://github.com/SampleUser0001/GetYoutubeLiveComment)などで取得した値を使用するが、このツールはBANできることを確認するためのサンプルなので、envファイルから取得。

## 実行

``` sh
docker-compose up
```

## 参考

### リンク

- [ドキュメント:liveChatBans](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.liveChatBans.html)
- [LiveChatBans:insert :YoutubeAPI](https://developers.google.cn/youtube/v3/live/docs/liveChatBans/insert)

### Request

下記をliveChatBansの引数に渡して実行する。  
[ドキュメント:liveChatBans](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.liveChatBans.html)から取得。

``` json
{
  "snippet": {
    "liveChatId": string, # video['items'][0]['liveStreamingDetails']['activeLiveChatId']
    "type": string,       # 'PERMANENT' or 'TEMPORARY'
    "banDurationSeconds": unsigned long, # typeが'TEMPORARY'のときだけ有効。デフォルトは300。
    "bannedUserDetails": {
      "channelId": string
    }
  }
}
```
