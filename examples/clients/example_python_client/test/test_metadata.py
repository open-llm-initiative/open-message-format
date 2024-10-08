# coding: utf-8

"""
    Open Message Format

    This specification defines an API contract between client and server for building conversational agents, and defines a standard schema for the \"messages\" object, which contains user and assistant interactions. The \"messages\" object schema serves a dual purpose, to capture user and assistant conversation from client to your back-end, and from your back-end server to an upstream LLM 

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from openapi_client.models.metadata import Metadata

class TestMetadata(unittest.TestCase):
    """Metadata unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Metadata:
        """Test Metadata
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Metadata`
        """
        model = Metadata()
        if include_optional:
            return Metadata(
                model = '',
                tokens = ''
            )
        else:
            return Metadata(
                model = '',
        )
        """

    def testMetadata(self):
        """Test Metadata"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
