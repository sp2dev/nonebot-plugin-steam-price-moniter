from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import httpx
import asyncio

from .manager import appid_list


checkappid = on_command("check")
checkall = on_command("checkall")

async def request_game_info(appid):
    async with httpx.AsyncClient(verify=False) as client:  # 如果验证证书会报SSL错误（至少在我这边是这样）
        requesturl = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=cn"
        response = await client.get(requesturl)
        game_info = response.json()
        return game_info

async def check_game(appid):
    game_info = await request_game_info(appid)
    is_available = game_info[str(appid)]["success"]
    if is_available:  # 检测可用性
        game_data = game_info[str(appid)]["data"]
        is_free = game_data["is_free"]
        game_name = game_data["name"]
        if is_free:  # 检测免费游戏
            price = False
            return is_available, game_name, price, None, None
        elif not is_free:  # 检测付费游戏
            game_price = game_data["price_overview"]
            final_price = game_price["final_formatted"]
            if game_price["discount_percent"] != 0:  # 检测折扣
                initial_price = game_price["initial_formatted"]
                discount_percent = game_price["discount_percent"]
                return is_available, game_name, final_price, initial_price, discount_percent
            return is_available, game_name, final_price, None, None
    elif not is_available:
           return is_available, None, None, None, None



async def send_message(command, game_name, price, initial_price, discount_percent):
    if price == False:
        await command.send(f"{game_name} 是免费游戏")
    else:
        if discount_percent is None:
            await command.send(f"{game_name} 的价格为 {price}")
        else:
            await command.send(f"原价为 {initial_price} 的 {game_name} 以 {discount_percent}% 的折扣打折，折后价为 {price}")


@checkappid.handle()
async def handlecheck(args: Message = CommandArg()):
    appid = args.extract_plain_text()
    is_available, game_name, price, initial_price, discount_percent = await check_game(appid)  # type: ignore
    if is_available:
        await send_message(checkappid, game_name, price, initial_price, discount_percent)
    elif not is_available:
        await checkappid.send(f"指定的 appid 不可用")


@checkall.handle()
async def handlecheckall():
    for appid in appid_list:
        is_available, game_name, price, initial_price, discount_percent = await check_game(appid)  # type: ignore
        if is_available:
            await send_message(checkappid, game_name, price, initial_price, discount_percent)
        elif not is_available:
            await checkappid.send(f"指定的 appid 不可用")


