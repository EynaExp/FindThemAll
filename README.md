

# FindThemAll – Lightweight Phishing Simulation Tracker

A minimal, self-contained HTTP tracking tool designed for **authorized security awareness campaigns** and **phishing simulations**.  
When a target clicks your tracked link, detailed browser/environment information is silently collected and dispatched to your Telegram chat in real time.

> ⚠️ **IMPORTANT**  
> This tool is intended **exclusively** for legitimate security testing with **explicit, written authorization** from the system/network owner.  
> Unauthorized use is illegal and unethical. The author assumes no liability for misuse.

---

## 📦 What it collects

| Field              | Source                        |
|--------------------|-------------------------------|
| IP geolocation     | ipinfo.io (city, region, country) |
| IP address         | client-side `window.location.hostname` |
| User-Agent         | `navigator.userAgent`         |
| Platform           | `navigator.platform`          |
| Screen resolution  | `window.screen`               |
| Color depth        | `screen.colorDepth`           |
| Language           | `navigator.language`          |
| Timezone           | `Intl.DateTimeFormat`         |
| Cookies enabled    | `navigator.cookieEnabled`     |
| Java enabled       | `navigator.javaEnabled()`     |
| Browser name/ver   | `navigator.appName/Version`   |
| CPU cores          | `navigator.hardwareConcurrency` |
| JS heap memory     | `performance.memory` (if available) |

All data is saved to `collected_info.json` and forwarded as a beautifully formatted Telegram message.

---

## 🚀 Quick Start

### 1. Prerequisites

- Python **3.6+**
- `pip install requests`

### 2. Create a Telegram Bot

1. Chat with [@BotFather](https://t.me/BotFather) on Telegram.
2. Follow the prompts to create a new bot and obtain its **API token**.
3. Start a chat with your bot and send any message.
4. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` to find your `chat_id` (the `"id"` field inside `"chat"`).

### 3. Configure the Script

Open the Python file and insert your credentials:

```python
TELEGRAM_BOT_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'
CHAT_ID = '987654321'   # your numeric chat ID or @channelusername
```

### 4. Run the Server

```bash
python server.py
```

The server will start on port **5000**.  
For public access you need to expose this port (see [Deployment](#-deployment) below).

---

## 🎯 Usage – Generating Tracked Links

Send your target a URL in this format:

```
http://your-server:5000/track?token=john_q4campaign
```

- Replace `your-server` with your public IP/domain or an ngrok URL.
- `token` is a free-text identifier that will appear in the Telegram message and JSON log – use it to tag each target (e.g., employee name, email address, campaign ID).

When the page loads, the embedded JavaScript immediately:
1. Collects all browser details.
2. Fetches approximate geolocation via `ipinfo.io`.
3. POSTs the full data to `/capture`, which triggers file saving and the Telegram notification.

---

## 📬 Example Telegram Message

```
Tracking Token: john_q4campaign

New Visitor Information:

IP Address: 203.0.113.42
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...
System Info: Win32
Screen Size: 1920 x 1080
Color Depth: 24 bits
Language: en-US
Timezone: America/New_York
Cookies Enabled: true
Java Enabled: false
Platform Version: 5.0 (Windows NT 10.0; Win64; x64) ...
Browser: Netscape
Geolocation: New York, New York, US
CPU Cores: 8
Memory Usage: 12.34 MB
```

---

## 🌍 Deployment (make it publicly reachable)

**Option A – ngrok (quick test)**  
```bash
ngrok http 5000
```
Use the `https://xxxx.ngrok.io` URL it gives you.

**Option B – Reverse Proxy (production-like)**  
Place the server behind **nginx** or **Apache** with HTTPS. This makes the link look more legitimate.

**Option C – Cloud Server**  
Run the script on a VPS, open port 5000 (or change it), and use the public IP.

---

## 📂 Output

- **`collected_info.json`** – append-only log of captured payloads.
- **Telegram chat** – real-time, formatted alerts per visitor.

---

## 🔒 Security & Ethics

- This server is **plain HTTP** by default – use a reverse proxy with TLS for production campaigns.
- It does not persist or serve any malicious content. It is purely a **data collection** endpoint.
- **Always obtain prior written consent** before running phishing simulations.
- Do **not** use this tool to collect real credentials – it is designed for tracking only.
- Respect privacy laws applicable in your jurisdiction (GDPR, etc.).

---

## 📝 License

This project is provided for educational and authorised security testing purposes.  
You are free to use and modify it at your own risk.

---

**Happy (ethical) phishing!** 🎯
```
