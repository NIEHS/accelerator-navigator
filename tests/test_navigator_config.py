import os
import os
import unittest

from accelerator_core.utils import resource_utils

from accelerator_navigator.navigator_config import navigator_config_from_props

API_KEY = "test_env_key_api_key"

CHROMA_PASS = "test_env_key_chroma_password"

class TestNavigatorConfig(unittest.TestCase):


    def test_config_fromprops(self):
        test_path = "./test_resources/application.properties"

        os.environ[CHROMA_PASS] = "chromapassword"
        os.environ[API_KEY] = "apikey"
        
        config = navigator_config_from_props(test_path, chroma_password_env_var=CHROMA_PASS, api_key_env_var=API_KEY)
        self.assertIsNotNone(config)
        self.assertEqual(config.ai_api_key,"apikey" )
        self.assertEqual(config.chroma_password, "chromapassword" )

    def test_todict(self):
        test_path = "./test_resources/application.properties"

        os.environ[CHROMA_PASS] = "chromapassword"
        os.environ[API_KEY] = "apikey"

        config = navigator_config_from_props(test_path, chroma_password_env_var=CHROMA_PASS, api_key_env_var=API_KEY)
        actual = config.to_dict()
        self.assertEqual(actual["AI_API_KEY"],config.ai_api_key)

if __name__ == '__main__':
    unittest.main()
