import requests
import backoff
from typing import Optional
from enum import Enum 


from pexels_api.models.response import Response, Photo, RateLimitInfo

from typing import Union, Optional

class Color(Enum):
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    TURQUOISE = "turquoise"
    BLUE = "blue"
    VIOLET = "violet"
    PINK = "pink"
    BROWN = "brown"
    BLACK = "black"
    GRAY = "gray"
    WHITE = "white"

    @classmethod
    def is_valid_hex(cls, value: str) -> bool:
        # Check if the value is a valid hexadecimal color code
        return value.startswith("#") and len(value) == 7 and all(c in "0123456789abcdefABCDEF" for c in value[1:])

    @classmethod
    def get_color(cls, value: str) -> Union[str, None]:
        # Check if the value is a valid named color or hexadecimal color code
        if value.lower() in [color.value.lower() for color in cls]:
            return value.lower()
        elif cls.is_valid_hex(value):
            return value.lower()
        else:
            return None

class Locale(Enum):
    EN_US = "en-US"
    PT_BR = "pt-BR"
    ES_ES = "es-ES"
    CA_ES = "ca-ES"
    DE_DE = "de-DE"
    IT_IT = "it-IT"
    FR_FR = "fr-FR"
    SV_SE = "sv-SE"
    ID_ID = "id-ID"
    PL_PL = "pl-PL"
    JA_JP = "ja-JP"
    ZH_TW = "zh-TW"
    ZH_CN = "zh-CN"
    KO_KR = "ko-KR"
    TH_TH = "th-TH"
    NL_NL = "nl-NL"
    HU_HU = "hu-HU"
    VI_VN = "vi-VN"
    CS_CZ = "cs-CZ"
    DA_DK = "da-DK"
    FI_FI = "fi-FI"
    UK_UA = "uk-UA"
    EL_GR = "el-GR"
    RO_RO = "ro-RO"
    NB_NO = "nb-NO"
    SK_SK = "sk-SK"
    TR_TR = "tr-TR"
    RU_RU = "ru-RU"

class PhotoSize(Enum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"


class PexelsAPI:
    URL = "https://api.pexels.com/v1"
    def __init__(self, authorization_token: str, hourly_rate_limit=200):
        self.authorization_token = authorization_token
        self.headers = {"Authorization": authorization_token} 
        self.remaining_requests_by_hour = hourly_rate_limit

    def get_photo_by_id(self, photo_id: int):
        response = requests.get(f"{self.URL}/photos/{photo_id}", headers=self.headers, timeout=60)

        return Photo(**response.json())

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
    def _make_request(self, method, url, payload):
        response = requests.request(method, url, payload, headers=self.headers, timeout=60)
        response.raise_for_status()
        return response

    def get_curated(
        self,
        page: Optional[int] = 1,
        per_page: Optional[int] = 15
    ):
        response = self._make_request('get', f"{self.URL}/curated?per_page={per_page}&page={page}")

        response_json = response.json()

        parsed_response = Response(
            photos=[Photo(**photo) for photo in response_json['photos']],
            page=response_json['page'],
            per_page=response_json['per_page'],
            total_results=response_json['total_results'],
            prev_page=response_json.get('prev_page'),
            next_page=response_json.get('next_page')
        )

        return parsed_response

    def search_image(
        self,
        query: str,
        orientation: Optional[str] = None,
        size: Optional[PhotoSize] = None,
        color: Optional[Color] = None,

        locale: Optional[Locale] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 15
    ):
        request_url = f"{self.URL}/search?query={query}&per_page={per_page}&page={page}"

        if orientation:
            request_url += f"&orientation={orientation}"
        if size:
            request_url += f"&size={size.value}"
        if color:
            request_url += f"&color={color.value}"
        if locale:
            request_url += f"&locale={locale.value}"


        response = self._make_request('get', request_url)
        try:
            rate_limit_info = RateLimitInfo(
                limit=int(response.headers['X-Ratelimit-Limit']),
                remaining=int(response.headers['X-Ratelimit-Remaining']),
                reset=int(response.headers['X-Ratelimit-Reset'])
            )
        except Exception as e:
            print(response.content)
            print(response.status_code)
            print(response.headers)

        response_json = response.json()

        parsed_response = Response(
            photos=[Photo(**photo) for photo in response_json['photos']],
            page=response_json['page'],
            per_page=response_json['per_page'],
            total_results=response_json['total_results'],
            prev_page=response_json.get('prev_page'),
            next_page=response_json.get('next_page')
        )

        return parsed_response
