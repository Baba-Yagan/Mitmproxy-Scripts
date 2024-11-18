import os
import mitmproxy.http
import uuid
from urllib.parse import urlparse
import time


class FileDumpAddon:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def parse_url(self, url):
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")
        result = [parsed_url.netloc] + path_parts[:-1]
        filename = path_parts[-1].split("?")[0], parsed_url.query
        #print("filename: ", filename)
        return result, filename

    def create_folder_and_filepath(self, url, flow_id, content_type=""):
        url_parts, filename = self.parse_url(url)
        # flow_uuid = f"{flow_id}-{uuid.uuid4()}"
        folder_path = os.path.join(self.output_dir, *url_parts)

        os.makedirs(folder_path, exist_ok=True)

        timestamp = int(time.time())
        file_name_with_timestamp = f"{uuid.uuid4()}-{filename[0]}"
        #print(file_name_with_timestamp)

        file_path = os.path.join(folder_path, file_name_with_timestamp)
        return file_path

    def save_content_to_file(self, content, file_path, headers=False, additional_content=b""):
        mode = "w" if isinstance(content, str) else "wb"
        with open(file_path, mode) as f:
            if headers:
                f.write(b"--HEADERS-START--\n")
                f.write(additional_content+b'\n')
                for k, v in content.fields:
                    f.write(k + b" =-=-= " + v + b"\n")
                f.write(b"--HEADERS-END--\n")
            else:
                f.write(content)


    def request(self, flow: mitmproxy.http.HTTPFlow):
        return
        url = flow.request.url
        file_path = self.create_folder_and_filepath(url, flow.id, "request")
        #print(flow.request.content)
        self.save_content_to_file(flow.request.content, file_path)

        file_path_meta = file_path + ".meta"
        if flow.response is not None:
            if flow.response.headers is not None:
                additional_content = url.encode('utf-8')
                self.save_content_to_file(flow.response.headers, file_path_meta, headers=True, additional_content=additional_content)
            if flow.response.trailers is not None:
                additional_content = url.encode('utf-8')
                self.save_content_to_file(flow.response.trailers, file_path_meta, additional_content=additional_content)

    # Log the arguments
        with open("metalog.log", "a") as log_file:
            log_file.write(f"Request: URL: {url}, File Path: {file_path}\n")

    def response(self, flow: mitmproxy.http.HTTPFlow):
        url = flow.request.url
        file_path = self.create_folder_and_filepath(url, flow.id, "response")
        #print(flow.response.content)
        self.save_content_to_file(flow.response.content, file_path)

        file_path_meta = file_path + ".meta"
        if flow.response is not None:
            if flow.response.headers is not None:
                additional_content = url.encode('utf-8')
                self.save_content_to_file(flow.response.headers, file_path_meta, headers=True, additional_content=additional_content)
            if flow.response.trailers is not None:
                additional_content = url.encode('utf-8')
                self.save_content_to_file(flow.response.trailers, file_path_meta, additional_content=additional_content)

        # Log the arguments
        with open("metalog.log", "a") as log_file:
            log_file.write(f"Response: URL: {url}, File Path: {file_path}\n")


addons = [
    FileDumpAddon(output_dir="DIRECTORY_HERE")
]
