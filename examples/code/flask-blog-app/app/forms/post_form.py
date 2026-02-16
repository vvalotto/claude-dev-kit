"""Post form for creating and editing blog posts."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """
    Form for creating and editing blog posts.

    Fields:
        title: Post title (required)
        content: Post content (required, minimum 10 characters)
        author: Post author name (required)
        submit: Submit button
    """

    title = StringField(
        'Título',
        validators=[
            DataRequired(message='El título es requerido')
        ],
        render_kw={'placeholder': 'Ingrese el título del post'}
    )

    content = TextAreaField(
        'Contenido',
        validators=[
            DataRequired(message='El contenido es requerido'),
            Length(min=10, message='El contenido debe tener al menos 10 caracteres')
        ],
        render_kw={'placeholder': 'Ingrese el contenido del post', 'rows': 10}
    )

    author = StringField(
        'Autor',
        validators=[
            DataRequired(message='El autor es requerido')
        ],
        render_kw={'placeholder': 'Ingrese el nombre del autor'}
    )

    submit = SubmitField('Guardar')
