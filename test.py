import asyncio
import aiosqlite

# Ma'lumotlar bazasi fayli
ORDER_DB = "database/orders.db"

async def add_service(service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif):
    async with aiosqlite.connect(ORDER_DB) as db:
        await db.execute("""
        INSERT OR IGNORE INTO services (
            service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif))
        await db.commit()

async def insert_all_services():
    xizmatlar = {
        "🔵Telegram": {
            "👍👎 Reaksiya": [
                {"service": 74, "name": "ijobiy Reaksiya [ Aralash 👍😅🎉🔥🥰👏❤️ ]"},
                {"service": 86, "name": "🎉 Reaksiya"},
                {"service": 84, "name": "🤩 Reaksiya"},
                {"service": 82, "name": "🔥 Reaksiya"},
                {"service": 950, "name": "🤝 Reaksiya"},
                {"service": 949, "name": "🍓 Reaksiya"},
                {"service": 75, "name": "Salbiy Reaksiya [ Aralash 👎😁😢💩🤮🤢 ]"},
                {"service": 81, "name": "👎 Reaksiya"},
                {"service": 1056, "name": "⚡ Reaksiya"},
                {"service": 1054, "name": "💔 Reaksiya"},
                {"service": 80, "name": "👍 Reaksiya"},
                {"service": 83, "name": "❤️ Reaksiya"},
                {"service": 88, "name": "😁 Reaksiya"},
                {"service": 912, "name": "💯 Reaksiya"}
            ],
            "👁 Ko'rishlar": [
                {"service": 102, "name": "👁 Prosmotir"},
                {"service": 105, "name": "📖 Istoriya ko'rish"}
            ],
            "👤 Obunachilar": [
                {"service": 27, "name": "👤 Obunachi ARZON (BOT)"},
                {"service": 22, "name": "👤 Obunachi(♻️R60) kafolat"},
                {"service": 41, "name": "👤 Obunachi ⚡Super Tezkor(♻️R30 kunlik)"},
                {"service": 42, "name": "👤 Obunachi (♻️R30) kafolat ⚡"},
                {"service": 14, "name": "👤 Obunachi 🔥 VIP BEZMINUS 🔥"},
                {"service": 3, "name": "👤 Obunachi (♻️R90) kafolat ⚡"},
                {"service": 821, "name": "👤 Obunachi 🇨🇳Xitoy (⛔BEZMINUS)"},
                {"service": 15, "name": "👤 Obunachi 1 yil Kafolatlangan (⛔BEZMINUS)"},
                {"service": 916, "name": "🇺🇿 O'zbek obunachi "},
                {"service": 974, "name": "🇺🇿 TG O‘zbek Obunachi [ Aktiv ] 🔥"},
                {"service": 32, "name": "👤 Obunachi (👁 Online 100% guruh uchun 🚀🚀🚀)"}
            ],
            "🤖 Bot uchun": [
                {"service": 1175, "name": "🤖Bot uchun Start (arzon)"},
                {"service": 1227, "name": "🤖 Arzon"},
                {"service": 1180, "name": "🇮🇱 Isroildan startlar"},
                {"service": 1181, "name": "🤖 Oddiy"},
                {"service": 1174, "name": "🇸🇦 Arablardan startlar"},
                {"service": 1177, "name": "🇺🇸 Aqishdan startlar"},
                {"service": 1178, "name": "🇨🇳 Xitoydan startlar"},
                {"service": 1175, "name": "🇮🇳 Hindistondan startlar"},
                {"service": 1182, "name": "🇩🇪 Germaniyadan startlar"},
                {"service": 1183, "name": "🇺🇦 Ukrainada startlar"},
                {"service": 1293, "name": "🇺🇿 O'zbekiston jonli / Referal"}
            ],
            "📊 So'rovnoma": [
                {"service": 106, "name": "📊 Ovoz so'rovnoma"}
            ],
            "💬 Izohlar": [
                {"service": 108, "name": "✉️ Izohlar +"}
            ],
            "🔁 Ulashish": [
                {"service": 110, "name": "🔁 Ulashishlar"}
            ],
            "📢 Boost ovoz": [
                {"service": 111, "name": "📢 BOOST OVOZ (hikoya)"}
            ]
        },
        "🔴Instagram": {
            "👤 Obunachi (✅ Kafolatli)": [
                {"service": 206, "name": "👤 Obunachi (✅ Kafolatli)"},
                {"service": 230, "name": "🔥Haqiqiy 👤 Obunachilar "}
            ],
            "🎥 Video Ko‘rishlar": [
                {"service": 207, "name": "🎥 Video Ko‘rishlar"}
            ],
            "❤️ Like": [
                {"service": 208, "name": "❤️ Like"}
            ],
            "👁 Ko‘rish (live video)": [
                {"service": 209, "name": "👁 Ko‘rish (live video)"}
            ],
            "👁 Stories Prosmotr": [
                {"service": 210, "name": "👁 Stories Prosmotr"}
            ],
            "🚀 Ulashish / 💾 Saxranit": [
                {"service": 211, "name": "🚀 Ulashish / 💾 Saxranit"}
            ]
        },
        "🟡You Tube": {
            "👁 Ko'rishlar": [
                {"service": 301, "name": "👁 Ko'rishlar"}
            ],
            "👍 Like": [
                {"service": 302, "name": "👍 Like"}
            ],
            "👤 Obunachilar": [
                {"service": 303, "name": "👤 Obunachilar"}
            ],
            "👁 Live ko'rishlar": [
                {"service": 304, "name": "👁 Live ko'rishlar"}
            ]
        },
        "⚫️Tik Tok": {
            "👁 Ko'rishlar": [
                {"service": 401, "name": "👁 Ko'rishlar"}
            ],
            "👍 Like": [
                {"service": 402, "name": "👍 Like"}
            ],
            "👤 Obunachilar": [
                {"service": 403, "name": "👤 Obunachilar"}
            ]
        },
        "Bepul xizmatlar": {}
    }

    for categoria_nomi, bolimlar in xizmatlar.items():
        for bolim_nomi, xizmat_list in bolimlar.items():
            for xizmat in xizmat_list:
                service_id = xizmat.get("service")
                xizmat_nomi = xizmat.get("name")
                narxi = 0  # Narxi keltirilmagan, shuning uchun 0
                tavsif = ""  # Tavsif keltirilmagan, shuning uchun bo'sh
                await add_service(service_id, categoria_nomi, bolim_nomi, xizmat_nomi, narxi, tavsif)
                print(f"Qo'shildi: {categoria_nomi} -> {bolim_nomi} -> {xizmat_nomi}")

# Kodni ishga tushirish
asyncio.run(insert_all_services())