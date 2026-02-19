import json
import os

from jinja2 import Environment, FileSystemLoader, Template

from accelerator_core.utils.logger import setup_logger

logger = setup_logger("accelerator")

class NavigatorDocument:
    """
    Value class for information in the Navigator document model
    """

    def __init__(self):
        self.description = ""
        self.title = ""
        self.link = ""
        self.keywords = []
        self.resource_type = ""
        self.resource = {}


class DocumentTemplateProcessor:
    """
    Library for jinja templates for document models for navigator
    """

    def __init__(self):
        """
        Initialize ingest tool
        :return:
        """

        # Get the directory of the script
        script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

        # Create a Jinja environment with the FileSystemLoader
        self.env = Environment(loader=FileSystemLoader(script_dir))

    def retrieve_template(self, document: str) -> Template:
        """
        retrieve a template from the templates dir
        :param template_name: string with the template name as found in the templates dir, without version or extension
        :param template_version: string in x.x.x form with the version number
        :return: Template for jinja rendering
        """

        return self.env.get_template(f"{document}.jinja")

    def produce_navigator_document(self, navigator_document) -> str:
        """
        take the data in the navigator document and render into the format for ingest into the vector db
        :param navigator_document:
        :return: str with the document in the format for ingest into the vector db
        """
        template = self.retrieve_template("document")
        return template.render(document=navigator_document)
