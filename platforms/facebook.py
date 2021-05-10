import requests

class Facebook:

    def event_call(page_id,facebook_page_access_token,msg):
        pg_id = int(page_id)
        post_url = 'https://graph.facebook.com/{}/feed'.format(pg_id)
        payload = {
            'message': msg,
            'access_token': facebook_page_access_token
        }
        res = requests.post(post_url,data=payload)
        return res