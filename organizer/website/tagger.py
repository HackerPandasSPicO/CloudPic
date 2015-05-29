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

    @staticmethod
    def get_content_id(image_path):
        url = "https://api.imagga.com/v1/content"
        files = {'file': open(image_path, 'rb')}

        r = requests.post(url, files=files, headers=IMAGGA_API_HEADERS)
        result_as_dict = r.json()

        try:
            return result_as_dict['uploaded'][0]['id']
        except:
            return None

    @staticmethod
    def categorize_by_content_id(content_id):
        url = "https://api.imagga.com/v1/categorizations/personal_photos"
        r = requests.get(url + "?content=" + content_id,
                         headers=IMAGGA_API_HEADERS)
        result_as_dict = r.json()

        try:
            top_category = result_as_dict['results'][0]['categories'][0]
            return top_category['name'], float(top_category['confidence'])
        except:
            return None

    @staticmethod
    def tag_by_content_id(content_id):
        url = "https://api.imagga.com/v1/tagging"
        r = requests.get(url + "?content=" + content_id,
                         headers=IMAGGA_API_HEADERS)
        result_as_dict = r.json()

        try:
            output = []
            for result in result_as_dict["results"][0]["tags"]:
                output.append((result["tag"], float(result["confidence"])))
            return output
        except:
            return None
