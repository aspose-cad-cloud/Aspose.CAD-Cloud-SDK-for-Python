#  coding: utf-8
#  ----------------------------------------------------------------------------
#  <copyright company="Aspose" file="api_tester.py">
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

import os

import getpass
import json
import os
from distutils.util import strtobool
import shutil

import six

import asposecadcloud.models.requests as requests
from asposecadcloud.api_client import ApiClient
from asposecadcloud import CadApi

if six.PY2:
    import unittest2 as unittest
else:
    import unittest


class ApiTester(unittest.TestCase):
    EXTENDED_TEST = False

    def setUp(self):
        self.failed_any_test = False
        self.default_storage = 'Cad-QA'
        self.cloud_test_folder_prefix = 'CadCloudTestPython'
        self.original_data_folder = 'CadCloudTestPythonData'
        self._server_access_file = 'serverAccess.json'
        self._api_version = 'v3.0'
        self._local_test_folder = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'TestData/')
        self._local_reference_data = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ReferenceData/')
        self.remove_result = True
        self.override_reference_files = False

        self.temp_folder = self.cloud_test_folder_prefix

        self.basic_export_formats = ['.dwg',
                                     '.dxf',
                                     '.dgn',
                                     '.stl',
                                     '.dwf']

        self.basic_raster_export_formats = ['.png']

        self.test_storage = os.environ.get('StorageName')
        if not self.test_storage:
            print('Storage name is not set by environment variable. Using the default one.')
            self.test_storage = self.default_storage

        self.__create_api_instance()

        folderExists = self.cad_api.object_exists(requests.ObjectExistsRequest(path = self.temp_folder, storage_name = self.test_storage))
        if not folderExists.exists:
            self.cad_api.create_folder(requests.CreateFolderRequest(path = self.temp_folder, storage_name = self.test_storage))

    def tearDown(self):
        if not self.failed_any_test and self.remove_result and self.cad_api.object_exists(requests.ObjectExistsRequest(path = self.temp_folder, storage_name = self.test_storage)).exists:
            self.cad_api.delete_folder(requests.DeleteFolderRequest(path = self.temp_folder, storage_name = self.test_storage))

    def __create_api_instance(self):
        print('Trying to obtain configuration from environment variables.')
        on_premise = True if os.environ.get('OnPremise') and \
                             bool(strtobool(os.environ.get('OnPremise'))) \
            else False
        app_key = None if on_premise else os.environ.get('AppKey')
        app_sid = None if on_premise else os.environ.get('AppSid')
        base_url = os.environ.get('ApiEndpoint')
        api_version = os.environ.get('ApiVersion')
        proxy = None

        if (not on_premise and (
                not app_key or not app_sid)) or not base_url or not api_version:
            print('Access data isn\'t set completely by environment variables.'
                  ' Filling unset data with default values.')

        if not api_version:
            api_version = self._api_version
            print('Set default API version')

        server_access_info = os.path.join(
            self._local_test_folder, self._server_access_file)
        with open(server_access_info) as f:
            server_file_info = json.load(f)

        if server_file_info:
            if not app_key and not on_premise:
                app_key = server_file_info['AppKey']
                print('Set default App key')

            if not app_sid and not on_premise:
                app_sid = server_file_info['AppSid']
                print('Set default App SID')

            if not base_url:
                base_url = server_file_info['BaseURL']
                print('Set default Base URL')

            if server_file_info['Storage'] and not on_premise:
                self.test_storage = server_file_info['Storage']
                self.default_storage = server_file_info['Storage']
                print('Set default and test storage')

            if 'Proxy' in server_file_info and not on_premise:
                proxy = server_file_info['Proxy']
                print('Set proxy')

        if (not on_premise and (
                not app_key or not app_sid)) or not base_url or not api_version:
            raise ValueError(
                'Please, specify valid access data (AppKey, AppSid, Base URL)')

        print('On Premise: ' + str(on_premise))
        if not on_premise:
            print('App key: ' + app_key)
            print('App SID: ' + app_sid)

        print('Storage: ' + self.test_storage)
        print('Base URL: ' + base_url)
        print('API version: ' + api_version)

        self.cad_api = CadApi(app_key, app_sid, base_url, api_version, False, proxy)

        testFolderExists = self.cad_api.object_exists(requests.ObjectExistsRequest(path=self.original_data_folder, storage_name=self.test_storage))
        if not testFolderExists.exists:
            self.cad_api.create_folder(requests.CreateFolderRequest(path=self.original_data_folder, storage_name=self.test_storage))

        # Getting an up-to-date list of files in the remote storage.
        self.input_test_files = self.cad_api.get_files_list(requests.GetFilesListRequest(
            path=self.original_data_folder,
            storage_name=self.test_storage)).value

        # Extract only file names from the remote list for quick search.
        remote_file_names = {os.path.basename(f.path) for f in self.input_test_files}

        # Collecting the names of all non-JSON files from the local folder.
        local_file_names = {
            filename for filename in os.listdir(self._local_test_folder)
            if not filename.endswith(".json")
        }

        # Calculating the difference: files that are locally available but not in the remote storage.
        files_to_sync = local_file_names - remote_file_names

        # Perform the upload only if missing files are found.
        if files_to_sync:
            for filename in files_to_sync:
                remote_file_name = f"{self.original_data_folder}/{filename}"
        
                if not self.cad_api.object_exists(requests.ObjectExistsRequest(
                    path=remote_file_name, 
                    storage_name=self.test_storage
                )).exists:
                    f = f"{self._local_test_folder}/{filename}"
                    self.cad_api.upload_file(requests.UploadFileRequest(
                        remote_file_name, 
                        f, 
                        storage_name=self.test_storage
                    ))

            # Updating the list of files after the upload is completed.
            self.input_test_files = self.cad_api.get_files_list(requests.GetFilesListRequest(
                path=self.original_data_folder,
                storage_name=self.test_storage)).value

    def __request_tester(
            self,
            test_method_name,
            out_path,
            parameters_line,
            input_file_name,
            invoke_request_action,
            properties_tester,
            folder,
            storage=None):
        if not storage:
            storage = self.default_storage

        print(test_method_name)

        if not self._check_input_file_exists(input_file_name):
            raise ValueError(
                "Input file {0} doesn't exist in the specified storage folder: {1}. Please, upload it first.".format(input_file_name, folder))

        passed = False

        try:
            print(parameters_line)

            result_properties = None
            response = invoke_request_action()

            if out_path:
                result_info = self._get_storage_file_info(out_path, storage)
                if not result_info:
                    raise ValueError(
                        "Result file {0} doesn't exist in the specified storage folder. "
                        "Result isn't present in the storage by an unknown reason.".format(out_path))

            passed = True

        except Exception as e:
            self.failed_any_test = True
            print(str(e))
            raise
        finally:
            if passed and out_path and self.remove_result:
                self.cad_api.delete_file(requests.DeleteFileRequest(path=out_path, storage_name=storage))
                
            print("Test passed: " + str(passed) + os.linesep)

    def get_request_tester(
            self,
            test_method_name,
            parameters_line,
            input_file_name,
            out_path,
            request_invoker,
            properties_tester,
            folder,
            reference_file_name,
            storage=None):
        if not storage:
            storage = self.default_storage

        self.__request_tester(
            test_method_name,
            out_path,
            parameters_line,
            input_file_name,
            lambda: self._obtain_get_response(request_invoker, out_path, storage, reference_file_name),
            properties_tester,
            folder,
            storage)

    def post_request_tester(
            self,
            test_method_name,
            parameters_line,
            input_file_name,
            result_file_name,
            request_invoker,
            properties_tester,
            folder,
            reference_file_name,
            storage=None):
        if not storage:
            storage = self.default_storage

        self.__request_tester(
            test_method_name,
            result_file_name,
            parameters_line,
            input_file_name,
            lambda: self._obtain_post_response(
                os.path.join(folder, input_file_name),
                result_file_name,
                storage,
                request_invoker,
                reference_file_name),
            properties_tester,
            folder,
            storage)

    def put_request_tester(
            self,
            test_method_name,
            parameters_line,
            input_file_name,
            result_file_name,
            request_invoker,
            properties_tester,
            folder,
            reference_file_name,
            storage=None):
        if not storage:
            storage = self.default_storage

        self.__request_tester(
            test_method_name,
            result_file_name,
            parameters_line,
            input_file_name,
            lambda: self._obtain_post_response(
                os.path.join(folder, input_file_name),
                result_file_name,
                storage,
                request_invoker,
                reference_file_name),
            properties_tester,
            folder,
            storage)

    def _check_input_file_exists(self, input_file_name):
        return any(input_file_name == storage_file_info.name for storage_file_info in self.input_test_files)

    def _get_storage_file_info(self, full_file_name, storage):
        parts = full_file_name.split("/")
        folder = parts[0]
        file_name = parts[1]

        file_list_response = self.cad_api.get_files_list(requests.GetFilesListRequest(path=folder, storage_name=storage)).value

        for storage_file_info in file_list_response:
            if storage_file_info.name == file_name:
                return storage_file_info
                
        return None

    def _obtain_get_response(self, request_invoker, output_path, storage, reference_file_name):
        response = request_invoker()

        self.assertIsNotNone(response)

        if output_path:
            response = self.cad_api.download_file(requests.DownloadFileRequest(path=output_path, storage_name=storage))

        if self.override_reference_files:
            shutil.copyfile(response, self._local_reference_data + reference_file_name)

        self.assertEqual(os.path.getsize(response), os.path.getsize(self._local_reference_data + reference_file_name))
        return response

    def _obtain_post_response(
            self,
            input_path,
            out_path,
            storage,
            request_invoker,
            reference_file_name=None):
        res = self.cad_api.download_file(requests.DownloadFileRequest(input_path, storage))

        response = request_invoker(res, out_path)

        if out_path:
            response = self.cad_api.download_file(requests.DownloadFileRequest(path=out_path, storage_name=storage))

        if out_path and reference_file_name is None:
            return None

        if self.override_reference_files:
            shutil.copyfile(response, self._local_reference_data + reference_file_name)

        self.assertEqual(os.path.getsize(response), os.path.getsize(self._local_reference_data + reference_file_name))

        return response
