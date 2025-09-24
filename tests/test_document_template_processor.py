import unittest

from accelerator_navigator.document_template_processor import NavigatorDocument, DocumentTemplateProcessor


class TestDocumentTemplateProcessor(unittest.TestCase):
    def test_produce_navigator_document(self):
        navigator_document = NavigatorDocument()
        navigator_document.keywords = ["keyword1", "keyword2"]
        navigator_document.title = "title"
        navigator_document.description = "description"

        doc_processor = DocumentTemplateProcessor()
        actual = doc_processor.produce_navigator_document(navigator_document)
        self.assertIsNotNone(actual)



if __name__ == '__main__':
    unittest.main()
