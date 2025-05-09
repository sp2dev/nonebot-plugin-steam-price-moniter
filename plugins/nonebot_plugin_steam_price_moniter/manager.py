from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import nonebot_plugin_localstore as store

appid_list = []
data_dir = store.get_plugin_data_dir()

addappid = on_command("add")
delappid = on_command("del")

@addappid.handle()
async def handleadd(args: Message = CommandArg()):
    appid = args.extract_plain_text()
    if appid in appid_list:
        await addappid.finish(f"{appid} 已存在")
    else:
        appid_list.append(appid)
        await addappid.finish(f"添加 {appid} 成功，目前名单为 {appid_list}")

@delappid.handle()
async def handledel(args: Message = CommandArg()):
    appid = args.extract_plain_text()
    if appid in appid_list:
        appid_list.remove(appid)
        await delappid.finish(f"删除成功，目前名单为 {appid_list}")
    else:
        await delappid.finish(f"删除失败，{appid} 不在名单中")
