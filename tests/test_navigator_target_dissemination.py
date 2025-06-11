import unittest

from accelerator_core.schema.models.accel_model import AccelProgramModel, AccelProjectModel, \
    AccelIntermediateResourceModel, AccelResourceReferenceModel, AccelPublicationModel, AccelDataResourceModel, \
    AccelTemporalDataModel, AccelGeospatialDataModel, build_accel_from_model
from accelerator_core.schema.models.base_model import SubmissionInfoModel, TechnicalMetadataModel
from accelerator_core.utils.xcom_utils import DirectXcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationDescriptor, DisseminationPayload
from accelerator_navigator.navigator_dissemination_crosswalk import NavigatorDisseminationCrosswalk
from accelerator_navigator.navigator_target_dissemination import NavigatorTargetDissemination
from pathlib import Path
import dotenv

class TestNavigatorDissemination(unittest.TestCase):
    def test_transform(self):
        submission = SubmissionInfoModel()
        submission.submitter_comment = "comment"
        submission.submitter_email = "email"
        submission.submitter_name = "name"

        technical = TechnicalMetadataModel()
        technical.created = "2025-06-03T18:57:30Z"
        technical.description = "CEDAR"
        technical.original_source_link = "https://cedar.metadatacenter.org/instances/edit/https://repo.metadatacenter.org/template-instances/3655ad1a-cfff-4018-9b2b-1ce153f7eb59?folderId=https:%2F%2Frepo.metadatacenter.org%2Ffolders%2Fc3e2f654-d6d1-402a-a64f-b3743a47fea2"

        program = AccelProgramModel()
        program.name = "bob"
        program.code = "hibob"

        project = AccelProjectModel()
        project.code = "bobsproject"
        project.name = "bobs excellent project"
        project.short_name = "bobs excellent projects short name"
        project.project_sponsor.append("sponsor1")
        project.project_sponsor.append("sponsor2")
        project.project_sponsor_type.append("sponsor type 1")
        project.project_url = "https://project.url"

        resource = AccelIntermediateResourceModel()
        resource.name = "dummy"
        resource.code = "dummycode"
        resource.description = "Poor air quality can negatively impact individuals with asthma, especially those sensitive to air pollutants like ozone and particulate matter. Air pollution can worsen asthma symptoms, trigger attacks, and even cause the onset of asthma. "
        resource.resource_type = "resourcetype"
        resource.resource_url = "https://resourceurl"
        resource.domain.append("air quality")
        resource.domain.append("asthma")
        resource.keywords.append("air quality")
        resource.keywords.append("air pollutants")
        resource.keywords.append("ozone")
        resource.keywords.append("asthma")
        resource.access_type = "access_type"

        resource_reference = AccelResourceReferenceModel()
        resource_reference.resource_reference_text = "resource_reference_text"
        resource_reference.resource_reference_link = "https://resource_reference_link"

        resource.resource_reference.append(resource_reference)

        publication = AccelPublicationModel()
        publication.citation = "citation"
        publication.citation_link = "https://citationlink"

        resource.publication.append(publication)

        data_resource = AccelDataResourceModel()
        data_resource.exposure_media.append("media1")
        data_resource.measures.append("measures1")
        data_resource.measurement_method = "measurement_method"
        data_resource.data_formats.append("data_formats")
        data_resource.data_location.append("data_location1")
        data_resource.data_location.append("data_location2")

        temporal = AccelTemporalDataModel()
        temporal.temporal_resolution.append("temporal_resolution1")
        temporal.temporal_resolution.append("temporal_resolution2")
        temporal.temporal_resolution_comment = "comment"

        geospatial = AccelGeospatialDataModel()
        geospatial.spatial_resolution.append("spatial_resolution1")
        geospatial.spatial_resolution.append("spatial_resolution2")
        geospatial.geometry_source.append("geometry_source1")

        accel_as_dict = build_accel_from_model(
            version="1.0.0",
            submission=submission,
            technical=technical,
            program=program,
            project=project,
            resource=resource,
            data_resource=data_resource,
            temporal=temporal,
            population=None,
            geospatial=geospatial
        )

        self.assertIsNotNone(accel_as_dict)

        # this stuff emulates DAG environment and Accel stuff that would come to you
        xcom_props_resolver = DirectXcomPropsResolver(temp_files_supported=False, temp_files_location=None)

        dissemination_descriptor = DisseminationDescriptor()
        dissemination_descriptor.dissemination_identifier = "test"
        dissemination_descriptor.dissemination_type = "Navigator"
        dissemination_descriptor.dissemination_version = "1.0.0"
        dissemination_descriptor.dissemination_item_id = "3655ad1a-cfff-4018-9b2b-1ce153f7eb59"
        dissemination_descriptor.use_tempfiles = False
        dissemination_descriptor.ingest_identifier = "CEDAR"
        dissemination_payload = DisseminationPayload(dissemination_descriptor)

        # accel will add your data in the payload, in this case it is inline
        dissemination_payload.payload.append(accel_as_dict)
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
