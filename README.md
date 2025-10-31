# 🚀 ClipDrop — Android ↔ macOS

## 🧠 Problem It Solves
Transferring files or clipboard content between **Android** and **macOS** devices isn’t as seamless as Apple’s AirDrop.  
Typical methods — like **WhatsApp Web**, **Google Drive**, or **email** — are either **slow**, **storage-inefficient**, or **limited by file size**.  

**ClipDrop** bridges this gap by creating a **direct, low-latency bridge** between Android and macOS using a mix of **HTTP, AWS S3, and Bluetooth Low Energy**.  
You can instantly copy text or share files from Android → macOS or vice versa — no cables, no third-party apps, no delay.

---

## ⚙️ Technologies Used
- **HTTP Server:** Node.js (deployed on Render)
- **macOS Daemon:** Python (clipboard listener + BLE event handling)
- **Android App:** Java (handles upload, download, and BLE sync)
- **Cloud Storage:** AWS S3 (pre-signed URL system for lightweight transfers)
- **Authentication:** Google OAuth (JWT-based)
- **Local Communication:** Bluetooth Low Energy (for event signaling between devices)

---

## ✨ Current Features
- 🔒 **JWT-based authentication** via Google OAuth  
- ☁️ **Pre-signed URL uploads** directly to S3 (no proxying through the backend)  
- 🧠 **Clipboard sync:** Copies text between Android ↔ macOS  
- 📁 **File sharing:** Share files like images or documents instantly  
- 🔔 **Bluetooth event triggers** to notify the macOS daemon when new clipboard or storage content is available  
- 🪶 **Lightweight metadata model:**  
  Uses a structured naming convention in S3 —  

- Hashed(JWT_TOKEN)__DELIMIT__Clipboard__DELIMIT__filename.ext
- Hashed(JWT_TOKEN)__DELIMIT__Storage__DELIMIT__filename.ext

This removes the need for a dedicated database such as Redis.

---

## 🧩 What’s Missing
- ❌ **Cross-platform clipboard integration** for Windows and Ubuntu
- ⚠️ **End-to-end encryption** for clipboard data
- 🪪 **Multi-device account linking** (currently one Android ↔ one Mac)  
- 🧱 **UI layer** for viewing and managing transferred files  
- 🧹 **Error handling & reconnection logic** for BLE and S3 network drops

---

## 🗺️ Roadmap / What’s Next
- [ ] Add **Windows daemon** using Python for clipboard sync
- [ ] Implement **Ubuntu version** with custom clipboard save logic 
- [ ] Add **file preview and history** on both Android & macOS
- [ ] Encrypt clipboard data before uploading to S3
- [ ] Build a **unified desktop UI** for managing transfers and logs
- [ ] Publish as an open-source project for community testing

---

## 🎥 Working Demo
📹 [Watch the Demo on Google Drive](https://drive.google.com/file/d/1ynCqExnk03fH_ekab2kql1sqX_sU2of0/view?usp=drivesdk)

---

## 🧩 Summary
This project started as a **personal experiment** to recreate Apple-like ecosystem functionality between **Android and macOS**.  
While not production-grade yet, it demonstrates a fully functional **cross-device communication architecture** blending **BLE**, **cloud storage**, and **automation scripts**.  
The next iterations will focus on **scalability, encryption, and UI polish**.
