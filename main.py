from telethon.sync import TelegramClient, events
from collections import OrderedDict

api_id = 23195655
api_hash = '3dfeae8b2dcf5680f377346232702e4f'
client = TelegramClient('anon', api_id, api_hash)
#681542404
#6067597781 2059695882 mois
#usernames_to_send = [729712277, 6067597781, 681542404]
usernames_to_send = [6067597781, 729712277, 681542404]

messages_db = OrderedDict()

with client:
    @client.on(events.NewMessage)
    async def message_handler(event):
        ids = []
        if not event.message.reply_to:
            sender = await event.get_sender()
            if sender.phone:
                phone = '+' + str(sender.phone)
            else:
                phone = 'phone number is hidden'
            print(event.message.peer_id.user_id)
            if (event.message.peer_id.user_id in usernames_to_send):
                message = f'{event.text}\n'
            else:
                message = f'**Номер телефона:** {phone}\n{event.text}\n'

            # Send messages to users
            for user in usernames_to_send:
                if event.message.peer_id.user_id == user:
                    continue
                print(user)
                try:
                    response = await client.send_message(user, message, parse_mode='md')
                except Exception as e:
                    print(e)
                    continue
                ids.append(response.id)

            for id in ids:
                messages_db[id] = {
                    'sender_id': sender.id,
                    'phone': phone,
                    'username': sender.username,
                    'message': message
                }

            if len(messages_db) > 500:
                for _ in range(250):
                    messages_db.popitem(last=True)

    @client.on(events.NewMessage)
    async def handle_reply(event):
        if event.message.reply_to and (event.message.peer_id.user_id in usernames_to_send):
            rep = messages_db.get(event.reply_to.reply_to_msg_id)
            if rep:
                for user in usernames_to_send:
                    if event.message.peer_id.user_id == user:
                        continue
                    if (event.message.peer_id.user_id in usernames_to_send):
                        print(rep["sender_id"])
                        message = f'**Ответ:** {rep["phone"]}\n{event.message.message}\n'
                        await client.send_message(user, message, parse_mode='md')
                return await client.send_message(rep['sender_id'], event.message.message)
        
    client.run_until_disconnected()