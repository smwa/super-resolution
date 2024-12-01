import io
from os import environ

from model import super_resolution_png

from PIL import Image
from flask import Flask, flash, request, redirect, send_file
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
BLACK = (0,0,0)
RESOLUTION_LIMIT = 2500
if "RESOLUTION_LIMIT" in environ:
  RESOLUTION_LIMIT = int(environ["RESOLUTION_LIMIT"])
print("Resolution limit: {}".format(RESOLUTION_LIMIT))

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    extension = file.filename.rsplit('.', 1)[1].lower()
    if file and '.' in file.filename and extension in ALLOWED_EXTENSIONS:
      filename = secure_filename(file.filename)
      sr_bytes_png = None
      buf = io.BytesIO(file.read())

      # Convert to png if necessary
      if extension != 'png':
        print("Converting to png")
        jpgimg = Image.open(buf)
        print("opened")
        jpgimg = jpgimg.convert('RGB')
        print("converted")
        pngbuf = io.BytesIO()
        print("new object created")
        jpgimg.save(pngbuf, format='PNG')
        print("saved")
        buf = pngbuf

      # Make image a square
      print("Squaring")
      img = Image.open(buf)
      width, height = img.size
      ratio = width / height
      max_dimension = max(width, height)
      if max_dimension > RESOLUTION_LIMIT:
        return "", 413 # too large
      tmpimg = Image.new(img.mode, (max_dimension, max_dimension), BLACK)
      tmpimg.paste(img, (0, 0))
      img = tmpimg
      img.save(buf, format="PNG")
      print("Squared")

      print("Super rezing")
      sr_bytes_png = super_resolution_png(buf).getvalue()
      print("Super resolution done")
      buf = io.BytesIO(sr_bytes_png)

      # Crop out from the expanded image
      img = Image.open(buf)
      width, height = img.size
      if ratio >= 1.0:
        img = img.crop((0, 0, width, int(height / ratio)))
      else:
        img = img.crop((0, 0, (width * ratio), height))
      img.save(buf)

      return send_file(
        buf,
        mimetype='image/png',
        as_attachment=False,
        download_name=filename)
  return '''
  <!doctype html>
  <title>Super Resolution of PNG File</title>
  <h1>Super Resolution of PNG File</h1>
  <form method=post enctype=multipart/form-data>
    <input type=file name=file accept=".png,.jpg,.jpeg">
    <button type="submit">Upload</button>
  </form>
  '''
