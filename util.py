from config import Config
from flask import jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_feedback_email(email_address, name, feedback, subject):
    message = Mail(
        from_email='MLAI@case.edu',
        to_emails='isw9@case.edu',
        subject=subject,
        html_content='{0} - {1} - {2}'.format(feedback, name, email_address))
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        return jsonify({'feedback': 'submitted successfully'})
    except Exception as e:
        print(e)
        return jsonify({'feedback': 'error'})
