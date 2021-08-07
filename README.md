# YoutubeAPI_liveChatBans

## Request

[ここ](https://developers.google.cn/youtube/v3/live/docs/liveChatBans#resource-representation)から取得。


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

## 参考

- [ドキュメント:liveChatBans](https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.liveChatBans.html)
- [LiveChatBans:insert :YoutubeAPI](https://developers.google.cn/youtube/v3/live/docs/liveChatBans/insert)
