import os
import io
import tempfile

from model import super_resolution_png

from PIL import Image
from flask import Flask, flash, request, redirect, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



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
      sr_bytes_png = super_resolution_png(buf).getvalue()
      print("Super resolution done")
      return send_file(
        io.BytesIO(sr_bytes_png),
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
