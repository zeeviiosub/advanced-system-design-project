class Website:

    def __init__(self):
        self.functions = {}

    def route(self, path):
        def decorator(f):
            self.functions[path] = f
            return f
        return decorator

    def run(self, address):
        import http.server
        functions = self.functions

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                import re
                path_found = False
                for path_pattern in functions.keys():
                    path_found = re.search(f'^{path_pattern}$', self.path)
                    if path_found:
                        f = functions[path_pattern]
                        args = path_found.groups()
                        break
                if not path_found:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'')
                else:
                    response, data = f(*args)
                    self.send_response(response)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Content-Length', len(data))
                    self.end_headers()
                    self.wfile.write(data.encode())
        http.server.HTTPServer(address, Handler).serve_forever()
