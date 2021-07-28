from unittest import TestCase

from decouple import config

from app import app
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm


app.config['SQLALCHEMY_DATABASE_URI'] = config('TEST_DB')
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class PetShopTestCase(TestCase):
    def create_pet(self):
        pet = Pet(name='Harry', species='dog', photo_url='', age=4, notes='A very dirty dog.', available=True)
        db.session.add(pet)
        db.session.commit()
        return pet
    

    def create_unadded_pet(self):
        data = {'name': 'Steve', 'species': 'cat', 'photo_url': 'www.google.com', 'age': 4, 'notes': 'A good cat.', 'available': True}
        return data
    

    def delete_pet(self, pet):
        db.session.delete(pet)
        db.session.commit()


    def setUp(self) -> None:
        Pet.query.delete()
    

    def tearDown(self) -> None:
        db.session.rollback()
    

    def test_display_pet(self):
        with app.test_client() as client:
            pet = self.create_pet()
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Pet Shop', resp.get_data(as_text=True))
            self.assertIn('Harry', resp.get_data(as_text=True))
            self.delete_pet(pet)
    

    def test_add_pet(self):
        with app.test_client() as client:
            data = self.create_unadded_pet()
            resp = client.post('/add', data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Steve', resp.get_data(as_text=True))
            pet = Pet.query.filter_by(name='Steve').first()
            if pet:
                self.delete_pet(pet)
    

    def test_edit_pet(self):
        with app.test_client() as client:
            pet = self.create_pet()
            data = {'photo_url': 'www.google.com', 'notes': 'The best dirty dog!', 'available': True}
            resp = client.post(f'/{pet.id}', data=data, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('The best dirty dog!', resp.get_data(as_text=True))
            newpet = Pet.query.first()
            self.assertEqual(newpet.name, 'Harry')
            self.delete_pet(pet)
    

    def test_404_route(self):
        with app.test_client() as client:
            resp = client.get('/404')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sorry', resp.get_data(as_text=True))