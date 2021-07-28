from flask import Flask, redirect, render_template, request, url_for
from decouple import config

from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()


@app.route('/')
def display_pets():
    pets = Pet.query.all()
    return render_template('display_pets.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pets():
    form = AddPetForm()

    if form.validate_on_submit():
        pet = Pet(name=form.name.data, species=form.species.data, photo_url=form.photo_url.data,
                    age=form.age.data, notes=form.notes.data)
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('display_pets'))
    return render_template('add_pets.html', form=form)


@app.route('/<id>', methods=['GET', 'POST'])
def edit_pets(id):
    pet = Pet.query.get(id)
    form = EditPetForm()
    if pet:
        if form.validate_on_submit():
            if form.photo_url.data:
                pet.photo_url = form.photo_url.data
            if form.notes.data:
                pet.notes = form.notes.data
            if form.available != None:
                if form.available.data == 'true':
                    pet.available = True
                else:
                    pet.available = False
            db.session.add(pet)
            db.session.commit()
            return redirect(url_for('display_pets'))
        return render_template('edit_pet.html', form=form, pet=pet)
    return redirect(url_for('not_found'))


@app.route('/404')
def not_found():
    """A catch all page that is used when the user types
       in a bad route. It automatically redirects after 
       three seconds."""
    return render_template('404.html')
    