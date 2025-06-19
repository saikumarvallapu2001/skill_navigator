# Skill Navigator

A Flask-based web application for skill tracking and navigation.

## Features

- User authentication and authorization
- Skill tracking and management
- File upload capabilities
- MySQL database integration
- Modern web interface

## Prerequisites

- Python 3.13 or higher
- MySQL Server
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd skill_navigator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:
```env
SECRET_KEY=your_secret_key
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=skill_navigator
```

5. Create the MySQL database:
```sql
CREATE DATABASE skill_navigator;
```

## Running the Application

1. Make sure your MySQL server is running

2. Start the Flask application:
```bash
python app.py
```

3. The application will be available at `http://localhost:5000`

## Project Structure

```
skill_navigator/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── models.py           # Database models
├── routes.py           # Application routes
├── extensions.py       # Flask extensions
├── manage.py           # Management commands
├── migrations.py       # Database migrations
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
└── instance/          # Instance-specific files
```

## Dependencies

- Flask==2.0.1
- Flask-SQLAlchemy==2.5.1
- SQLAlchemy==1.4.49
- Flask-Login==0.5.0
- Werkzeug==2.0.1
- mysql-connector-python==8.0.26
- PyMySQL==1.0.2
- python-dotenv==0.19.0
- email-validator==1.1.3
- Pillow>=10.0.0
- Flask-WTF==0.15.1
- WTForms==2.3.3
- Flask-Migrate==3.1.0
- Flask-Mail==0.9.1

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 