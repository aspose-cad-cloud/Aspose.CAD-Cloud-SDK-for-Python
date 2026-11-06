#  coding: utf-8
#  ----------------------------------------------------------------------------
#  <copyright company="Aspose" file="test_rotate_flip_api.py">
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
from test.api import CadApiTester


class TestRotateFlipApi(CadApiTester):
    """ Class for testing RotateFlipAPI """

    def test_get_rotate_flip_image(self):
        """
        Performs RotateFlip (export to another format) operation test with GET
        method, taking input data from storage
        """
        
        self.override_reference_files = True
        self.remove_result = False
        additional_export_formats = set()
        if not self.EXTENDED_TEST:
            format_extension_test_cases = ['bmp']
        else:
            format_extension_test_cases = ['jpg']

        formats_to_export = set(self.basic_export_formats).union(additional_export_formats)

        for save_to_storage in [True, False]:
            for format_extension in format_extension_test_cases:
                with self.subTest('format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

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
                        operation = '_rotate_flip_get'

                        reference_file_name = name + operation + "." + format_extension

                        output_path = None
                        if save_to_storage:
                            output_path = self.temp_folder + "/" + name + operation + "." + format_extension                    

                        def request_invoker():
                            return self.cad_api.get_drawing_rotate_flip(
                                requests.GetDrawingRotateFlipRequest(name, format_extension, "Rotate180FlipNone", self.original_data_folder, output_path, storage))

                        self.get_request_tester(
                                operation,
                                'Input image: {0}; Output format: {1}, out path: {2}'.format(name, format_extension, output_path),
                                name,
                                output_path,
                                request_invoker,
                                lambda x, y, z: None,
                                folder,
                                reference_file_name,
                                storage)

    def test_post_rotate_flip_image(self):
        """
        Performs RotateFlip (export to another format) operation test with POST
        method, sending input data in request stream.
        """
        
        self.override_reference_files = True
        self.remove_result = False
        additional_export_formats = set()
        if not self.EXTENDED_TEST:
            format_extension_test_cases = ['gif']
        else:
            format_extension_test_cases = ['tiff']

        formats_to_export = set(self.basic_export_formats).union(additional_export_formats)

        for save_to_storage in [True, False]:
            for format_extension in format_extension_test_cases:
                with self.subTest('format_extension: ' + str(format_extension) + ' save to storage: ' + str(save_to_storage)):

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
                        operation = '_rotate_flip_post'

                        reference_file_name = name + operation + "." + format_extension

                        output_path = None
                        if save_to_storage:
                            output_path = folder + "/" + name + operation + "." + format_extension                    

                        def request_invoker(input_stream, out_path):
                            return self.cad_api.post_drawing_rotate_flip(
                                requests.PostDrawingRotateFlipRequest(input_stream, format_extension, "RotateNoneFlipY", output_path, storage))

                        self.post_request_tester(
                                operation,
                                'Input image: {0}; Output format: {1}, out path: {2}'.format(name, format_extension, output_path),
                                name,
                                output_path,
                                request_invoker,
                                lambda x, y, z: None,
                                folder,
                                reference_file_name,
                                storage)

#t = TestRotateFlipApi()
#t.setUp()
#t.test_get_rotate_flip_image()
#t.test_post_rotate_flip_image()