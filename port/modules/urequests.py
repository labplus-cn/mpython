import usocket
import time
import os
from urllib.parse import quote


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


def request(method, url, data=None, json=None, headers={}, stream=None, params=None, files=None):
  _headers = {}
  _headers.update(headers)
  # url parse
  try:
    proto, dummy, host, path = url.split("/", 3)
  except ValueError:
    try:
      proto, dummy, host = url.split("/", 2)
    except ValueError:
      raise ValueError("Invalid URL")
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

  path = quote(path, safe='?,=,/,&')
  # if have params,urlencoded to URL
  if params:
    from urllib.parse import urlencode
    path = path + "?"
    path = path + urlencode(params)

  ai = usocket.getaddrinfo(host, port)
  addr = ai[0][4]
  s = usocket.socket()
  s.settimeout(5)
  s.connect(addr)
  if proto == "https:":
    s = ussl.wrap_socket(s,do_handshake=False)
  _headers['Host'] = host

  if data is not None:
    if isinstance(data, tuple):
      data = dict(data)
    if isinstance(data, dict):
      if not 'ujson' in globals():
        import ujson
      data = urlencode(data)
      _headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'

  if json is not None:
    assert data is None
    if not 'ujson' in globals():
      import ujson
    _headers['Content-Type'] = 'application/json'
    data = ujson.dumps(json)

  if files:
    boundary = '----WebKitFormBoundary'+hex(int(time.time()))
    _headers['Content-Type'] = "multipart/form-data; boundary=%s" % boundary
    _headers['Connection'] = "keep-alives"
    name = list(files.keys())[0]
    file_dir = files.get(name)[0]
    file_type = files.get(name)[1]
    file_size = os.stat(file_dir)[6]
    file_name = file_dir.split('/')[-1]
    file = open(file_dir, 'rb')
    content_disposition = b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (
        name, file_name)
    content_type = b"Content-Type: %s\r\n" % file_type
    content_length = len(boundary)+4+len(content_disposition) + \
        len(content_type)+2+file_size+len(boundary)+8
    _headers['Content-Length'] = str(content_length)
  if data:
    _headers['Content-Length'] = str(len(data))

  # Send Request Header
  s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
  for k, v in _headers.items():
      s.write('%s: %s\r\n' % (k, v))
      # print('%s: %s\r\n' % (k, v), end='')
  # Partition
  s.write(b"\r\n")

# Body
  if data:
    s.write(data)

  if files:
    # first boundary
    s.write(b"--%s\r\n" % boundary)
    s.write(content_disposition)
    s.write(content_type)
    s.write(b"\r\n")
    # file data for hex
    while True:
      _read = memoryview(file.read(1024*3))
      if _read != b'':
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
