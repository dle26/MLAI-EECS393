from config import Config
from flask import jsonify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pymongo

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

#json contents need to be in dictionary format
# ex send_json_to_database(isaacwithrow, {"a": 2}) will add
# {"file": {"a": 2}} to the user isaacwithrow's entry in the database
def send_json_to_database(username, json_contents):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["MLAI"]
    users = mydb["users"]

    myquery = { "username": username }

    newvalues = { "$set": { "file": json_contents } }
    users.update_one(myquery, newvalues)
