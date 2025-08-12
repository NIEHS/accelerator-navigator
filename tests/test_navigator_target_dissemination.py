import json
import unittest

from accelerator_core.utils import resource_utils

from accelerator_core.schema.models.accel_model import AccelProgramModel, AccelProjectModel, \
    AccelIntermediateResourceModel, AccelResourceReferenceModel, AccelPublicationModel, AccelDataResourceModel, \
    AccelTemporalDataModel, AccelGeospatialDataModel, build_accel_from_model
from accelerator_core.schema.models.base_model import SubmissionInfoModel, TechnicalMetadataModel
from accelerator_core.utils.accelerator_config import config_from_file
from accelerator_core.utils.resource_utils import determine_test_resource_path
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationDescriptor, DisseminationPayload
from accelerator_navigator.navigator_config import NavigatorConfig, navigator_config_from_props
from accelerator_navigator.navigator_dissemination_crosswalk import NavigatorDisseminationCrosswalk
from accelerator_navigator.navigator_target_dissemination import NavigatorTargetDissemination
from pathlib import Path
import dotenv

class TestNavigatorDissemination(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_path = resource_utils.determine_test_resource_path(
            "application.properties", "tests"
        )

        navigator_config = navigator_config_from_props(test_path)
        cls._navigator_config = navigator_config

    def test_disseminate(self):

        with open("test_resources/example1.json") as json_data:
            d = json.load(json_data)

            # this stuff emulates DAG environment and Accel stuff that would come to you
            xcom_props_resolver = DirectXcomPropsResolver(
                temp_files_supported=False, temp_files_location=""
            )

            dissemination_descriptor = DisseminationDescriptor()
            dissemination_descriptor.dissemination_identifier = "test"
            dissemination_descriptor.dissemination_type = "Navigator"
            dissemination_descriptor.dissemination_version = "1.0.0"
            dissemination_descriptor.dissemination_item_id = "3655ad1a-cfff-4018-9b2b-1ce153f7eb59"
            dissemination_descriptor.use_tempfiles = False
            dissemination_descriptor.ingest_identifier = "CEDAR"
            dissemination_payload = DisseminationPayload(dissemination_descriptor)

            # accel will add your data in the payload, in this case it is inline
            dissemination_payload.payload.append(d)
            dissemination_payload.payload_inline = True

            props = {}
            env_config = dotenv.dotenv_values(Path(".env"))
            props["CHROMA_HOST"] = env_config.get('CHROMA_HOST')
            props["CHROMA_PORT"] = env_config.get('CHROMA_PORT')
            props["CHROMA_USERNAME"] = env_config.get('CHROMA_USERNAME')
            props["CHROMA_PASSWORD"] = env_config.get('CHROMA_PASSWORD')
            props["CHROMA_COLLECTION_NAME"] = env_config.get('CHROMA_COLLECTION_NAME')
            props["AI_BASE_URL"] = env_config.get('AI_BASE_URL')
            props["AI_API_KEY"] = env_config.get('AI_API_KEY')
            props["AI_MODEL_EMBEDDING"] = env_config.get('AI_MODEL_EMBEDDING')
            props["CHUNK_SIZE"] = env_config.get('CHUNK_SIZE')
            props["CHUNK_OVERLAP"] = env_config.get('CHUNK_OVERLAP')

            dissem = NavigatorTargetDissemination(xcom_props_resolver)
            actual = dissem.disseminate(dissemination_payload, props)

            self.assertIsNotNone(actual)


if __name__ == '__main__':
    unittest.main()
