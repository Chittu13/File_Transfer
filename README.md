# 🔁 Advanced File Transfer Server

A lightweight, cross-platform, zero-dependency HTTP server written in Python that enables file upload and download from any system — through a web browser or command line. Perfect for sharing files across local networks quickly and securely (within trusted environments).

---

## ✅ Features

- 📂 Directory browsing via browser
- 📥 File download via direct links
- ⬆️ File upload via web UI
- 🧾 File upload via `curl` (`PUT` method)
- 📁 Uploads save correctly based on the browser or CLI path
- ⚙️ Works on **Linux**, **macOS**, and **Windows**
- 🚫 No third-party dependencies – 100% standard Python

---

## 💻 Requirements

- Python 3.x (tested on 3.6+)
- Open port (default: `8080`)
- No installation or configuration needed

---

## 🚀 Getting Started

### Clone or Download

```bash
git clone https://github.com/Chittu13/File_Transfer.git
cd File_Transfer
python3 file_server.py
```


## 🌐 Web Interface
  - Open http://<your-ip>:8080/ in your browser.
  - Navigate folders by clicking.
  - Use the upload form to send files to the current folder.
  - Uploaded files will be saved in the exact subdirectory you're viewing.

## 📤 Upload via Command Line (curl)

- You can upload files directly using the PUT method:
  - Upload to root:
    - `curl -T ./example.txt http://<server-ip>:8080/example.txt`


## 🛡 Security Warning

⚠️ This tool is not secure for public/internet-facing use.
  - No authentication or encryption
  - No user restrictions
  - Anyone on the network can access, upload, or download files

Use it only:
  - On local networks
  - For trusted users
  - In controlled environments


---

