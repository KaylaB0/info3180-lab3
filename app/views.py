from app import app, mail
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from app.forms import ContactForm
from flask_mail import Message
from flask import session


###
# Routing for your application.
###

app.config['SECRET_KEY'] = 'Som3$ec5etK*y'

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route ("/contact", methods=["GET","POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():  # Check if form is valid
        msg = Message(
            subject=form.subject.data,
            sender=form.email.data,  # Use user's name and email
            recipients=["to@example.com"],  # Replace with Mailtrap test email
        )
        msg.body = form.message.data  # Set the email body with user's message

        mail.send(msg)  # Send the email
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("home"))  # Redirect to home page after success
    flash_errors(form)  # Flash form errors if validation fails
    return render_template("contact.html", form=form)  # Show form again if not valid

###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
