import unittest

import json
import unittest

import httpx
import certifi

from accelerator_navigator.navigator_config import NavigatorConfig, navigator_config_from_props

API_KEY_CONSTANT = "TEST_API_KEY"
CHROMA_PASSWORD_CONSTANT = "CHROMA_PASSWORD"


class TestCerts(unittest.TestCase):

    # set env variables as follows


    @classmethod
    def setUpClass(cls):
        test_path = "test_resources/application.properties"
        navigator_config = navigator_config_from_props(test_path, chroma_password_env_var=CHROMA_PASSWORD_CONSTANT,
                                                       api_key_env_var=API_KEY_CONSTANT)
        cls._navigator_config = navigator_config

    def test_cert(self):

        with open("test_resources/example1.json") as json_data:
            d = json.load(json_data)
            test_props =  self._navigator_config.to_dict()
            print(f"certifi cert store: {certifi.where()}")
            resp = httpx.get(test_props["AI_BASE_URL"])
            print(f"response: {resp}")



if __name__ == '__main__':
    unittest.main()
