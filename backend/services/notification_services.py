import smtplib
from email.message import EmailMessage


def send_email_alert(message: str):

    sender_email = "singhanshumanv@gmail.com"
    receiver_email = "aks12399662@gmail.com"
    app_password = "zumkkunduytmvtxn"

    email = EmailMessage()
    email["Subject"] = "Compliance Alert"
    email["From"] = sender_email
    email["To"] = receiver_email

    email.set_content(message)

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, app_password)
            smtp.send_message(email)

        print("Email alert sent")

    except Exception as e:
        print("Email sending failed:", e)