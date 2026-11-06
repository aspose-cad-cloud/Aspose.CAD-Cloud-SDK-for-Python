#  coding: utf-8
#  ----------------------------------------------------------------
#  <copyright company="Aspose" file="PostDrawingResizeRequest.py">
#    Copyright (c) 2018-2019 Aspose Pty Ltd. All rights reserved.
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
#  -----------------------------------------------------------------

from asposecadcloud.models.requests.cad_request import CadRequest
from asposecadcloud.models.requests.http_request import HttpRequest


class PostDrawingResizeRequest(CadRequest):
    """
    Request model for post_drawing_resize operation.
    Initializes a new instance.

    :param drawing_data Input drawing
    :param output_format Resulting file format.
    :param new_width New width.
    :param new_height New height.
    :param out_path Path to updated file (if this is empty, response contains streamed file).
    :param storage Your Aspose Cloud Storage name.
    """

    def __init__(self, drawing_data, output_format, new_width, new_height, out_path=None, storage=None):
        CadRequest.__init__(self)
        self.drawing_data = drawing_data
        self.output_format = output_format
        self.new_width = new_width
        self.new_height = new_height
        self.out_path = out_path
        self.storage = storage

    def to_http_info(self, config):
        """
        Prepares initial info for HTTP request

        :param config: CAD API configuration
        :type: asposecadcloud.Configuration
        :return: http_request configured http request
        :rtype: Configuration.models.requests.HttpRequest
        """
        # verify the required parameter 'drawing_data' is set
        if self.drawing_data is None:
            raise ValueError("Missing the required parameter `drawing_data` when calling `post_drawing_resize`")
        # verify the required parameter 'output_format' is set
        if self.output_format is None:
            raise ValueError("Missing the required parameter `output_format` when calling `post_drawing_resize`")
        # verify the required parameter 'new_width' is set
        if self.new_width is None:
            raise ValueError("Missing the required parameter `new_width` when calling `post_drawing_resize`")
        # verify the required parameter 'new_height' is set
        if self.new_height is None:
            raise ValueError("Missing the required parameter `new_height` when calling `post_drawing_resize`")

        collection_formats = {}
        path = '/cad/resize/{outputFormat}'
        path_params = {}

        query_params = []
        if self._lowercase_first_letter('outputFormat') in path:
            path = path.replace('{' + self._lowercase_first_letter('outputFormat' + '}'), self.output_format if self.output_format is not None else '')
        else:
            if self.output_format is not None:
                query_params.append((self._lowercase_first_letter('outputFormat'), self.output_format))
        if self._lowercase_first_letter('newWidth') in path:
            path = path.replace('{' + self._lowercase_first_letter('newWidth' + '}'), self.new_width if self.new_width is not None else '')
        else:
            if self.new_width is not None:
                query_params.append((self._lowercase_first_letter('newWidth'), self.new_width))
        if self._lowercase_first_letter('newHeight') in path:
            path = path.replace('{' + self._lowercase_first_letter('newHeight' + '}'), self.new_height if self.new_height is not None else '')
        else:
            if self.new_height is not None:
                query_params.append((self._lowercase_first_letter('newHeight'), self.new_height))
        if self._lowercase_first_letter('outPath') in path:
            path = path.replace('{' + self._lowercase_first_letter('outPath' + '}'), self.out_path if self.out_path is not None else '')
        else:
            if self.out_path is not None:
                query_params.append((self._lowercase_first_letter('outPath'), self.out_path))
        if self._lowercase_first_letter('storage') in path:
            path = path.replace('{' + self._lowercase_first_letter('storage' + '}'), self.storage if self.storage is not None else '')
        else:
            if self.storage is not None:
                query_params.append((self._lowercase_first_letter('storage'), self.storage))

        header_params = {}

        form_params = []
        local_var_files = []
        if self.drawing_data is not None:
            local_var_files.append((self._lowercase_first_letter('drawingData'), self.drawing_data))

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self._select_header_accept(
            ['application/json'])

        # HTTP header `Content-Type`
        header_params['Content-Type'] = 'multipart/form-data' if form_params or local_var_files else self._select_header_content_type(
            ['application/octet-stream', 'multipart/form-data'])

        # Authentication setting
        auth_settings = ['Bearer']

        return HttpRequest(path, path_params, query_params, header_params, form_params, body_params, local_var_files,
                           collection_formats, auth_settings)
