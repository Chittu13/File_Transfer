import SimpleHTTPServer
import BaseHTTPServer
import os
import urllib
import cgi
import sys
import signal

DEFAULT_PORT = 8080  # Default if none provided


class MaliciousHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        """Serve files correctly and allow directory navigation."""
        path = self.translate_path(self.path)

        if os.path.isdir(path):
            return self.list_directory(path)  # Show directory listing
        elif os.path.isfile(path):
            return self.serve_file(path)  # Serve the file for download
        else:
            self.send_error(404, "File not found")

    def serve_file(self, path):
        """Serve the requested file for download."""
        try:
            with open(path, 'rb') as f:
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition",
                                 "attachment; filename={}".format(os.path.basename(path)))
                self.end_headers()
                self.wfile.write(f.read())  # Send file content
        except IOError:
            self.send_error(404, "File not found")

    def do_PUT(self):
        """Handles file uploads from CLI (curl -T <file> http://server)."""
        path = self.translate_path(self.path)
        length = int(self.headers.get("Content-Length", 0))

        if length > 0:
            with open(path, "wb") as dst:
                dst.write(self.rfile.read(length))

            self.send_response(201, "Created")
            self.end_headers()
            self.wfile.write("[+] File uploaded successfully: {}\n".format(path))
            print("[+] File uploaded via CLI: {}".format(path))
        else:
            self.send_error(400, "No file data received")

    def do_POST(self):
        """Handles file uploads from the Web UI."""
        print("[+] Received file upload request")
        path = self.translate_path(self.path)
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={'REQUEST_METHOD': 'POST'})

        if "file" in form:
            file_item = form["file"]
            filename = os.path.basename(file_item.filename)

            if filename:
                save_path = os.path.join(path, filename)
                with open(save_path, "wb") as f:
                    f.write(file_item.file.read())

                self.send_response(200)
                self.end_headers()
                self.wfile.write("<script>alert('Upload successful!');window.location=document.referrer;</script>")
                print("[+] File uploaded via Web UI: {}".format(save_path))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write("No file selected for upload")
                print("[-] No file uploaded")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Invalid request")
            print("[-] Invalid upload request")

    def list_directory(self, path):
        """Generate a proper directory listing with file download links."""
        try:
            file_list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return

        file_list.sort(key=lambda a: a.lower())  # Sort files alphabetically
        rel_path = urllib.unquote(self.path)  # Decode URL path

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write("<!DOCTYPE html>")
        self.wfile.write("<html><head><title>Index of {}</title></head>".format(rel_path))
        self.wfile.write("<body><h2>Index of {}</h2>".format(rel_path))

        # Upload form (Web)
        self.wfile.write("""
        <form action="" method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form><hr>
        """)

        # Parent directory link
        if rel_path != "/":
            self.wfile.write('<a href="..">[Parent Directory]</a><br><br>')

        # List files and folders with correct links
        for item in file_list:
            full_path = os.path.join(path, item)
            display_name = item + "/" if os.path.isdir(full_path) else item
            link = urllib.quote(item)  # Encode for URL

            if os.path.isdir(full_path):
                self.wfile.write('<a href="{}/">{}</a><br>'.format(link, display_name))
            else:
                self.wfile.write('<a href="{}" download>{}</a><br>'.format(link, display_name))  # Direct download link

        self.wfile.write("</body></html>")


def get_port():
    """Get port from CLI args or ask user input."""
    if len(sys.argv) > 1:
        try:
            return int(sys.argv[1])
        except ValueError:
            print("[!] Invalid port provided. Falling back to default.")
            return DEFAULT_PORT
    else:
        try:
            user_input = raw_input("Enter port to use (default {}): ".format(DEFAULT_PORT)).strip()
        except NameError:
            # Fallback in case of python3 accidentally
            user_input = input("Enter port to use (default {}): ".format(DEFAULT_PORT)).strip()

        if user_input.isdigit():
            return int(user_input)
        return DEFAULT_PORT


if __name__ == '__main__':
    PORT = get_port()
    server_address = ('', PORT)
    httpd = BaseHTTPServer.HTTPServer(server_address, MaliciousHTTPRequestHandler)
    print("[+] Malicious HTTP server running on port {}...".format(PORT))

    # Graceful shutdown on Ctrl+C
    def shutdown_handler(signum, frame):
        print("\n[!] Shutting down server gracefully...")
        httpd.server_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)

    httpd.serve_forever()
