from celery import shared_task


@shared_task
def send_welcome_email(username: str, email: str):
    # Mock email sending by printing to console/log
    message = (
        "Hello {username}, welcome to NuxTest! "
        "Thanks for registering with {email}."
    ).format(username=username, email=email)
    print("[Mock email]", message) 