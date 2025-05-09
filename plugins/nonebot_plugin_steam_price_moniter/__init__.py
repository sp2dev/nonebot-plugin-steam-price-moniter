import nonebot
from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_localstore")

from .steammoniter import *
from .manager import *


__plugin_meta__ = PluginMetadata(
    name="Steam价格监控",
    description="自动检测Steam游戏的价格，并在有折扣时推送",
    usage="待定",
    type="application",
    homepage="",
)
