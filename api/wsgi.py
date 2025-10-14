from demostocks.wsgi import application

# Vercel uses the variable 'app' or 'application' as the entrypoint.
app = application

if __name__ == '__main__':
    # Simple run for local testing if needed
    from wsgiref.simple_server import make_server
    httpd = make_server('127.0.0.1', 8000, app)
    print('Serving on http://127.0.0.1:8000')
    httpd.serve_forever()
