# tests.py

import unittest
import os

from flask import abort, url_for

from flask_testing import TestCase

from app import create_app, db
from app.models import User, Participant, Storage


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://db_admin:dbadmin@localhost/bccipfest'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = User(username="admin", password="adminbcc2020", is_admin=True)

        # create test non-admin user
        user = User(username="test_user", password="test2020")

        # save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_user_model(self):
        """
        Test number of records in User table
        """
        self.assertEqual(User.query.count(), 2)

    def test_participant_model(self):
        """
        Test number of records in Participant table
        """

        # create test department
        participant = Participant(partname="Tester", fcd=1, usd=1, sar=1, rub=1, yen=1)

        # save department to database
        db.session.add(participant)
        db.session.commit()

        self.assertEqual(Participant.query.count(), 1)

    def test_storage_model(self):
        """
        Test number of storages in Role table
        """

        # create test role
        storage = Storage(storown="Tester", stornum=1, current_capacity=50)

        # save role to database
        db.session.add(storage)
        db.session.commit()

        self.assertEqual(Storage.query.count(), 1)

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_participants_view(self):
        """
        Test that participants page is inaccessible without login
        and redirects to login page then to participants page
        """
        target_url = url_for('admin.list_participants')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_storages_view(self):
        """
        Test that storages page is inaccessible without login
        and redirects to login page then to storages page
        """
        target_url = url_for('admin.list_storages')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_users_view(self):
        """
        Test that users page is inaccessible without login
        and redirects to login page then to users page
        """
        target_url = url_for('admin.list_users')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

if __name__ == '__main__':
    unittest.main()