import requests

class Telegram:

    def event_call(tg_token,groups_id_of_user,msg):
        for group_id in groups_id_of_user:
            print(str(group_id[0]))
            send_message_url = 'https://api.telegram.org/bot{}/sendMessage'.format(tg_token)
            data ={
                'chat_id': str(group_id[0]),
                'text': str(msg)
            }
            requests.post(send_message_url,data=data)