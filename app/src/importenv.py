# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from enum import Enum

class ImportEnvKeyEnum(Enum):
  """ .envファイルのキーを書く """
  VIDEO_ID = 'video_id'
  CHANNEL_ID = 'channel_id'

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENV_DIC = {}
# ImportEnvKeyEnumの値を書く
ENV_KEYS = [ \
  ImportEnvKeyEnum.VIDEO_ID.value, \
  ImportEnvKeyEnum.CHANNEL_ID.value]

for key in ENV_KEYS:
  ENV_DIC[key] = os.environ.get(key)