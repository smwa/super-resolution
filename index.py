import io

from model import super_resolution_png


sr = None
with open('demo/0851x4-crop.png', "rb") as fh:
  buf = io.BytesIO(fh.read())
  sr = super_resolution_png(buf).getvalue()
  open('test.png', 'wb').write(sr)
