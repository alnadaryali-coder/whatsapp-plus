#!/usr/bin/env python3
"""خادم ملفات بسيط لتشغيل تطبيق «صوت إلى نص» محليًا.

يضيف ترويسات COOP/COEP حتى يعمل متصفح كروم بوضع العزل (crossOriginIsolated)
الذي يسرّع معالجة الصوت متعددة الخيوط (WebAssembly).

التشغيل:  python3 serve.py [المنفذ]   (الافتراضي 8080)
ثم افتح:  http://localhost:8080
"""
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format, *args):  # سجل أخف
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    directory = os.path.dirname(os.path.abspath(__file__))
    handler = partial(Handler, directory=directory)
    server = ThreadingHTTPServer(("0.0.0.0", port), handler)
    print(f"🎙️ تطبيق صوت إلى نص يعمل على http://0.0.0.0:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
