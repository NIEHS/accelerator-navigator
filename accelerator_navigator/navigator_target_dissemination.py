import os

from accelerator_core.utils.logger import setup_logger
from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.accel_target_dissemination import AccelDisseminationComponent
from accelerator_navigator.cert_bundler import bundle_certs
from accelerator_navigator.document_template_processor import NavigatorDocument
from accelerator_navigator.vectordb import ChromaDB, load_document

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

        #bundle_certs(None)

        # the following will be put into 'additional_parameters' above and provided by the environment

        # Vector related
        chroma_host = additional_parameters["host"]
        chroma_port = additional_parameters["port"]
        chroma_user = additional_parameters["user"]
        chroma_password = additional_parameters["password"]
        collection_name = additional_parameters["collection"]

        # AI Auth
        ai_base_url = additional_parameters["ai_base_url"]
        ai_api_key = additional_parameters["api_key"]

        # AI Embedding model
        embedding = additional_parameters["ai_model_embedding"]

        # Vector db insert metrics
        chunk_size = 1000
        chunk_overlap = 200

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
            resource = payload['data']['resource']

            metadata = {'id':payload['_id']['$oid'],
                        'Source':payload['technical_metadata']['original_source_link'],
                        'original_identifier':payload['technical_metadata']['original_source_identifier'],
                        'project':payload['data']['project']['project_name'],
                        'Title':resource['resource_name'],
                        'Keywords':resource['resource_keywords'],
                        'Type of data': resource['resource_type'],
                        'Link': resource['resource_url']
                        }

            doc = load_document(content=resource['resource_description'], metadata=metadata)

            # Vector db insert
            db.add(docs=[doc], chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        return dissemination_payload


