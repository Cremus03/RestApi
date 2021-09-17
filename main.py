
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db=SQLAlchemy(app)


class Image(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    byteimg = db.Column(db.String(80), nullable=False)
    formatimg = db.Column(db.String(5), nullable=False)
    name= db.Column(db.String(80))
    description= db.Column(db.String(100))

    def __repr__(self):
        return f" Id={self.id}; Imaginea in bytes={self.byteimg}; Format={self.formatimg}; Nume={self.name}; Descriere={self.description}"


@app.route('/')
def index():
    return 'Hello'

@app.route('/images')
def get_images():
    images = Image.query.all()

    output=[]
    for image in images:
        image_data = {'Id': image.id, 'Imaginea in bytes': image.byteimg, 'Format imagine': image.formatimg, 'Nume': image.name, 'Descriere': image.description}
        output.append(image_data)
    return {"images": output}

#Aici se vor accessa informatiile (GET) asociate imaginii cu id-ul dat
@app.route('/images/<id>')
def get_image(id):
    image = Image.query.get_or_404(id)
    return {"Id": image.id, "Imaginea in bytes": image.byteimg, "Format imagine": image.formatimg, "Nume": image.name, "Descriere": image.description}

@app.route('/images',methods=['POST'])
def add_image():
    image = Image(id=request.json['id'], byteimg=request.json['byteimg'], formatimg=request.json['formatimg'], name=request.json['name'], description=request.json['description'])
    db.session.add(image)
    db.session.commit()
    return {"Aveti o noua imagine pentru id-ul": image.id}

@app.route('/images/<id>', methods=['DELETE'])
def delete_image(id):
    image= Image.query.get(id)
    if image is None:
        return{"NU exista imagine la acest id"}
    db.session.delete(image)
    db.session.commit()
    return {"A fost stearsa imaginea cu id-ul":image.id}

@app.route('/images/<id>', methods=['PUT'])
def put_image(id):
    image = Image.query.get(id)
    byteimg=request.json['byteimg']
    formatimg=request.json['formatimg']
    name=request.json['name']
    description=request.json['description']
    image.byteimg=byteimg
    image.formatimg=formatimg
    image.name=name
    image.description=description

    db.session.commit()
    return {"A fost updatata imaginea cu id-ul":image.id}

#La adresa asta imaginea in format bytes va fi returnata (GET).
@app.route('/images/<id>/image')
def view_image(id):
    image = Image.query.get_or_404(id)
    return { 'Image byte': image.byteimg }

