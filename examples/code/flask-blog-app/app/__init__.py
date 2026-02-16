"""Application factory for the blog application."""
from flask import Flask


def create_app(config=None):
    """
    Application factory pattern for creating Flask app instances.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Default configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['WTF_CSRF_ENABLED'] = True

    # Override with custom config if provided
    if config:
        app.config.update(config)

    # Register custom Jinja2 filters
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to <br> tags."""
        from markupsafe import Markup
        return Markup(text.replace('\n', '<br>\n'))

    # Register blueprints
    from app.routes import blog_bp
    app.register_blueprint(blog_bp)

    return app
