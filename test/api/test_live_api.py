#  coding: utf-8
#  ----------------------------------------------------------------------------
#  <copyright company="Aspose" file="test_live_api.py">
#    Copyright (c) 2019 Aspose Pty Ltd. All rights reserved.
#  </copyright>
#  <summary>
#    Permission is hereby granted, free of charge, to any person obtaining a
#   copy  of this software and associated documentation files (the "Software"),
#   to deal  in the Software without restriction, including without limitation
#   the rights  to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell  copies of the Software, and to permit persons to whom the
#   Software is  furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all  copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM,  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.
#  </summary>
#  ----------------------------------------------------------------------------

from itertools import product

import asposecadcloud.models.requests as requests
from asposecadcloud import rest
from asposecadcloud.models import *
from test.api import CadApiTester


class TestLiveApi(CadApiTester):
    """ Class for testing BmpAPI """

    def test_convert(self):
        """
        Convert drawing to png
        """
        
        self.override_reference_files = True
        self.remove_result = False
        additional_export_formats = set()
        format_extension_test_cases = ['png']

        formats_to_export = set(self.basic_export_formats).union(additional_export_formats)

        for save_to_storage in [False]:
            for format_extension in format_extension_test_cases:
                with self.subTest(
                        'format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

                    folder = self.original_data_folder
                    storage = self.test_storage

                    for input_file in self.input_test_files:
                        has_to_be_exported = False
                        for input_format in formats_to_export:
                            if str(input_file.name).endswith(input_format):
                                has_to_be_exported = True
                                break

                        if not has_to_be_exported:
                            continue

                        name = input_file.name
                        operation = '_convert'

                        output_path = None

                        reference_file_name = name + operation + "." + format_extension

                        def request_invoker(input_stream, out_path):
                            return self.cad_api.convert(
                                requests.ConvertRequest(input_stream, format_extension, None))

                        self.post_request_tester(
                            operation,
                            'Input image: {0}; Output format: {1}, out path: {2}'.format(name, format_extension,
                                                                                         output_path),
                            name,
                            output_path,
                            request_invoker,
                            lambda x, y, z: None,
                            folder,
                            reference_file_name,
                            storage)

    def test_watermark(self):
        """
        Convert drawing to png with watermark
        """
        
        self.override_reference_files = True
        self.remove_result = False
        additional_export_formats = set()
        format_extension_test_cases = ['png']

        formats_to_export = set(self.basic_export_formats).union(additional_export_formats)

        watermark = WatermarkRGB()
        watermark.text = "watermark"
        watermark.r = 0
        watermark.b = 0
        watermark.g = 255
        watermark_json = rest.ObjectHelper.sanitize_for_serialization(watermark)

        for save_to_storage in [False]:
            for format_extension in format_extension_test_cases:
                with self.subTest(
                        'format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

                    folder = self.original_data_folder
                    storage = self.test_storage

                    for input_file in self.input_test_files:
                        has_to_be_exported = False
                        for input_format in formats_to_export:
                            if str(input_file.name).endswith(input_format):
                                has_to_be_exported = True
                                break

                        if not has_to_be_exported:
                            continue

                        name = input_file.name
                        operation = '_watermark'

                        output_path = None
                        reference_file_name = name + operation + "." + format_extension

                        def request_invoker(input_stream, out_path):
                            return self.cad_api.watermark(
                                requests.WatermarkRequest(input_stream, format_extension, fr"{watermark_json}", None))

                        self.post_request_tester(
                            operation,
                            'Input image: {0}; Output format: {1}, out path: {2}'.format(name, format_extension,
                                                                                         output_path),
                            name,
                            output_path,
                            request_invoker,
                            lambda x, y, z: None,
                            folder,
                            reference_file_name,
                            storage)

    def test_paper_to_cad(self):
        """
        Convert raster drawing to png with watermark
        """
        
        self.override_reference_files = True
        self.remove_result = False
        additional_export_formats = set()
        format_extension_test_cases = ['dxf']

        formats_to_export = self.basic_raster_export_formats

        for save_to_storage in [False]:
            for format_extension in format_extension_test_cases:
                with self.subTest(
                        'format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

                    folder = self.original_data_folder
                    storage = self.test_storage

                    for input_file in self.input_test_files:
                        has_to_be_exported = False
                        for input_format in formats_to_export:
                            if str(input_file.name).endswith(input_format):
                                has_to_be_exported = True
                                break

                        if not has_to_be_exported:
                            continue

                        name = input_file.name
                        operation = '_paper_to_cad'

                        output_path = None
                        reference_file_name = name + operation + "." + format_extension

                        def request_invoker(input_stream, out_path):
                            return self.cad_api.paper_to_cad(
                                requests.PaperToCadRequest(input_stream, format_extension))

                        self.post_request_tester(
                            operation,
                            'Input image: {0}; Output format: {1}, out path: {2}'.format(name, format_extension,
                                                                                         output_path),
                            name,
                            output_path,
                            request_invoker,
                            lambda x, y, z: None,
                            folder,
                            reference_file_name,
                            storage)

    def test_text_extractor(self):
        """
        Extract text
        """
        
        self.override_reference_files = True
        self.remove_result = False
        additional_export_formats = set()
        input_format = 'dxf'
        format_extension_test_cases = ['txt']

        formats_to_export = set(self.basic_export_formats).union(additional_export_formats)

        for save_to_storage in [False]:
            for format_extension in format_extension_test_cases:
                with self.subTest(
                        'format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

                    folder = self.original_data_folder
                    storage = self.test_storage

                    for input_file in self.input_test_files:
                        has_to_be_exported = False
                        if str(input_file.name).endswith(input_format):
                            has_to_be_exported = True

                        if not has_to_be_exported:
                            continue

                        name = input_file.name
                        operation = '_text_extractor'

                        output_path = None
                        reference_file_name = name + operation + "." + format_extension

                        def request_invoker(input_stream, out_path):
                            return self.cad_api.extract_text(
                                requests.ExtractTextRequest(input_stream))

                        self.post_request_tester(
                            operation,
                            'Input image: {0}; Output format: {1}, out path: {2}'.format(name, format_extension,
                                                                                         output_path),
                            name,
                            output_path,
                            request_invoker,
                            lambda x, y, z: None,
                            folder,
                            reference_file_name,
                            storage)

    def test_metadata_extractor(self):
        """
        Extract metadata
        """
        
        self.override_reference_files = True
        self.remove_result = False
        additional_export_formats = set()
        format_extension_test_cases = ['txt', 'json', 'xml']

        formats_to_export = set(self.basic_export_formats).union(additional_export_formats)

        for save_to_storage in [False]:
            for format_extension in format_extension_test_cases:
                with self.subTest(
                        'format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

                    folder = self.original_data_folder
                    storage = self.test_storage

                    for input_file in self.input_test_files:
                        has_to_be_exported = False
                        for input_format in formats_to_export:
                            if str(input_file.name).endswith(input_format):
                                has_to_be_exported = True
                                break

                        if not has_to_be_exported:
                            continue

                        name = input_file.name
                        operation = '_metadata_extractor'

                        output_path = None

                        reference_file_name = name + operation + "." + format_extension

                        def request_invoker(input_stream, out_path):
                            return self.cad_api.extract_metadata(
                                requests.ExtractMetadataRequest(input_stream, format_extension))

                        self.post_request_tester(
                            operation,
                            'Input image: {0}; Output format: {1}, out path: {2}'.format(name, format_extension,
                                                                                         output_path),
                            name,
                            output_path,
                            request_invoker,
                            lambda x, y, z: None,
                            folder,
                            reference_file_name,
                            storage)

    def test_post_edit_metadata(self):
        """
        Get CAD metadata
        """
        self.override_reference_files = True
        self.remove_result = False
        input_format = 'dxf'
        format_extension_test_cases = ['json']
        output_path = None

        for save_to_storage in [False]:
            for format_extension in format_extension_test_cases:
                with self.subTest(
                        'format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

                    folder = self.original_data_folder
                    storage = self.test_storage

                    for input_file in self.input_test_files:
                        has_to_be_exported = False
                        if str(input_file.name).endswith(input_format):
                            has_to_be_exported = True

                        if not has_to_be_exported:
                            continue

                        name = input_file.name
                        operation = '_post_edit_metadata'

                        reference_file_name = name + operation + "." + format_extension

                        def request_invoker(input_stream, out_path):
                            return self.cad_api.edit_metadata(
                                requests.EditMetadataRequest(input_stream))

                        self.post_request_tester(
                            operation,
                            'Input image: {0}; Output file: {1}'.format(name, reference_file_name),
                            name,
                            output_path,
                            request_invoker,
                            lambda x, y, z: None,
                            folder,
                            reference_file_name,
                            storage)
