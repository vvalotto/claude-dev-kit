"""Unit tests for forms."""
import pytest
from app.forms import PostForm


@pytest.mark.unit
class TestPostForm:
    """Test suite for PostForm."""

    def test_form_initialization(self, app):
        """Test form can be initialized."""
        with app.app_context():
            form = PostForm()
            assert form is not None
            assert hasattr(form, 'title')
            assert hasattr(form, 'content')
            assert hasattr(form, 'author')
            assert hasattr(form, 'submit')

    def test_form_valid_data(self, app):
        """Test form validation with valid data."""
        with app.app_context():
            form = PostForm(
                data={
                    'title': 'Valid Title',
                    'content': 'This is valid content with more than 10 characters',
                    'author': 'Valid Author'
                }
            )
            assert form.validate()

    def test_form_missing_title(self, app):
        """Test form validation fails when title is missing."""
        with app.app_context():
            form = PostForm(
                data={
                    'title': '',
                    'content': 'Valid content here',
                    'author': 'Valid Author'
                }
            )
            assert not form.validate()
            assert 'title' in form.errors
            assert 'requerido' in form.errors['title'][0].lower()

    def test_form_missing_content(self, app):
        """Test form validation fails when content is missing."""
        with app.app_context():
            form = PostForm(
                data={
                    'title': 'Valid Title',
                    'content': '',
                    'author': 'Valid Author'
                }
            )
            assert not form.validate()
            assert 'content' in form.errors

    def test_form_content_too_short(self, app):
        """Test form validation fails when content is too short."""
        with app.app_context():
            form = PostForm(
                data={
                    'title': 'Valid Title',
                    'content': 'Short',  # Less than 10 characters
                    'author': 'Valid Author'
                }
            )
            assert not form.validate()
            assert 'content' in form.errors
            assert '10' in form.errors['content'][0]

    def test_form_missing_author(self, app):
        """Test form validation fails when author is missing."""
        with app.app_context():
            form = PostForm(
                data={
                    'title': 'Valid Title',
                    'content': 'Valid content here',
                    'author': ''
                }
            )
            assert not form.validate()
            assert 'author' in form.errors
            assert 'requerido' in form.errors['author'][0].lower()

    def test_form_all_fields_missing(self, app):
        """Test form validation fails when all fields are missing."""
        with app.app_context():
            form = PostForm(
                data={
                    'title': '',
                    'content': '',
                    'author': ''
                }
            )
            assert not form.validate()
            assert 'title' in form.errors
            assert 'content' in form.errors
            assert 'author' in form.errors

    def test_form_content_exactly_10_characters(self, app):
        """Test form validation passes with exactly 10 characters in content."""
        with app.app_context():
            form = PostForm(
                data={
                    'title': 'Valid Title',
                    'content': '1234567890',  # Exactly 10 characters
                    'author': 'Valid Author'
                }
            )
            assert form.validate()
