# Imports
import os
import jwt
import logging

from flask import request, current_app
from .functions import create_signup_mail, create_password_reset_mail

# Setting app
app = current_app

# JWT Decoding Key
decoding_key = str(os.environ.get("JWT_KEY"))

####################
#  ROUTES LOGGING  #
####################

# ------- Configuring Logging File -------- #

# Logger For Log File
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Log File Logging Format
formatter = logging.Formatter("%(asctime)s:%(levelname)s::%(message)s")

# Log File Handler
Log_File_Handler = logging.FileHandler("mail_automation.log")
Log_File_Handler.setLevel(logging.DEBUG)
Log_File_Handler.setFormatter(formatter)

# Stream Handlers
Stream_Handler = logging.StreamHandler()

# Adding The Handlers
logger.addHandler(Log_File_Handler)
logger.addHandler(Stream_Handler)

# Log On START 
logger.debug("")
logger.debug("="*100)
logger.info("Routes Automation Section :: Logging Active")
logger.debug("")

# Email Verification and Account Activation
@app.route("/mail_verification",methods=["POST"])
async def mail_verification():
    if request.method == "POST":
        try:
            payload = jwt.decode(request.form["encoded_data"], decoding_key, "HS256")

            active_color = payload["active_color"]
            background_dark = payload["background_dark"]
            background_light = payload["background_light"]
            account_mail = payload["email"]
            user_type = payload["user_type"]
            brand_logo = payload["brand_logo"]
            brand_name = payload["brand_name"]
            brand_message = payload["brand_message"]
            verification_link = payload["verification_link"]
            sender_name = payload["sender_name"]
            closing_remark = payload["closing_remark"]
            brand_sender_email = payload["brand_sender_email"]
            brand_response_email = payload["brand_response_email"]
            user = payload["user"] if "user" in payload.keys() else None
            closure = payload["closure"] if payload["closure"] else "Best Regards"
            

            response = create_signup_mail(
                active_color=active_color, background_dark=background_dark,
                background_light=background_light, account_mail = account_mail,
                brand_logo=brand_logo, brand_name=brand_name, brand_message=brand_message,
                user_type=user_type, verification_link=verification_link, sender_name=sender_name,
                closing_remark=closing_remark, brand_sender_email=brand_sender_email,
                brand_response_email=brand_response_email, user=user, closure=closure)
            
            return response

        except Exception as e:
            logger.exception(e)
            return "Not Sent"


# message object mapped to a particular URL ‘/’
@app.route("/reset_password",methods=["POST"])
async def password_reset():
    if request.method == "POST":

        try:
            payload = jwt.decode(request.form["encoded_data"], decoding_key, "HS512")

            account_mail = payload["email"]
            active_color = payload["active_color"]
            background_light = payload["background_light"]
            background_dark = payload["background_dark"]
            brand_logo = payload["brand_logo"]
            brand_name = payload["brand_name"]
            reset_link = payload["reset_link"]
            brand_response_email = payload["brand_response_email"]
            brand_sender_email = payload["brand_sender_email"]

            response = create_password_reset_mail(
                account_mail = account_mail, active_color=active_color,
                background_light=background_light, background_dark=background_dark,
                brand_logo=brand_logo, brand_name=brand_name, reset_link=reset_link, 
                brand_sender_email=brand_sender_email,brand_response_email=brand_response_email)
            
            return response
        
        except Exception as e:
            logger.exception(e)
            return "Not Sent"

    else:
        print("Not post request")