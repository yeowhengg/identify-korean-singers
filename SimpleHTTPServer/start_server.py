from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi


class ImageHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        content_type, _ = cgi.parse_header(self.headers['Content-Type'])

        if content_type == 'multipart/form-data':
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )

            file_item = form_data['file']
            if file_item.file:
                full_path = str(file_item.filename).replace(
                    "./images/", "downloaded_images/")
                with open(full_path, 'wb') as f:
                    while True:
                        chunk = file_item.file.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Image received and saved successfully')
                return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'Error: Unable to save the image')


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, ImageHandler)
    print('Server running on port 8001...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
