
# `FCM Notification`

![20241006_134055-COLLAGE](https://github.com/user-attachments/assets/b0f8d8b0-160e-467c-ab6a-aa748562f8dd)
![image](https://github.com/user-attachments/assets/ec1dc18c-55a0-4bbd-856b-881b235c0ba7)

# `Amazon SES`

## Step 1: Set Up the Django Project

1. **Install Python and Django**: If you haven’t installed Python and Django already, do so now.

   - Install Python: [Download and install Python](https://www.python.org/downloads/).
   - Install Django: Open your terminal and run:

     ```bash
     pip install django
     ```

2. **Create a New Django Project**: Open your terminal and run the following command to create a new project named `myproject` (you can change the project name as needed):

   ```bash
   django-admin startproject myproject
   ```

   This will create a directory structure like this:

   ```
   myproject/
       ├── manage.py
       └── myproject/
           ├── __init__.py
           ├── settings.py
           ├── urls.py
           └── wsgi.py
   ```

3. **Navigate to the Project Directory**:

   ```bash
   cd myproject
   ```

4. **Create a New Django App**: Create an app named `emailapp` (you can choose any name):

   ```bash
   python manage.py startapp emailapp
   ```

   The directory structure will now look like this:

   ```
   myproject/
       ├── manage.py
       ├── emailapp/
       │   ├── __init__.py
       │   ├── admin.py
       │   ├── apps.py
       │   ├── models.py
       │   ├── tests.py
       │   └── views.py
       └── myproject/
           ├── __init__.py
           ├── settings.py
           ├── urls.py
           └── wsgi.py
   ```

## Step 2: Configure the Django Project for Email

1. **Add the App to `settings.py`**: Open `myproject/settings.py` and add `emailapp` to the `INSTALLED_APPS` list:

   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'emailapp',  # Add this line
   ]
   ```

2. **Set Up Email Configuration**: Add the following email configuration to the `settings.py` file:

   ```python
   # myproject/settings.py

   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'AKIAUUGAOKJTZCJPILPC'  # Replace with your SMTP username
   EMAIL_HOST_PASSWORD = 'BC8JvtCJK4ul/14LLeQK5kjQYkVgWoEQfix'  # Replace with your SMTP password
   DEFAULT_FROM_EMAIL = 'your_verified_email@example.com'  # Replace with your verified SES email
   ```

   > Note: Replace the `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `DEFAULT_FROM_EMAIL` values with your Amazon SES credentials and verified email.

3. **Verify the SES Email Address**: Make sure that the `DEFAULT_FROM_EMAIL` you’re using is a verified email in your Amazon SES console. You can verify email addresses in the [Amazon SES console](https://console.aws.amazon.com/ses/).

4. **Update `urls.py`**: In the `myproject/urls.py` file, include the app’s URLs:

   ```python
   # myproject/urls.py

   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('emailapp.urls')),  # Include emailapp URLs
   ]
   ```

5. **Create a `urls.py` File for the App**: Inside the `emailapp` directory, create a new file named `urls.py` and add the following code:

   ```python
   # emailapp/urls.py

   from django.urls import path
   from . import views

   urlpatterns = [
       path('', views.send_email, name='send_email'),
   ]
   ```

6. **Create a View to Send Email**: In the `emailapp/views.py` file, create a view to send an email using Django’s `send_mail` function:

   ```python
   # emailapp/views.py

   from django.core.mail import send_mail
   from django.http import HttpResponse

   def send_email(request):
       # Replace 'recipient@example.com' with the recipient email address
       send_mail(
           subject='Test Email from Django',
           message='This is a test email sent using Amazon SES with Django.',
           from_email='your_verified_email@example.com',  # Must be a verified SES email
           recipient_list=['recipient@example.com'],
           fail_silently=False,
       )
       return HttpResponse('Email sent successfully!')
   ```

   > Replace `your_verified_email@example.com` with your verified SES email address and `recipient@example.com` with the recipient’s email address.

## Step 3: Run the Django Project

1. **Migrate the Database**: Run the following command to create the necessary database tables:

   ```bash
   python manage.py migrate
   ```

2. **Create a Superuser**: Create a superuser account to access the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the on-screen prompts to enter a username, email, and password.

3. **Run the Django Development Server**: Start the development server:

   ```bash
   python manage.py runserver
   ```

4. **Access the Application**: Open a web browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/). If everything is set up correctly, you should see the message "Email sent successfully!" and an email should be sent to the recipient’s address.

## Step 4: Troubleshooting

- **Verify SES Credentials**: Make sure that the `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are correct. You can generate these credentials in the SES console.
- **Verify the Email Address**: Verify that the email address used in `DEFAULT_FROM_EMAIL` is verified in your Amazon SES.
- **Check the SES Sandbox Mode**: If your SES account is in sandbox mode, you can only send emails to verified email addresses. To lift these restrictions, request [production access](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/request-production-access.html) for SES.

This guide should help you set up a basic Django project with Amazon SES email integration. Let me know if you have any questions or encounter any issues!
