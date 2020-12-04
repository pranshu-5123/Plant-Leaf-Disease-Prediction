from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static\\images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
img_path = 'static/images'

app.static_folder = 'static'

user_choice = ''

fname = ''

@app.route('/', methods = ['GET', 'POST'])
def home():
   global user_choice
   if request.method == 'POST':
      if request.form['veggie'] == 'Potato':
         user_choice = 'p'
         return redirect(url_for('upload_file'))
      else:
         user_choice = 't'
         return redirect(url_for('upload_file'))
   else:
      return render_template('index.html')

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uplad_file():
   if request.method == 'POST':
      f = request.files['file']
      global fname
      global img_path
      sfname = secure_filename(f.filename)
      fname = os.path.join(app.config['UPLOAD_FOLDER'], sfname)
      img_path = os.path.join(img_path, sfname)
      f.save(fname)
      return render_template('predict.html')

@app.route('/delete', methods = ['GET', 'POST'])
def delete_file():
   global fname
   global img_path
   os.remove(fname)
   fname = ''
   img_path = 'static/images'
   return redirect(url_for('home'))


@app.route('/predictor', methods = ['GET', 'POST'])
def predict():

   pmodel = None
   global user_choice

   if user_choice == 'p':
      pmodel = load_model('PotatoLeaf.h5')
   else:
      pmodel = load_model('TomatoLeaf.h5')
   
   img = load_img(fname, target_size = (256, 256))
   x = img_to_array(img)
   x = x/255
   x = np.expand_dims(x, axis=0)
   x = np.expand_dims(x, axis=0)
   imge = np.vstack(x)
   pred = np.argmax(pmodel.predict(imge), axis=-1)[0]

   disease = None

   if user_choice == 'p':   
      if pred == 0:
         disease = 'Early Blight'
      elif pred == 1:
         disease = 'Healthy'
      else:
         disease = 'Late Blight'
   else:
      if pred == 0:
         disease = 'Bacterial Spot'
      elif pred == 1:
         disease = 'Early Blight'
      elif pred == 2:
         disease = 'Healthy'
      elif pred == 3:
         disease = 'Late Blight'
      elif pred == 4:
         disease = 'Leaf Mold'
      elif pred == 5:
         disease = 'Mosaic Virus'     
      elif pred == 6:
         disease = 'Septoria Leaf Spot'
      elif pred == 7:
         disease = 'Target Spot'
      elif pred == 8:
         disease = 'Two Spotted Spider Mite'
      else:
         disease = 'Yellow Leaf Curl Virus'

   return render_template('prediction.html', disease = disease, img = img_path)
      
		
if __name__ == '__main__':
   app.run(debug = True)