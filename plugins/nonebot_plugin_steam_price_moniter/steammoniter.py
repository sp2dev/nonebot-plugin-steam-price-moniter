from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import httpx
import asyncio

from .manager import appid_list


checkappid = on_command("check")
checkall = on_command("checkall")

async def request_game_info(appid):
    async with httpx.AsyncClient(verify=False) as client: # 如果验证证书会报SSL错误（至少在我这边是这样）
        requesturl = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        response = await client.get(requesturl)
        game_info = response.json()
        is_aviliable = game_info[str(appid)]["success"]
        if is_aviliable:  # 检测可用性
            game_data = game_info[str(appid)]["data"]
            is_free = game_data["is_free"]
            game_name = game_data["name"]
            if is_free:  # 检测免费游戏
                price = "free"
                return is_aviliable, game_name, price, None, None
            elif not is_free:  # 检测付费游戏
                game_price = game_data["price_overview"]
                price = game_price["final_formatted"]
                if game_price["discount_percent"] != 0 :  # 检测折扣
                    init_price = game_price["initial_formatted"]
                    discount = game_price["discount_percent"]
                    return is_aviliable, game_name, price, init_price, discount
                return is_aviliable, game_name, price, None, None
        elif not is_aviliable:
            return is_aviliable, None, None, None, None



@checkappid.handle()
async def handlecheck(args: Message = CommandArg()):
    appid = args.extract_plain_text()
    is_aviliable, game_name, price, init_price, discount = await request_game_info(appid)  # 异步调用
    if is_aviliable:
        if price == "free":
            await checkappid.send(f"{game_name} 是免费游戏")
        else:
            if discount is None:
                await checkappid.send(f"{game_name} 的价格为 {price}")
            else:
                await checkappid.send(f"原价为 {init_price} 的 {game_name} 以 {discount}% 的折扣打折，折后价为 {price}")
    elif not is_aviliable:
        await checkappid.send(f"指定的 appid 不可用")


@checkall.handle()
async def handlecheckall():
    for appid in appid_list:
        is_aviliable, game_name, price, init_price, discount = await request_game_info(appid)  # 在循环中调用异步函数
        if is_aviliable:
            if price == "free":
                await checkappid.send(f"{game_name} 是免费游戏")
            else:
                if discount is None:
                    await checkappid.send(f"{game_name} 的价格为 {price}")
                else:
                    await checkappid.send(f"原价为 {init_price} 的 {game_name} 以 {discount}% 的折扣打折，折后价为 {price}")
        elif not is_aviliable:
            await checkappid.send(f"指定的 appid 不可用")
