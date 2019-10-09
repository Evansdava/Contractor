from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId


sample_listing_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_listing = {
    'title': 'Clown Nose',
    'price': '1000',
    'image': 'https://inst-1.cdn.shockers.de/hs_cdn/out/pictures/master/\
product/1/clownsnase-vinyl--rote-kunststoff-clown-nase--faschingsnase\
--karnevals-zubehoer--horrorclown-nase--13915.jpg'
}
sample_form_data = {
    'title': sample_listing['title'],
    'price': sample_listing['price'],
    'image': sample_listing['image']
}


class listingsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the listings homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'listing', result.data)

    def test_new(self):
        """Test the new listing creation page."""
        result = self.client.get('/listings/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New listing', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_listing(self, mock_find):
        """Test showing a single listing."""
        mock_find.return_value = sample_listing

        result = self.client.get(f'/listings/{sample_listing_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Clown Nose', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_listing(self, mock_find):
        """Test editing a single listing."""
        mock_find.return_value = sample_listing

        result = self.client.get(f'/listings/{sample_listing_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Clown Nose', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_listing(self, mock_insert):
        """Test submitting a new listing."""
        result = self.client.post('/listings', data=sample_form_data)

        # After submitting, should redirect to that listing's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_listing)


if __name__ == '__main__':
    unittest_main()
