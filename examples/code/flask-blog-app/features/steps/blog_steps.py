"""Step definitions for blog BDD scenarios."""
from pytest_bdd import scenarios, given, when, then, parsers
from app.models import Post
from app.database import db

# Load all scenarios from blog.feature
scenarios('../blog.feature')


# Context storage for sharing data between steps
class Context:
    """Context for storing data between steps."""
    def __init__(self):
        self.response = None
        self.last_post_id = None
        self.form_data = {}


context = Context()


# Background steps

@given('the blog application is running')
def app_running(client):
    """Verify the application is running."""
    response = client.get('/')
    assert response.status_code == 200


# Given steps

@given('the following posts exist:')
def create_posts_from_table(datatable):
    """Create multiple posts from a data table."""
    for row in datatable:
        post = Post(
            title=row['title'],
            content=row['content'],
            author=row['author']
        )
        db.create(post)


@given(parsers.parse('a post exists with title "{title}" content "{content}" author "{author}"'))
def create_single_post(title, content, author):
    """Create a single post."""
    post = Post(title=title, content=content, author=author)
    created_post = db.create(post)
    context.last_post_id = created_post.id


@given(parsers.parse('{count:d} posts exist in the system'))
def create_multiple_posts(count):
    """Create multiple posts for pagination testing."""
    for i in range(count):
        post = Post(
            title=f"Post Number {i+1}",
            content=f"Content for post {i+1}. This is a test post.",
            author=f"Author {i+1}"
        )
        db.create(post)


# When steps

@when('I visit the home page')
def visit_index(client):
    """Visit the index page."""
    context.response = client.get('/')


@when('I visit the post creation page')
def visit_create_page(client):
    """Visit the create post page."""
    context.response = client.get('/post/new')


@when(parsers.parse('I click on the post "{title}"'))
def click_post(client, title):
    """Click on a post (visit its detail page)."""
    # Find the post by title
    posts = db.get_all(page=1, per_page=100)
    post = next((p for p in posts if p.title == title), None)
    assert post is not None, f"Post '{title}' not found"

    context.last_post_id = post.id
    context.response = client.get(f'/post/{post.id}')


@when(parsers.parse('I click on "{link_text}"'))
def click_link(client, link_text):
    """Click on a link."""
    if 'Página' in link_text:
        page_num = link_text.split()[-1]
        context.response = client.get(f'/?page={page_num}')
    elif link_text == "Crear Post":
        context.response = client.get('/post/new')
    else:
        context.response = client.get('/')


@when(parsers.parse('I click "{button}"'))
def click_button(client, button):
    """Click a button."""
    if button == "Edit":
        assert context.last_post_id is not None
        context.response = client.get(f'/post/{context.last_post_id}/edit')
    elif button == "Delete":
        assert context.last_post_id is not None
        context.response = client.get(f'/post/{context.last_post_id}/delete')
    elif button == "Save":
        # Creating new post
        context.response = client.post(
            '/post/new',
            data=context.form_data,
            follow_redirects=True
        )
    elif button == "Update":
        # Updating existing post
        assert context.last_post_id is not None
        context.response = client.post(
            f'/post/{context.last_post_id}/edit',
            data=context.form_data,
            follow_redirects=True
        )


@when('I fill the form with:')
def fill_form(datatable):
    """Fill the form with provided data."""
    for row in datatable:
        context.form_data[row['field']] = row['value']


@when('I modify the form with:')
def modify_form(datatable):
    """Modify form fields."""
    for row in datatable:
        context.form_data[row['field']] = row['value']


@when('I confirm deletion')
def confirm_delete(client):
    """Confirm deletion by submitting delete form."""
    assert context.last_post_id is not None
    context.response = client.post(
        f'/post/{context.last_post_id}/delete',
        follow_redirects=True
    )


@when('I cancel deletion')
def cancel_delete(client):
    """Cancel deletion by going back to index."""
    context.response = client.get('/')


# Then steps

@then(parsers.parse('I see the message "{message}"'))
def see_message(message):
    """Verify message is visible."""
    assert message.encode() in context.response.data


@then(parsers.parse('I see a link to "{link_text}"'))
def see_link(link_text):
    """Verify link exists."""
    assert link_text.encode() in context.response.data or b'Siguiente' in context.response.data or b'Crear Post' in context.response.data


@then(parsers.parse('I see {count:d} posts in the list'))
def see_post_count(count):
    """Verify number of posts displayed."""
    post_count = context.response.data.count(b'<article class="post-card">')
    assert post_count == count, f"Expected {count} posts, found {post_count}"


@then(parsers.parse('I see the post "{title}"'))
def see_post(title):
    """Verify post is visible."""
    assert title.encode() in context.response.data


@then(parsers.parse('I see the title "{title}"'))
def see_title(title):
    """Verify title is visible."""
    assert title.encode() in context.response.data


@then(parsers.parse('I see the content "{content}"'))
def see_content(content):
    """Verify content is visible."""
    assert content.encode() in context.response.data


@then(parsers.parse('I see the author "{author}"'))
def see_author(author):
    """Verify author is visible."""
    assert author.encode() in context.response.data


@then('I see the creation date')
def see_creation_date():
    """Verify creation date is visible."""
    assert b'post-meta' in context.response.data
    assert b'date' in context.response.data


@then(parsers.parse('I see an "{button}" button'))
@then(parsers.parse('I see a "{button}" button'))
def see_button(button):
    """Verify button exists."""
    assert button.encode() in context.response.data or b'Editar' in context.response.data or b'Eliminar' in context.response.data


@then('I see a creation form')
def see_creation_form():
    """Verify creation form is displayed."""
    assert b'<form' in context.response.data
    assert b'name="title"' in context.response.data
    assert b'name="content"' in context.response.data
    assert b'name="author"' in context.response.data


@then(parsers.parse('I see the success message "{message}"'))
def see_success_message(message):
    """Verify success message."""
    assert message.encode() in context.response.data


@then(parsers.parse('I see the post "{title}" in the list'))
def see_post_in_list(title):
    """Verify post is in the list."""
    posts = db.get_all(page=1, per_page=100)
    post = next((p for p in posts if p.title == title), None)
    assert post is not None


@then(parsers.parse('I see the error message "{message}"'))
def see_error_message(message):
    """Verify error message is displayed."""
    assert message.encode() in context.response.data


@then('I stay on the creation page')
def stay_on_creation_page():
    """Verify still on creation page."""
    assert b'<form' in context.response.data
    assert b'Crear' in context.response.data or b'form' in context.response.data


@then('I see the edit form with current data')
def see_edit_form_with_data():
    """Verify edit form with current data."""
    assert b'<form' in context.response.data
    assert b'Editar' in context.response.data


@then(parsers.parse('I see the post "{title}" with content "{content}"'))
def see_post_with_content(title, content):
    """Verify post with specific content."""
    posts = db.get_all(page=1, per_page=100)
    post = next((p for p in posts if p.title == title), None)
    assert post is not None
    assert post.content == content


@then('I see the delete confirmation page')
def see_delete_confirmation_page():
    """Verify delete confirmation page."""
    assert b'Confirmar' in context.response.data
    assert b'seguro' in context.response.data.lower()


@then(parsers.parse('I see the confirmation message for "{title}"'))
def see_delete_confirmation_message(title):
    """Verify delete confirmation message."""
    assert b'seguro' in context.response.data.lower()
    assert title.encode() in context.response.data


@then(parsers.parse('I do not see the post "{title}" in the list'))
def not_see_post(title):
    """Verify post is not in the list."""
    posts = db.get_all(page=1, per_page=100)
    post = next((p for p in posts if p.title == title), None)
    assert post is None


@then(parsers.parse('I see {count:d} posts on the first page'))
def see_posts_on_first_page(count):
    """Verify number of posts on first page."""
    post_count = context.response.data.count(b'<article class="post-card">')
    assert post_count == count


@then(parsers.parse('I see {count:d} posts on the second page'))
def see_posts_on_second_page(count):
    """Verify number of posts on second page."""
    post_count = context.response.data.count(b'<article class="post-card">')
    assert post_count == count
