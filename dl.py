import os
import json
import time

import asyncio
import aiohttp

import config

header = {"User-Agent": f"Lithum AIG/{config.version} (Fediverse @sonyakun@misskey.io)"}


async def get_artifact_img(id: str = "15034", name_ja: str = "残響の森で囁かれる夜話"):
    if not os.path.exists(f"./lib/ArtifacterImageGen/Artifact/{name_ja}"):
        os.mkdir(f"./lib/ArtifacterImageGen/Artifact/{name_ja}")
    fname = {"5": "clock", "3": "hat", "1": "cup", "4": "flower", "2": "wing"}
    for i in range(5):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"https://enka.network/ui/UI_RelicIcon_{id}_{i + 1}.png"
            ) as rj:
                if rj.status == 200:
                    f = open(
                        f"./lib/ArtifacterImageGen/Artifact/{name_ja}/{fname[str(i + 1)]}.png",
                        mode="wb",
                    )
                    f.write(await rj.read())
                    print("file saved to: " + f"./lib/ArtifacterImageGen/Artifact/{name_ja}/{fname[str(i + 1)]}.png")
                    f.close()
        await asyncio.sleep(1.5)


async def get_character_img(name: str, name_ja: str, charaId: str):
    if not os.path.exists(f"./lib/ArtifacterImageGen/character/{name_ja}"):
        os.mkdir(f"./lib/ArtifacterImageGen/character/{name_ja}")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url="https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store/characters.json"
        ) as rj:
            if rj.status == 200:
                f = open("./lib/ArtifacterImageGen/cache/characters.json", mode="wb")
                f.write(await rj.read())
                f.close()
                with open(
                    "./lib/ArtifacterImageGen/cache/characters.json",
                    "r",
                    encoding="utf-8",
                ) as f:
                    rj = json.load(f)
        async with session.get(
            url=f"https://enka.network/ui/UI_Gacha_AvatarImg_{name}.png"
        ) as resp:
            print(
                "("
                + "Banner"
                + ") url: "
                + f"https://enka.network/ui/UI_Gacha_AvatarImg_{name}.png"
            )
            if resp.status == 200:
                f = open(
                    f"./lib/ArtifacterImageGen/character/{name_ja}/avatar.png",
                    mode="wb",
                )
                f.write(await resp.read())
                print("file saved to: " + f"./lib/ArtifacterImageGen/character/{name_ja}/avatar.png")
                f.close()
        lp = 1
        await asyncio.sleep(1.5)
        for const in rj[charaId]["Consts"]:
            url = f"https://enka.network/ui/{const}.png"
            async with session.get(url=url) as resp:
                print("url: " + url)
                if resp.status == 200:
                    f = open(
                        f"./lib/ArtifacterImageGen/character/{name_ja}/{str(lp)}.png",
                        mode="wb",
                    )
                    f.write(await resp.read())
                    print("file saved to: " + f"./lib/ArtifacterImageGen/character/{name_ja}/{str(lp)}.png")
                    f.close()
                else:
                    print(resp.status)
            lp = lp + 1
            await asyncio.sleep(1.5)
        for skill in rj[charaId]["SkillOrder"]:
            if rj[charaId]["Skills"][str(skill)].startswith("Skill_A"):
                fname = "通常"
            elif rj[charaId]["Skills"][str(skill)].startswith("Skill_S"):
                fname = "スキル"
            elif rj[charaId]["Skills"][str(skill)].startswith("Skill_E"):
                fname = "爆発"
            url = "https://enka.network/ui/{}.png".format(
                rj[charaId]["Skills"][str(skill)]
            )
            print("({}) url: ".format(fname) + url)
            async with session.get(url=url) as resp:
                if resp.status == 200:
                    f = open(
                        f"./lib/ArtifacterImageGen/character/{name_ja}/{fname}.png",
                        mode="wb",
                    )
                    f.write(await resp.read())
                    print("file saved to: " + f"./lib/ArtifacterImageGen/character/{name_ja}/{fname}.png")
                    f.close()
                else:
                    print(resp.status)
                await asyncio.sleep(1.5)


def get_artifact_img_latest():
    asyncio.run(get_artifact_img(id="15030", name_ja="花海甘露の光"))
    asyncio.run(get_artifact_img(id="15029", name_ja="水仙の夢"))
    time.sleep(5)
    asyncio.run(get_artifact_img(id="15031", name_ja="ファントムハンター"))
    asyncio.run(get_artifact_img(id="15032", name_ja="黄金の劇団"))
    time.sleep(5)
    asyncio.run(get_artifact_img(id="15033", name_ja="在りし日の歌"))
    asyncio.run(get_artifact_img())

def get_chara_img_latest():
    asyncio.run(get_character_img(name="Baizhuer", name_ja="白朮", charaId="10000082"))
    asyncio.run(get_character_img(name="Kaveh", name_ja="カーヴェ", charaId="10000081"))
    time.sleep(5)
    asyncio.run(get_character_img(name="Momoka", name_ja="綺良々", charaId="10000061"))
    asyncio.run(
        get_character_img(name="PlayerBoy", name_ja="空(水)", charaId="10000005-503")
    )
    time.sleep(5)
    asyncio.run(
        get_character_img(name="PlayerGirl", name_ja="蛍(水)", charaId="10000005-503")
    )
    asyncio.run(
        get_character_img(name="Linette", name_ja="リネット", charaId="10000083")
    )
    time.sleep(5)
    asyncio.run(get_character_img(name="Liney", name_ja="リネ", charaId="10000084"))
    asyncio.run(
        get_character_img(name="Freminet", name_ja="フレミネ", charaId="10000085")
    )
    time.sleep(5)
    asyncio.run(
        get_character_img(name="Wriothesley", name_ja="リオセスリ", charaId="10000086")
    )
    asyncio.run(
        get_character_img(
            name="Neuvillette", name_ja="ヌヴィレット", charaId="10000087"
        )
    )
    time.sleep(5)
    asyncio.run(
        get_character_img(name="Charlotte", name_ja="シャルロット", charaId="10000088")
    )
    asyncio.run(
        get_character_img(name="Furina", name_ja="フリーナ", charaId="10000089")
    )
    time.sleep(5)
    asyncio.run(
        get_character_img(name="Chevreuse", name_ja="シュヴルーズ", charaId="10000090")
    )
    asyncio.run(get_character_img(name="Navia", name_ja="ナヴィア", charaId="10000091"))
    time.sleep(5)
    asyncio.run(get_character_img(name="Gaming", name_ja="嘉明", charaId="10000092"))
    asyncio.run(get_character_img(name="Liuyun", name_ja="閑雲", charaId="10000093"))


get_chara_img_latest()
time.sleep(10)
get_artifact_img_latest()
