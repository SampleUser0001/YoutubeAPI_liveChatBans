# YoutubeAPI_liveChatBans

### Request

[ここ](https://developers.google.cn/youtube/v3/live/docs/liveChatBans#resource-representation)から取得。

``` json
{
  "kind": "youtube#liveChatBan",
  "etag": etag, # videoの実行結果 : video['items'][0]['etag']
  "id": string, # videoの実行結果 : video['items'][0]['id']
  "snippet": {
    "liveChatId": string, # video['items'][0]['liveStreamingDetails']['activeLiveChatId']
    "type": string,       # 'permanent' or 'temporary'
    "banDurationSeconds": unsigned long, # typeが'temporary'のときだけ有効。デフォルトは300。
    "bannedUserDetails": {
      "channelId": string
    }
  }
}
```

#### video liveStreamingDetails

``` json

```

## 参考

- [ドキュメント:liveChatBans](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.liveChatBans.html)
- [LiveChatBans:insert :YoutubeAPI](https://developers.google.cn/youtube/v3/live/docs/liveChatBans/insert)
