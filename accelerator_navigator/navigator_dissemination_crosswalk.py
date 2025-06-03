from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.dissemination_crosswalk import DisseminationCrosswalk


class NavigatorDisseminationCrosswalk(DisseminationCrosswalk):
    """
    Task to turn accelerator schema into target schema appropriate for navigator.
    """

    def __init__(self, xcom_props_resolver:XcomPropsResolver):
        """
        class constructor, injects a subclass of XcomPropsResolver which allows external
        configuration of behavior
        :param xcom_props_resolver: XcomPropsResolver instance for access to external configuration
        """
        super().__init__(xcom_props_resolver)

    def transform(
        self, dissemination_payload: DisseminationPayload
    ) -> DisseminationPayload:
        """
        Main action, translate the content in DisseminationPayload into the targegt format
        :param dissemination_payload: The data from accelerator to be transformed
        :return: DisseminationPayload updated with translated data
        """

        # the payload will either have an inline response or provide a path to a temporary file location,
        # depending on the size and configuration. Utilize the payload_resolve method of AcceratorWorkflowTask
        # to extract this data in either presentation (TODO: still needs refactoring)

        # 1) create a destination payload for output that passes along the DisseminationDescriptor


        # 2) use the payload_resolve method of AcceleratorWorkflowTask (a parent of this implementation) to
        # get the payload data, it may be either passed inline or stored in a temp file, this will abstract that

        # 3) crosswalk from the input to your output

        # 4) use the report_individual_dissemination method of AcceleratorWorkflowTask to put your data out

