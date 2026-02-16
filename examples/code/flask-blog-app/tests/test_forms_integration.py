"""Integration tests for forms with routes."""
import pytest


@pytest.mark.integration
class TestFormsIntegration:
    """Test suite for forms integrated with routes."""

    def test_create_form_displays_correctly(self, client):
        """Test that create form displays with correct fields."""
        response = client.get('/post/new')

        assert response.status_code == 200
        assert b'name="title"' in response.data
        assert b'name="content"' in response.data
        assert b'name="author"' in response.data
        # Note: CSRF token not present in testing mode (WTF_CSRF_ENABLED=False)

    def test_create_form_validation_errors_display(self, client):
        """Test that validation errors display in create form."""
        response = client.post(
            '/post/new',
            data={
                'title': '',
                'content': 'ABC',  # Too short
                'author': ''
            }
        )

        assert response.status_code == 200
        assert b'requerido' in response.data
        assert b'10 caracteres' in response.data

    def test_edit_form_pre_fills_data(self, client, sample_post):
        """Test that edit form pre-fills with existing post data."""
        response = client.get(f'/post/{sample_post.id}/edit')

        assert response.status_code == 200
        assert sample_post.title.encode() in response.data
        assert sample_post.content.encode() in response.data
        assert sample_post.author.encode() in response.data

    def test_edit_form_validation_errors_display(self, client, sample_post):
        """Test that validation errors display in edit form."""
        response = client.post(
            f'/post/{sample_post.id}/edit',
            data={
                'title': 'Valid Title',
                'content': 'Short',  # Too short
                'author': 'Valid Author'
            }
        )

        assert response.status_code == 200
        assert b'10 caracteres' in response.data

    def test_form_csrf_protection_enabled_in_production(self, app):
        """Test that CSRF protection is enabled by default."""
        # Create app with default config (CSRF enabled)
        from app import create_app
        prod_app = create_app()

        assert prod_app.config.get('WTF_CSRF_ENABLED', True) is True

    def test_form_submission_with_special_characters(self, client):
        """Test form submission with special characters."""
        response = client.post(
            '/post/new',
            data={
                'title': 'Test with "quotes" & <html>',
                'content': 'Content with special chars: áéíóú ñ',
                'author': 'Author with ñ'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'Post creado exitosamente' in response.data

    def test_form_submission_preserves_whitespace(self, client):
        """Test that form submission preserves whitespace in content."""
        content = "Line 1\n\nLine 2\n  Indented line"

        response = client.post(
            '/post/new',
            data={
                'title': 'Whitespace Test',
                'content': content,
                'author': 'Test Author'
            },
            follow_redirects=True
        )

        assert response.status_code == 200

        from app.database import db
        posts = db.get_all()
        assert len(posts) == 1
        assert posts[0].content == content

    def test_flash_messages_display_correctly(self, client, sample_post):
        """Test that flash messages display correctly after form submission."""
        # Test success message
        response = client.post(
            '/post/new',
            data={
                'title': 'New Post',
                'content': 'New content here',
                'author': 'New Author'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'alert-success' in response.data
        assert b'Post creado exitosamente' in response.data

    def test_cancel_button_redirects_correctly(self, client):
        """Test that cancel button/link exists in forms."""
        response = client.get('/post/new')

        assert response.status_code == 200
        assert b'Cancelar' in response.data
        assert b'href' in response.data
