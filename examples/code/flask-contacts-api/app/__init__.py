"""Flask application factory."""

from flask import Flask
from app.routes import contacts_bp


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance

    Examples:
        >>> app = create_app()
        >>> app.config['TESTING']
        False
    """
    app = Flask(__name__)

    # Configuration
    app.config['JSON_AS_ASCII'] = False  # Allow UTF-8 in JSON responses
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    # Register blueprints
    app.register_blueprint(contacts_bp)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy'}, 200

    return app
