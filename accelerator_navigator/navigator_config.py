"""
Flexible configuration for Navigator components
"""
import os

from accelerator_core.utils.resource_utils import properties_file_from_path

class NavigatorConfig():

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


    def to_dict(self):
      """
      convert the properties configuration to a dict that maps to the expected
      additional parameters
      :return: dict that can be used as additional parameters
      """

      additional_parameters = {
        "CHROMA_HOST": self.chroma_host,
        "CHROMA_PORT": self.chroma_port,
        "CHROMA_USERNAME": self.chroma_user,
        "CHROMA_PASSWORD": self.chroma_password,
        "CHROMA_COLLECTION_NAME": self.chroma_collection_name,
        "AI_BASE_URL": self.ai_base_url,
        "AI_API_KEY": self.ai_api_key,
        "AI_MODEL_EMBEDDING": self.ai_model_embedding,
        "CHUNK_SIZE": self.chunk_size,
        "CHUNK_OVERLAP": self.chunk_overlap
      }

      return additional_parameters



def navigator_config_from_props(props_path, chroma_password_env_var:str = None, api_key_env_var:str = None):
  config = NavigatorConfig()
  props = properties_file_from_path(props_path)


  config.chroma_host = props["chroma.host"]
  config.chroma_port = props["chroma.port"]
  config.chroma_user = props["chroma.username"]
  config.chroma_password = props["chroma.password"]
  config.chroma_collection_name = props["chroma.collection.name"]
  config.ai_base_url = props["ai.base.url"]
  config.ai_api_key = props["ai.api.key"]
  config.ai_model_embedding = props["ai.model.embedding"]
  config.chunk_size = props["chunk.size"]
  config.chunk_overlap = props["chunk.overlap"]

  # check for env variable overrides
  if chroma_password_env_var:
      config.chroma_password = os.environ.get(chroma_password_env_var)

  if api_key_env_var:
      config.ai_api_key = os.environ.get(api_key_env_var)

  return config