import http.server
import socketserver
import os
import urllib.parse
import cgi

PORT = 8080  # Change this if needed

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        """Serve files and allow directory navigation."""
        if self.path == "/":
            return self.list_directory(os.getcwd())  # Show file listing
        return super().do_GET()  # Serve the file

    def do_POST(self):
        """Handles file uploads from the Web UI."""
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

        if "file" in form:
            file_item = form["file"]
            filename = os.path.basename(file_item.filename)

            if filename:
                # Get the correct upload directory based on URL
                upload_dir = self.translate_path(self.path)

                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                file_path = os.path.join(upload_dir, filename)

                with open(file_path, "wb") as f:
                    f.write(file_item.file.read())

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<script>alert('Upload successful!');window.location=document.referrer;</script>")
                print(f"[+] File uploaded via Web UI: {file_path}")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No file selected for upload")

    def do_PUT(self):
        """Handles file uploads from CLI using curl -T"""
        path = self.translate_path(self.path)
        length = int(self.headers.get("Content-Length", 0))

        if length > 0:
            with open(path, "wb") as f:
                f.write(self.rfile.read(length))

            self.send_response(201, "Created")
            self.end_headers()
            self.wfile.write(f"[+] File uploaded successfully: {path}\n".encode())
            print(f"[+] File uploaded via CLI: {path}")
        else:
            self.send_error(400, "No file data received")

    def list_directory(self, path):
        """Generate directory listing with file download links."""
        try:
            file_list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        file_list.sort(key=lambda a: a.lower())  # Sort files alphabetically
        rel_path = urllib.parse.unquote(self.path)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(f"<!DOCTYPE html><html><head><title>Index of {rel_path}</title></head>".encode())
        self.wfile.write(f"<body><h2>Index of {rel_path}</h2>".encode())

        # Upload form (Web)
        self.wfile.write(b"""
        <form action="" method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form><hr>
        """)

        # Parent directory link
        if rel_path != "/":
            self.wfile.write(b'<a href="..">[Parent Directory]</a><br><br>')

        # List files & folders
        for item in file_list:
            link = urllib.parse.quote(item)  # Encode for URL
            display_name = item + "/" if os.path.isdir(item) else item

            if os.path.isdir(item):
                self.wfile.write(f'<a href="{link}/">{display_name}</a><br>'.encode())
            else:
                self.wfile.write(f'<a href="{link}" download>{display_name}</a><br>'.encode())  # Direct download

        self.wfile.write(b"</body></html>")

if __name__ == '__main__':
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, CustomHTTPRequestHandler)
    print(f"[+] Serving HTTP on port {PORT} (http://127.0.0.1:{PORT})...")
    httpd.serve_forever()
