# tests.py
import unittest

from peewee import SqliteDatabase
from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.

    def test_timeline_post(self):
        first_post = TimelinePost.create(name='John Doe', email='john@mail.com',
                                         content='Hello')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane', email='jane@mail.com',
                                         content='Hello World')
        assert second_post.id == 2
        timeline_posts = [model_to_dict(p)
                          for p in
                          TimelinePost.select().order_by(
                              TimelinePost.created_at.desc())]
        # print(timeline_posts)

        assert timeline_posts[1]['name'] == first_post.name
        assert timeline_posts[1]['email'] == first_post.email
        assert timeline_posts[1]['content'] == first_post.content
        assert timeline_posts[1]['id'] == first_post.id
        assert timeline_posts[0]['name'] == second_post.name
        assert timeline_posts[0]['email'] == second_post.email
        assert timeline_posts[0]['content'] == second_post.content
        assert timeline_posts[0]['id'] == second_post.id

        # self.assertCountEqual(timeline_posts[1], first_post)




