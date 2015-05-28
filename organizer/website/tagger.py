import requests
from website.sending_settings import IMAGGA_API_TAG_END_POINT_BASE, IMAGGA_API_HEADERS


class Tagger:

        # This method returns first then matching tags

    def get_tags_for_pic_from_url(self, url):
        r = requests.get(IMAGGA_API_TAG_END_POINT_BASE + url, headers=IMAGGA_API_HEADERS)
        result_as_dict = r.json()

        # chek if request is ok -> if is not ok return empty list
        if 'status' in result_as_dict:
            return []
        newlist = sorted([x['tags'] for x in result_as_dict['results']][0], key=lambda k: k['confidence'], reverse=True)
        return newlist
