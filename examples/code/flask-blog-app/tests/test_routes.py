"""Integration tests for blog routes."""
import pytest
from app.database import db
from app.models import Post


@pytest.mark.integration
class TestBlogRoutes:
    """Test suite for blog routes."""

    def test_index_empty(self, client):
        """Test index page with no posts."""
        response = client.get('/')

        assert response.status_code == 200
        assert b'No hay posts disponibles' in response.data
        assert b'Crear Post' in response.data

    def test_index_with_posts(self, client, sample_post):
        """Test index page with posts."""
        response = client.get('/')

        assert response.status_code == 200
        assert b'Sample Post' in response.data
        assert b'Test Author' in response.data
        assert sample_post.content[:50].encode() in response.data

    def test_index_pagination(self, client, multiple_posts):
        """Test index pagination."""
        # First page
        response = client.get('/')
        assert response.status_code == 200
        assert b'Post 1' in response.data  # Newest posts first
        assert b'P' in response.data

        # Second page
        response = client.get('/?page=2')
        assert response.status_code == 200

    def test_post_detail_valid(self, client, sample_post):
        """Test viewing post detail."""
        response = client.get(f'/post/{sample_post.id}')

        assert response.status_code == 200
        assert b'Sample Post' in response.data
        assert b'This is sample content' in response.data
        assert b'Test Author' in response.data
        assert b'Editar' in response.data
        assert b'Eliminar' in response.data

    def test_post_detail_not_found(self, client):
        """Test viewing non-existent post."""
        response = client.get('/post/999', follow_redirects=True)

        assert response.status_code == 200
        assert b'Post no encontrado' in response.data

    def test_post_create_get(self, client):
        """Test GET request to create post form."""
        response = client.get('/post/new')

        assert response.status_code == 200
        assert b'Crear Nuevo Post' in response.data
        assert b'form' in response.data
        assert b'title' in response.data.lower()
        assert b'content' in response.data.lower()
        assert b'author' in response.data.lower()

    def test_post_create_post_valid(self, client):
        """Test POST request to create post with valid data."""
        response = client.post(
            '/post/new',
            data={
                'title': 'New Test Post',
                'content': 'This is the content of the new test post.',
                'author': 'New Author'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'Post creado exitosamente' in response.data
        assert b'New Test Post' in response.data

        # Verify post was created in database
        posts = db.get_all()
        assert len(posts) == 1
        assert posts[0].title == 'New Test Post'

    def test_post_create_post_invalid(self, client):
        """Test POST request to create post with invalid data."""
        response = client.post(
            '/post/new',
            data={
                'title': '',  # Missing title
                'content': 'Valid content',
                'author': 'Valid Author'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'requerido' in response.data

        # Verify post was not created
        assert db.count() == 0

    def test_post_edit_get(self, client, sample_post):
        """Test GET request to edit post form."""
        response = client.get(f'/post/{sample_post.id}/edit')

        assert response.status_code == 200
        assert b'Editar Post' in response.data
        assert b'Sample Post' in response.data

    def test_post_edit_post_valid(self, client, sample_post):
        """Test POST request to edit post with valid data."""
        response = client.post(
            f'/post/{sample_post.id}/edit',
            data={
                'title': 'Updated Title',
                'content': 'Updated content for this post.',
                'author': 'Updated Author'
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'Post actualizado exitosamente' in response.data
        assert b'Updated Title' in response.data

        # Verify post was updated
        updated_post = db.get_by_id(sample_post.id)
        assert updated_post.title == 'Updated Title'
        assert updated_post.content == 'Updated content for this post.'

    def test_post_edit_not_found(self, client):
        """Test editing non-existent post."""
        response = client.get('/post/999/edit', follow_redirects=True)

        assert response.status_code == 200
        assert b'Post no encontrado' in response.data

    def test_post_delete_get(self, client, sample_post):
        """Test GET request to delete confirmation page."""
        response = client.get(f'/post/{sample_post.id}/delete')

        assert response.status_code == 200
        assert b'Confirmar' in response.data
        assert b'Sample Post' in response.data
        assert b'seguro' in response.data.lower()

    def test_post_delete_post_valid(self, client, sample_post):
        """Test POST request to delete post."""
        post_id = sample_post.id
        response = client.post(
            f'/post/{post_id}/delete',
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'Post eliminado exitosamente' in response.data

        # Verify post was deleted
        assert db.get_by_id(post_id) is None
        assert db.count() == 0

    def test_post_delete_not_found(self, client):
        """Test deleting non-existent post."""
        response = client.get('/post/999/delete', follow_redirects=True)

        assert response.status_code == 200
        assert b'Post no encontrado' in response.data
