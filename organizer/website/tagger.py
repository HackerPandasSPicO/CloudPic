import requests
from website.sending_settings import IMAGGA_API_TAG_END_POINT_BASE, IMAGGA_API_HEADERS


class Tagger:

	# This method returns first then matching tags 
    def get_tags_for_pic_from_url(self, url):
        r = requests.get(IMAGGA_API_TAG_END_POINT_BASE + url, headers=IMAGGA_API_HEADERS)
        result_as_dict = r.json()
        return [[a['tag'] for a in x['tags']][:10] for x in result_as_dict['results']]
