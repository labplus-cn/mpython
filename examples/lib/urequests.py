import usocket
  if params:
    path = path + "?"
    for k in params:
      path = path + '&'+k+'='+params[k]

  if not "Host" in headers: