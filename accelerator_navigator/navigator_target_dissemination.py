from accelerator_core.utils.xcom_utils import XcomPropsResolver
from accelerator_core.workflow.accel_data_models import DisseminationPayload
from accelerator_core.workflow.accel_target_dissemination import AccelDisseminationComponent


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

        # send the prepared data to the target, we need to investigate connectors and plugins where they
        # may be suitable, or go directly.

        # the payload will either have an inline response or provide a path to a temporary file location,
        # depending on the size and configuration. Utilize the payload_resolve method of AcceratorWorkflowTask
        # to extract this data in either presentation (TODO: still needs refactoring)

        # 1) create a destination payload for output that passes along the DisseminationDescriptor

        # 2) use the payload_resolve method of AcceleratorWorkflowTask (a parent of this implementation) to
        # get the payload data, it may be either passed inline or stored in a temp file, this will abstract that

        # 3) push data to target

        # 4) use the report_individual_dissemination method of AcceleratorWorkflowTask to put your data out


        # TODO: some add'l work to report back to accelerator after dissemination, how to pass back logs to accel?

