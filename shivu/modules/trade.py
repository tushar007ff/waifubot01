from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient 
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultPhoto, InputTextMessageContent
from collections import Counter
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums
from shivu import db, collection, top_global_groups_collection, group_user_totals_collection, user_collection, user_totals_collection
from shivu import shivuu




pending_trades = {}


@shivuu.on_message(filters.command("trade"))
async def trade(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("𝙔𝙤𝙪 𝙣𝙚𝙚𝙙 𝙩𝙤 𝙧𝙚𝙥𝙡𝙮 𝙩𝙤 𝙖 𝙪𝙨𝙚𝙧'𝙨 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙩𝙤 𝙩𝙧𝙖𝙙𝙚 𝙖 𝙘𝙝𝙖𝙧𝙖𝙘𝙩𝙚𝙧!")
        return

    receiver_id = message.reply_to_message.from_user.id

    if sender_id == receiver_id:
        await message.reply_text("𝐘𝐨𝐮 𝐜𝐚𝐧'𝐭 𝐭𝐫𝐚𝐝𝐞 𝐚 𝐜𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫 𝐰𝐢𝐭𝐡 𝐲𝐨𝐮𝐫𝐬𝐞𝐥𝐟!")
        return

    if len(message.command) != 3:
        await message.reply_text("𝙔𝙤𝙪 𝙣𝙚𝙚𝙙 𝙩𝙤 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙩𝙬𝙤 𝙘𝙝𝙖𝙧𝙖𝙘𝙩𝙚𝙧 𝙄𝘿𝙨!")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    sender = await user_collection.find_one({'id': sender_id})
    receiver = await user_collection.find_one({'id': receiver_id})

    sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
    receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

    if not sender_character:
        await message.reply_text("𝗬𝗼𝘂 𝗱𝗼𝗻'𝘁 𝗵𝗮𝘃𝗲 𝘁𝗵𝗲 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘆𝗼𝘂'𝗿𝗲 𝘁𝗿𝘆𝗶𝗻𝗴 𝘁𝗼 𝘁𝗿𝗮𝗱𝗲!")
        return

    if not receiver_character:
        await message.reply_text("𝐓𝐡𝐞 𝐨𝐭𝐡𝐞𝐫 𝐮𝐬𝐞𝐫 𝐝𝐨𝐞𝐬𝐧'𝐭 𝐡𝐚𝐯𝐞 𝐭𝐡𝐞 𝐜𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫 𝐭𝐡𝐞𝐲'𝐫𝐞 𝐭𝐫𝐲𝐢𝐧𝐠 𝐭𝐨 𝐭𝐫𝐚𝐝𝐞")
        return

    # Rest of your code...




    if len(message.command) != 3:
        await message.reply_text("/𝙩𝙧𝙖𝙙𝙚 [𝙔𝙤𝙪𝙧 𝘾𝙝𝙖𝙧𝙖𝙘𝙩𝙚𝙧 𝙄𝘿] [𝙊𝙩𝙝𝙚𝙧 𝙐𝙨𝙚𝙧 𝘾𝙝𝙖𝙧𝙖𝙘𝙩𝙚𝙧 𝙄𝘿]!")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    # Add the trade offer to the pending trades
    pending_trades[(sender_id, receiver_id)] = (sender_character_id, receiver_character_id)

    # Create a confirmation button
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Confirm Trade", callback_data="confirm_trade")],
            [InlineKeyboardButton("Cancel Trade", callback_data="cancel_trade")]
        ]
    )

    await message.reply_text(f"{message.reply_to_message.from_user.mention}, do you accept this trade?", reply_markup=keyboard)


@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_trade", "cancel_trade"]))
async def on_callback_query(client, callback_query):
    receiver_id = callback_query.from_user.id

    # Find the trade offer
    for (sender_id, _receiver_id), (sender_character_id, receiver_character_id) in pending_trades.items():
        if _receiver_id == receiver_id:
            break
    else:
        await callback_query.answer("𝙏𝙝𝙞𝙨 𝙞𝙨 𝙣𝙤𝙩 𝙛𝙤𝙧 𝙮𝙤𝙪!", show_alert=True)
        return

    if callback_query.data == "confirm_trade":
        # Perform the trade
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
        receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

        # Remove the characters from the users' collections
        sender['characters'].remove(sender_character)
        receiver['characters'].remove(receiver_character)

        # Update the users' collections in the database
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        # Add the characters to the other users' collections
        sender['characters'].append(receiver_character)
        receiver['characters'].append(sender_character)

        # Update the users' collections in the database again
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        # Remove the trade offer from the pending trades
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"𝙔𝙤𝙪 𝙝𝙖𝙫𝙚 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙩𝙧𝙖𝙙𝙚𝙙 𝙮𝙤𝙪𝙧 𝙘𝙝𝙖𝙧𝙖𝙘𝙩𝙚𝙧 𝙬𝙞𝙩𝙝 {callback_query.message.reply_to_message.from_user.mention}!")

    elif callback_query.data == "cancel_trade":
        # Remove the trade offer from the pending trades
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text("❌️ 𝙎𝙖𝙙 𝘾𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙....")



# This dictionary will hold the gift offers until they are confirmed or cancelled
pending_gifts = {}


@shivuu.on_message(filters.command("gift"))
async def gift(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("𝗬𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗿𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝘂𝘀𝗲𝗿'𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘁𝗼 𝗴𝗶𝗳𝘁 𝗮 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿!")
        return

    receiver_id = message.reply_to_message.from_user.id
    receiver_username = message.reply_to_message.from_user.username
    receiver_first_name = message.reply_to_message.from_user.first_name

    if sender_id == receiver_id:
        await message.reply_text("𝙔𝙤𝙪 𝙘𝙖𝙣'𝙩 𝙜𝙞𝙛𝙩 𝙖 𝙘𝙝𝙖𝙧𝙖𝙘𝙩𝙚𝙧 𝙩𝙤 𝙮𝙤𝙪𝙧𝙨𝙚𝙡𝙛!")
        return

    if len(message.command) != 2:
        await message.reply_text("𝙔𝙤𝙪 𝙣𝙚𝙚𝙙 𝙩𝙤 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙖 𝙘𝙝𝙖𝙧𝙖𝙘𝙩𝙚𝙧 𝙄𝘿!")
        return

    character_id = message.command[1]

    sender = await user_collection.find_one({'id': sender_id})

    character = next((character for character in sender['characters'] if character['id'] == character_id), None)

    if not character:
        await message.reply_text("𝐘𝐨𝐮 𝐝𝐨𝐧'𝐭 𝐡𝐚𝐯𝐞 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐫𝐚𝐜𝐭𝐞𝐫 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐜𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧!")
        return

    # Add the gift offer to the pending gifts
    pending_gifts[(sender_id, receiver_id)] = {
        'character': character,
        'receiver_username': receiver_username,
        'receiver_first_name': receiver_first_name
    }

    # Create a confirmation button
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Confirm Gift", callback_data="confirm_gift")],
            [InlineKeyboardButton("Cancel Gift", callback_data="cancel_gift")]
        ]
    )

    await message.reply_text(f"do You Really Wanns To Gift {message.reply_to_message.from_user.mention}?", reply_markup=keyboard)

@shivuu.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_gift", "cancel_gift"]))
async def on_callback_query(client, callback_query):
    sender_id = callback_query.from_user.id

    # Find the gift offer
    for (_sender_id, receiver_id), gift in pending_gifts.items():
        if _sender_id == sender_id:
            break
    else:
        await callback_query.answer("This is not for you!", show_alert=True)
        return

    if callback_query.data == "confirm_gift":
        # Perform the gift
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        # Remove the character from the sender's collection
        sender['characters'].remove(gift['character'])
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})

        # Add the character to the receiver's collection
        if receiver:
            await user_collection.update_one({'id': receiver_id}, {'$push': {'characters': gift['character']}})
        else:
            # Create new user document
            await user_collection.insert_one({
                'id': receiver_id,
                'username': gift['receiver_username'],
                'first_name': gift['receiver_first_name'],
                'characters': [gift['character']],
            })

        # Remove the gift offer from the pending gifts
        del pending_gifts[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗴𝗶𝗳𝘁𝗲𝗱 𝘆𝗼𝘂𝗿 𝗰𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝘁𝗼 [{gift['receiver_first_name']}](tg://user?id={receiver_id})!")


