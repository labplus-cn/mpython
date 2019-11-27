import usocket
import time,os
class Response:

  def __init__(self, f):
    self.raw = f
    self.encoding = "utf-8"
    self._cached = None

  def close(self):
    if self.raw:
      self.raw.close()
      self.raw = None
    self._cached = None

  @property
  def content(self):
    if self._cached is None:
      self._cached = self.raw.read()
      self.raw.close()
      self.raw = None
    return self._cached

  @property
  def text(self):
    return str(self.content, self.encoding)

  def json(self):
    import ujson
    return ujson.loads(self.content)
    
  def recv(self, dataLen):
    dat = self.raw.read(dataLen)
    return dat

def request(method, url, data=None, json=None, headers={}, stream=None,params=None,files=None):
  try:
    proto, dummy, host, path = url.split("/", 3)
  except ValueError:
    proto, dummy, host = url.split("/", 2)
    path = ""
  if proto == "http:":
    port = 80
  elif proto == "https:":
    import ussl
    port = 443
  else:
    raise ValueError("Unsupported protocol: " + proto)

  if ":" in host:
    host, port = host.split(":", 1)
    port = int(port)
    
  if params:
    path = path + "?"
    for k in params:
      path = path + '&'+k+'='+params[k]

  ai = usocket.getaddrinfo(host, port)
  addr = ai[0][4]
  s = usocket.socket()
  s.connect(addr)
  if proto == "https:":
    s = ussl.wrap_socket(s)
  s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
  if not "Host" in headers:
    s.write(b"Host: %s\r\n" % host)
  # Iterate over keys to avoid tuple alloc
  for k in headers:
    s.write(k)
    s.write(b": ")
    s.write(headers[k])
    s.write(b"\r\n")
  if json is not None:
    assert data is None
    import ujson
    data = ujson.dumps(json)
  if data:
    s.write(b"Content-Length: %d\r\n" % len(data))

  if files:
    boundary = '------WebKitFormBoundary'+hex(int(time.time()))
    s.write(b"Content-Type: multipart/form-data; boundary=%s\r\n" % boundary ) 
    s.write(b"Connection: keep-alives\r\n" )
    name = list(files.keys())[0]
    file_dir = files.get(name)[0]
    file_type = files.get(name)[1]
    file_size = os.stat(file_dir)[6]
    file_name = file_dir.split('/')[-1]
    file = open(file_dir, 'rb')
    content_disposition = b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' %(name,file_name)
    content_type = b"Content-Type: %s\r\n" % file_type
    content_length = len(boundary*2)+len(content_disposition)+len(content_type)+file_size+16
    s.write(b"Content-Length: %d\r\n" % content_length)
   
  s.write(b"\r\n")

# body
  if data:
    s.write(data)

  if files:
    # first boundary
    s.write(b"--%s\r\n" % boundary)
    s.write(b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' %(name,file_name))
    s.write(b"Content-Type: %s\r\n" % file_type)
    s.write(b"\r\n")
    # file data for hex
    while True:
      _read = file.read(1024)
      if _read !=b'':
        s.write(_read)
      else:
        break
    # end boundary
    s.write(b"\r\n--%s--\r\n" % boundary)
    file.close()

  l = s.readline()
  protover, status, msg = l.split(None, 2)
  status = int(status)
  #print(protover, status, msg)
  while True:
    l = s.readline()
    if not l or l == b"\r\n":
      break
        #print(l)
    if l.startswith(b"Transfer-Encoding:"):
      if b"chunked" in l:
        raise ValueError("Unsupported " + l)
    elif l.startswith(b"Location:") and not 200 <= status <= 299:
      raise NotImplementedError("Redirects not yet supported")

  resp = Response(s)
  resp.status_code = status
  resp.reason = msg.rstrip()
  return resp


def head(url, **kw):
  return request("HEAD", url, **kw)

def get(url, **kw):
  return request("GET", url, **kw)

def post(url, **kw):
  return request("POST", url, **kw)

def put(url, **kw):
  return request("PUT", url, **kw)

def patch(url, **kw):
  return request("PATCH", url, **kw)

def delete(url, **kw):
  return request("DELETE", url, **kw)




