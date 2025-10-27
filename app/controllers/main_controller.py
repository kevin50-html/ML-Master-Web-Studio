# app/controllers/main_controller.py
from flask import Blueprint, render_template

main_controller = Blueprint('main', __name__)

@main_controller.route('/')
def index():
    return render_template('index.html')

@main_controller.route('/about')
def about():
    return render_template('about.html')

@main_controller.route('/contact')
def contact():
    return render_template('contact.html')

@main_controller.route('/services')
def services():
    return render_template('service.html')

@main_controller.route('/blog')
def blog():
    return render_template('blog.html')

@main_controller.route('/team')
def team():
    return render_template('team.html')

@main_controller.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@main_controller.route('/faq')
def faq():
    return render_template('FAQ.html')


@main_controller.route('/feature')
def feature():
    return render_template('feature.html')

@main_controller.route('/404')
def error404():
    return render_template('404.html'), 404

@main_controller.route('/login2')
def login2():
    return render_template('login2.html')

#_____________________________________________________________________________
"""
# main_controller.py
from flask import Blueprint, render_template
from .dashboard_menu_config import DASHBOARD_MENU  # Importa el archivo de configuración

main_controller = Blueprint('dashboard', __name__)

@main_controller.route('/dashboard')
def index():
    return render_template('dashboard.html', dashboard_menu=DASHBOARD_MENU)

@main_controller.route('/profile')
def profile():
    return render_template('profile.html', dashboard_menu=DASHBOARD_MENU)

@main_controller.route('/settings')
def settings():
    return render_template('settings.html', dashboard_menu=DASHBOARD_MENU)

@main_controller.route('/reports')
def reports():
    return render_template('reports.html', dashboard_menu=DASHBOARD_MENU)

@main_controller.route('/test')
def test():
    return "¡Ruta de prueba exitosa!"
"""
