# -*- coding: utf-8 -*-
import json
import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from logging import getLogger, config, StreamHandler, DEBUG
import os

import sys
sys.path.append('./')
from logutil import LogUtil
from importenv import ImportEnvKeyEnum
import importenv as setting

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(PYTHON_APP_HOME + '/config/log_config.json')
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# OAuth認証キーファイル
CLIENT_SECRETS_FILE = PYTHON_APP_HOME + '/config/client_secret.json'
# OAuth認証結果ファイル
OAUTH_FILE = PYTHON_APP_HOME + '/config/app.py-oauth2.json'

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# 動画ID
VIDEO_ID = setting.ENV_DIC[ImportEnvKeyEnum.VIDEO_ID.value];
# BanするチャンネルID
CHANNEL_ID = setting.ENV_DIC[ImportEnvKeyEnum.CHANNEL_ID.value];

# youtubeapiインスタンス
youtube = None

def get_authenticated_service(oauth_file):
  """
  認証済みjsonファイルを使用して、YoutubeAPI接続インスタンスを取得する。
  
  Parameter
  ----
  oauth_file : string
    認証済みjsonファイルのファイルパス
  
  Return
  ----
  YoutubeAPI接続インスタンス
  """
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage(oauth_file)
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

def live_chat_ban(request):
  """
  指定したチャンネルIDのユーザをBANする。
  
  Parameter
  ----
  request : dict
    BAN実行のためのリクエスト情報
    
  Return
  ----
  None
    なし
  """
  youtube.liveChatBans().insert(
    part="snippet",
    body=request
  ).execute()

def get_video_info(video_id):
  """
  動画情報を取得する。
  
  Parameter
  ----
  video_id : string
    動画ID
  
  Return
  ----
  dict
    動画情報
  
  """
  return youtube.videos().list(
    part='liveStreamingDetails',
    id=video_id
  ).execute()

def convert_to_ban_request(live_chat_id, ban_channel_id):
  """
  liveChatBansの引数を生成する
  
  Parameter
  ----
  live_chat_ban : string
    チャットID
  ban_channel_id : string
    BAN対象のチャンネルID
    
  Return
  ----
  dict
    liveChatBansに渡す引数
  """

  return_dict = {}

  snippet = {}
  
  # https://www.googleapis.com/youtube/v3/liveChat/messagesで取得できる値
  bannedUserDetails = {}
  bannedUserDetails['channelId'] = ban_channel_id

  snippet['bannedUserDetails'] = bannedUserDetails
  snippet['liveChatId'] = live_chat_id
  # 指定したユーザを永続的に非表示にする。「非表示のユーザー」に登録される。
  snippet['type'] = 'PERMANENT'
  
  # 指定したユーザを一時的に非表示にする。banDurationSecondsで指定した秒数、投稿不可にする。
  # snippet['type'] = 'TEMPORARY'
  # snippet['banDurationSeconds'] = '30'
  
  return_dict['snippet'] = snippet
  return return_dict

if __name__ == '__main__':
  logger.info('Start')
  
  logger.info('video_id : %s' % VIDEO_ID)
  logger.info('ban channel_id : %s' % CHANNEL_ID)
  
  # Youtube接続インスタンス取得
  youtube = get_authenticated_service(OAUTH_FILE)
  video_info = get_video_info(VIDEO_ID)
  logger.debug(video_info)

  # BANリクエストの引数を生成する。  
  ban_request = convert_to_ban_request( \
    video_info['items'][0]['liveStreamingDetails']['activeLiveChatId'], \
    CHANNEL_ID)
  logger.debug(ban_request)
  
  # BAN実行
  live_chat_ban(ban_request)
  
  logger.info('Finish')
