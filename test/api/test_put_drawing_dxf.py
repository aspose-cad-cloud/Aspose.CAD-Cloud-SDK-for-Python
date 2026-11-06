#  coding: utf-8
#  ----------------------------------------------------------------------------
#  <copyright company="Aspose" file="test_rotate_flip_api.py">
#    Copyright (c) 2026 Aspose Pty Ltd. All rights reserved.
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

import os
import json
import asposecadcloud.models.requests as requests
from test.api import CadApiTester


class TestPutDrawing(CadApiTester):
    """
    Tests for PUT drawing conversion methods.

    The test uses the common ApiTester infrastructure:
    - input files are taken from TestData;
    - files are uploaded by ApiTester.setUp();
    - request results are saved to CadCloudTestPython;
    - result files are compared with ReferenceData by ApiTester.
    """

    DEFAULT_INPUT_DXF = "910609.dxf"
    SVG_INPUT_FILE = "input_simplified.svg"

    def _assert_drawing_size(
        self,
        output_file,
        expected_height,
        expected_width,
        delta=0.01):
        """
        Checks the size of the result via post_drawing_properties.
        """

        self.assertTrue(
            os.path.isfile(output_file),
            "Output file was not found: {0}".format(output_file)
        )
        
        request = requests.PostDrawingPropertiesRequest(output_file)
        properties = self.cad_api.post_drawing_properties(request)

        actual_height = float(properties.height)
        actual_width = float(properties.width)

        self.assertAlmostEqual(
            expected_height,
            actual_height,
            delta=delta,
            msg=(
                "Unexpected drawing height for {0}: "
                "expected {1}, actual {2}"
            ).format(
                output_file,
                expected_height,
                actual_height
            )
        )

        self.assertAlmostEqual(
            expected_width,
            actual_width,
            delta=delta,
            msg=(
                "Unexpected drawing width for {0}: "
                "expected {1}, actual {2}"
            ).format(
                output_file,
                expected_width,
                actual_width
            )
        )

    def _get_request_class(self, class_names):
        """
        Returns the first request class available.
        """
        for class_name in class_names:
            request_class = getattr(requests, class_name, None)

            if request_class is not None:
                return request_class

        raise AttributeError(
            "None of the request classes exists: {0}".format(
                ", ".join(class_names)
            )
        )

    def _create_put_request(
            self,
            request_class_names,
            input_path,
            output_path,
            export_options=None):
        """
        Creates a generated PUT request.
        """
        request_class = self._get_request_class(request_class_names)

        arguments = {
            "drawing_data": input_path,
            "out_path": output_path
        }

        if export_options is not None:
            arguments["export_options"] = export_options

        try:
            return request_class(**arguments)
        except TypeError:
            if export_options is None:
                return request_class(input_path, output_path)

            return request_class(
                input_path,
                output_path,
                export_options
            )

    def _invoke_put(
            self,
            api_method_name,
            request_class_names,
            input_path,
            output_path,
            export_options=None):
        """
        Creates a request and invokes the corresponding CadApi method.
        """
        request = self._create_put_request(
            request_class_names=request_class_names,
            input_path=input_path,
            output_path=output_path,
            export_options=export_options
        )

        api_method = getattr(self.cad_api, api_method_name)

        return api_method(request)

    def _run_put_test(
            self,
            test_method_name,
            api_method_name,
            request_class_names,
            input_file_name,
            output_file_name,
            reference_file_name=None,
            export_options=None):
        """
        Runs one PUT conversion through ApiTester.put_request_tester().
        """
        if reference_file_name is None:
            reference_file_name = output_file_name

        result_file_name = "{0}/{1}".format(
            self.temp_folder,
            output_file_name
        )

        parameters_line = (
            "Input file: {0}; output file: {1}; request: {2}"
        ).format(
            input_file_name,
            result_file_name,
            api_method_name
        )

        self.put_request_tester(
            test_method_name=test_method_name,
            parameters_line=parameters_line,
            input_file_name=input_file_name,
            result_file_name=result_file_name,
            request_invoker=lambda input_path, output_path: (
                self._invoke_put(
                    api_method_name=api_method_name,
                    request_class_names=request_class_names,
                    input_path=input_path,
                    output_path=output_path,
                    export_options=export_options
                )
            ),
            properties_tester=None,
            folder=self.original_data_folder,
            reference_file_name=reference_file_name,
            storage=self.default_storage
        )

    def _put_drawing_test(
            self,
            test_method_name,
            api_method_name,
            request_class_names,
            input_file_name,
            output_file_name,
            expected_height,
            expected_width,
            reference_file_name=None,
            export_options=None):
        """
        Executes a PutDrawing request, checks the reference file, and additionally checks the height orwidth of the result.
        """

        self._run_put_test(
            test_method_name,
            api_method_name,
            request_class_names,
            input_file_name,
            output_file_name,
            reference_file_name,
            export_options
        )

        output_file = os.path.join(
            self._local_reference_data,
            output_file_name
        )

        self._assert_drawing_size(
            output_file,
            expected_height,
            expected_width
        )

    def _get_dxf_export_options(self):
        """
        Export options.

        The source SVG dimensions are converted from pixels to inches.
        """
        input_path = self.cad_api.download_file(
            requests.DownloadFileRequest(
                path="{0}/{1}".format(
                    self.original_data_folder,
                    self.SVG_INPUT_FILE
                ),
                storage_name=self.default_storage
            )
        )

        properties = self.cad_api.post_drawing_properties(
            requests.PostDrawingPropertiesRequest(input_path)
        )

        initial_height = float(properties.height)
        initial_width = float(properties.width)

        self.assertAlmostEqual(
            2357.0,
            initial_height,
            delta=0.01
        )

        self.assertAlmostEqual(
            2273.0,
            initial_width,
            delta=0.01
        )

        mm_per_inch = 25.4
        ratio = 1.0 / 0.9923130037

        page_width = initial_width * ratio / mm_per_inch
        page_height = initial_height * ratio / mm_per_inch

        return json.dumps({
            "VectorRasterizationOptions": {
                "PageHeight": page_height,
                "PageWidth": page_width
            }
        })

    def test_put_drawing_dxf(self):
        """
        Converts input_simplified.svg to DXF.

        This test requires the following files:

        TestData/input_simplified.svg
        ReferenceData/input_simplified.dxf
        """
        self.override_reference_files = True
        self.remove_result = False
        height_expected = 11.0
        widht_expected = 15.0
        export_options = self._get_dxf_export_options()

        self._put_drawing_test(
            test_method_name="PutDrawingDxf",
            api_method_name="put_drawing_dxf",
            request_class_names=(
                "PutDrawingDxfRequest",
            ),
            input_file_name=self.SVG_INPUT_FILE,
            output_file_name="input_simplified.dxf",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="input_simplified.dxf",
            export_options=export_options
        )

    def test_put_drawing_png(self):
        """
        Converts 910609.dxf to PNG.

        Required reference file:

        ReferenceData/910609.png
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 200.0
        widht_expected = 200.0
        self._put_drawing_test(
            test_method_name="PutDrawingPng",
            api_method_name="put_drawing_png",
            request_class_names=(
                "PutDrawingPngRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.png",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.png",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_bmp(self):
        """
        Converts 910609.dxf to BMP.

        Required reference file:

        ReferenceData/910609.bmp
        """
        self.override_reference_files = True
        self.remove_result = False
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 200.0
        widht_expected = 200.0
        self._put_drawing_test(
            test_method_name="PutDrawingBmp",
            api_method_name="put_drawing_bmp",
            request_class_names=(
                "PutDrawingBmpRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.bmp",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.bmp",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_cgm(self):
        """
        Converts 910609.dxf to CGM.

        Required reference file:

        ReferenceData/910609.cgm
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 414.0
        widht_expected = 617.0
        self._put_drawing_test(
            test_method_name="PutDrawingCgm",
            api_method_name="put_drawing_cgm",
            request_class_names=(
                "PutDrawingCgmRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.cgm",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.cgm",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_dwf(self):
        """
        Converts 910609.dxf to DWF.

        Required reference file:

        ReferenceData/910609.dwf
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 150.0
        widht_expected = 150.0
        self._put_drawing_test(
            test_method_name="PutDrawingDwf",
            api_method_name="put_drawing_dwf",
            request_class_names=(
                "PutDrawingDwfRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.dwf",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.dwf",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_fbx(self):
        """
        Converts 910609.dxf to FBX.

        Required reference file:

        ReferenceData/910609.fbx
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 98.0
        widht_expected = 149.0
        self._put_drawing_test(
            test_method_name="PutDrawingFbx",
            api_method_name="put_drawing_fbx",
            request_class_names=(
                "PutDrawingFbxRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.fbx",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.fbx",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_gif(self):
        """
        Converts 910609.dxf to GIF.

        Required reference file:

        ReferenceData/910609.gif
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 200.0
        widht_expected = 200.0
        self._put_drawing_test(
            test_method_name="PutDrawingGif",
            api_method_name="put_drawing_gif",
            request_class_names=(
                "PutDrawingGifRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.gif",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.gif",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_glb(self):
        """
        Converts 910609.dxf to GLB.

        Required reference file:

        ReferenceData/910609.glb
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 97.0
        widht_expected = 149.0
        self._put_drawing_test(
            test_method_name="PutDrawingGlb",
            api_method_name="put_drawing_glb",
            request_class_names=(
                "PutDrawingGlbRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.glb",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.glb",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_gltf(self):
        """
        Converts 910609.dxf to GLTF.

        Required reference file:

        ReferenceData/910609.gltf
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 97.0
        widht_expected = 149.0
        self._put_drawing_test(
            test_method_name="PutDrawingGltf",
            api_method_name="put_drawing_gltf",
            request_class_names=(
                "PutDrawingGltfRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.gltf",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.gltf",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_jpeg(self):
        """
        Converts 910609.dxf to JPEG.

        Required reference file:

        ReferenceData/910609.jpeg
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 200.0
        widht_expected = 200.0
        self._put_drawing_test(
            test_method_name="PutDrawingJpeg",
            api_method_name="put_drawing_jpeg",
            request_class_names=(
                "PutDrawingJpegRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.jpeg",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.jpeg",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_obj(self):
        """
        Converts 910609.dxf to OBJ.

        Required reference file:

        ReferenceData/910609.obj
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 97.0
        widht_expected = 149.0
        self._put_drawing_test(
            test_method_name="PutDrawingObj",
            api_method_name="put_drawing_obj",
            request_class_names=(
                "PutDrawingObjRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.obj",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.obj",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_psd(self):
        """
        Converts 910609.dxf to PSD.

        Required reference file:

        ReferenceData/910609.psd
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 200.0
        widht_expected = 200.0
        self._put_drawing_test(
            test_method_name="PutDrawingPsd",
            api_method_name="put_drawing_psd",
            request_class_names=(
                "PutDrawingPsdRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.psd",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.psd",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_stp(self):
        """
        Converts 910609.dxf to STP.

        Required reference file:

        ReferenceData/910609.stp
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 97.0
        widht_expected = 149.0
        self._put_drawing_test(
            test_method_name="PutDrawingStp",
            api_method_name="put_drawing_stp",
            request_class_names=(
                "PutDrawingStpRequest",
                "PutDrawingSTPRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.stp",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.stp",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_svg(self):
        """
        Converts 910609.dxf to SVG.

        Required reference file:

        ReferenceData/910609.svg
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 200.0
        widht_expected = 200.0
        self._put_drawing_test(
            test_method_name="PutDrawingSvg",
            api_method_name="put_drawing_svg",
            request_class_names=(
                "PutDrawingSvgRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.svg",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.svg",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_three_ds(self):
        """
        Converts 910609.dxf to 3DS.

        Different generated SDK versions can expose the request model
        with different capitalization.
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 97.0
        widht_expected = 149.0
        self._put_drawing_test(
            test_method_name="PutDrawingThreeDs",
            api_method_name="put_drawing_three_ds",
            request_class_names=(
                "PutDrawing3dsRequest",
                "PutDrawing3DSRequest",
                "PutDrawingThreeDsRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.3ds",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.3ds",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )

    def test_put_drawing_tiff(self):
        """
        Converts 910609.dxf to TIFF.

        Required reference file:

        ReferenceData/910609.tiff
        """
        self.override_reference_files = True
        self.remove_result = False
        height = 200.0
        widht = 200.0
        height_expected = 200.0
        widht_expected = 200.0
        self._put_drawing_test(
            test_method_name="PutDrawingTiff",
            api_method_name="put_drawing_tiff",
            request_class_names=(
                "PutDrawingTiffRequest",
            ),
            input_file_name=self.DEFAULT_INPUT_DXF,
            output_file_name="910609.tiff",
            expected_height=height_expected,
            expected_width=widht_expected,
            reference_file_name="910609.tiff",
            export_options="{\"VectorRasterizationOptions\": {\"PageHeight\":" + format(height, ".10g") + ",\"PageWidth\":" + format(widht, ".10g") + "}}"
        )