from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.accel_target_dissemination import AccelDisseminationComponent
from .vectordb import ChromaDB, loadDocuments

logger = setup_logger("accelerator")

class NavigatorTargetDissemination(AccelDisseminationComponent):

    def __init__(self, xcom_props_resolver: XcomPropsResolver):
        """
        @param: xcom_properties_resolver XcomPropertiesResolver that can access
        handling configuration
        """

        super().__init__(xcom_props_resolver)

    def disseminate(self, dissemination_payload: DisseminationPayload, additional_parameters:dict) -> DisseminationPayload:
        """

        Action method to disseminate the given payload to an arbitrary target (in this case, a vector db)

        @:parameter dissemination_payload DisseminationPayload that contains the data to be sent to the target
        @:parameter additional_parameters dict Additional parameters that can be passed to this function

        """

        # the following will be put into 'additional_parameters' above and provided by the environment

        # Vector related
        chroma_host = additional_parameters["CHROMA_HOST"]
        chroma_port = additional_parameters["CHROMA_PORT"]
        chroma_user = additional_parameters["CHROMA_USERNAME"]
        chroma_password = additional_parameters["CHROMA_PASSWORD"]
        collection_name = additional_parameters["CHROMA_COLLECTION_NAME"]

        # AI Auth
        ai_base_url = additional_parameters["AI_BASE_URL"]
        ai_api_key = additional_parameters["AI_API_KEY"]

        # AI Embedding model
        embedding = additional_parameters["AI_MODEL_EMBEDDING"]

        # Vector db insert metrics
        chunk_size = int(additional_parameters["CHUNK_SIZE"])
        chunk_overlap = int(additional_parameters["CHUNK_OVERLAP"])

        # Vector db instance
        db = ChromaDB(collection_name = collection_name, 
                 embedding = embedding, 
                 host = chroma_host, 
                 port = chroma_port, 
                 base_url = ai_base_url, 
                 api_key = ai_api_key
        )

        # Data retrieval from payload
        data_list = []
        payload_length = self.get_payload_length(dissemination_payload)
        for i in range(payload_length):
            payload = self.payload_resolve(dissemination_payload, i)
            logger.info(f"found payload {payload}")

            data_list.append(payload['data']['resource'])

        # Convert json data to langchain documents
        docs = loadDocuments(data_list)

        # Vector db insert
        db.add(docs=docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        return dissemination_payload


