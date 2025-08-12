"""
Flexible configuration for Navigator components
"""
def NavigatorConfig():

    def __init__(self):
      self.chroma_host = ""
      self.chroma_port = ""
      self.chroma_user = ""
      self.chroma_password = ""
      self.chroma_collection_name = ""
      self.ai_base_url = ""
      self.ai_api_key = ""
      self.ai_model_embedding = ""
      self.chunk_size = ""
      self.chunk_overlap = ""

def navigator_config_from_props(props, chroma_password_env_var:str = None, api_key_env_var:str = None):
  config = NavigatorConfig()

  config.chroma_host = props["CHROMA_HOST"]
  config.chroma_port = props["CHROMA_PORT"]
  config.chroma_user = props["CHROMA_USERNAME"]
  config.chroma_password = props["CHROMA_PASSWORD"]
  config.chroma_collection_name = props["CHROMA_COLLECTION_NAME"]
  config.ai_base_url = props["AI_BASE_URL"]
  config.ai_api_key = props["AI_API_KEY"]
  config.ai_model_embedding = props["AI_MODEL_EMBEDDING"]