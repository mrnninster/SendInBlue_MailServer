# importing libraries
import os
import logging
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


##################
#  MAIL LOGGING  #
##################

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
logger.info("Mail Automation Section :: Logging Active")
logger.debug("")

# Create SendInBlue Configuration
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.environ.get("SENDINBLUE_API_KEY")


def sib_send_mail(subject,html_content,sender,destination,response_destination) -> str:
    """
        Thid fuctions sends generated email using the 
        send-in-blue mailing service

        Params
        ------
        subject: The emails subject
        html_content: The html of the email being sent
        sender: The sender of the email
        destination: The destination the email is being sent to
        response_destination, The email that receives a reply from the 
            receipient of the sent mail.


        Returns
        -------
        returns a response "Sent" or Not Sent
    """

    try:
        # Create a new mail api Instance
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Send Mail
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=destination, reply_to=response_destination, html_content=html_content, sender=sender, 
            subject=subject
            )
        
        # Request response
        response = api_instance.send_transac_email(send_smtp_email)
        logger.debug(response)
        return 'Sent'

    except ApiException as e:
        logger.exception(f"SendSIBMailError: Failed to send mail with send-in-blue")
        return "Not Sent"


def create_signup_mail(account_mail:str,active_color:str, 
        background_dark:str, background_light:str, brand_logo:str,
        brand_name:str,user_type:str, brand_message:str, verification_link:str,
        closing_remark:str, sender_name:str, brand_sender_email:str,
        brand_response_email:str, user:str| None = None, closure:str="Best Regards",
        ) -> str:
    """
        This function generates the email verification
        and account activation mail

        Params
        -------
        active_color: The brands main color
        background_dark: The dark shade of the brand colour used for backgrounds
        background_light: The light shade of the brand colour used for backgrounds
        account_token: The token used to identify the account
        account_mail: The email associated with the account
        brand_logo: Url for the logo of the brand
        brand_name: The name of the brand
        user_type: The type of account to be verified, samples are
            - Product Owner
            - Product User
        brand_message: Message to be added in the onboarding email
        verification_liink: The link used to verify accounts
        closing_remarks: The clsoing remark for the email
        closure: An email closure, sample
            - Best regards
        sender_name: The name used to sign off the email
        brand_response_email: The email account that receives a response from the sent email
        brand_sender_email: The email account that is sending the email


        Returns
        -------
        response: returns a response "Sent" or Not Sent
    """
    # Pick Response file
    path = f"{os.curdir}/mail_app/templates/sign_up.html"
       
    try:
        # Generate Mail Data

        with open(path, "r+") as ht:
            verification_page = ht.read()
            verification_page = verification_page.replace("**active-color**",active_color)
            verification_page = verification_page.replace("**background-dark**",background_dark)
            verification_page = verification_page.replace("**background-light**",background_light)
            verification_page = verification_page.replace("**BRAND NAME**", brand_name)
            verification_page = verification_page.replace("**USER / USER TYPE**", user) if user != None else verification_page.replace("**USER / USER TYPE**", user_type)
            verification_page = verification_page.replace("**BRAND MESSAGE**", brand_message)
            verification_page = verification_page.replace("**VERIFICATION LINK**", verification_link)
            verification_page = verification_page.replace("**CLOSING REMARKS**", closing_remark)
            verification_page = verification_page.replace("**CLOSURE**", closure)
            verification_page = verification_page.replace("**SENDER NAME**", sender_name)

        subject = "Email Verification and Account Activation"
        sender = {"name": brand_name,"email":brand_sender_email}
        destination = [{"email":account_mail,"name":account_mail}]
        response_destination = {"name":brand_name,"email":brand_response_email}

        # Send Mail With SendInBlue
        response = sib_send_mail(subject=subject, html_content=verification_page, sender=sender, destination=destination, response_destination=response_destination)
        return response

    except Exception as e:
        logger.exception(f"GenrateVerificationMailError:  Email Verifiction and Account Activation template load failed, {e}")
        return "Not Sent"


def create_password_reset_mail(
        account_mail, active_color, 
        background_dark, background_light, brand_logo, 
        brand_name, reset_link, brand_response_email, 
        brand_sender_email,) -> str:
    """
        This function send the password reset email

        Params
        -------
        account_token: The token used to identify the account
        account_mail: The email associated with the account
        active_color: The brands main color
        background_dark: The dark shade of the brand colour used for backgrounds
        background_light: The light shade of the brand colour used for backgrounds
        brand_logo: A link to the brands logo
        brand_name: The name of the brand
        reset_link: The reset link being sent
        brand_response_email: The email account that receives a response 
            from the sent email
        brand_sender_email: The email account that is sending the email


        Returns
        -------
        response: returns a response "Sent" or Not Sent
    """

    try:
        path = f"{os.curdir}/mail_app/templates/password_reset.html"
        with open(path, "r+") as ht:
            reset_page = ht.read()
            reset_page = reset_page.replace("**active-color**",active_color)
            reset_page = reset_page.replace("**background-dark**",background_dark)
            reset_page = reset_page.replace("**background-light**",background_light)
            reset_page = reset_page.replace("**BRAND LOGO HERE**",brand_logo)
            reset_page = reset_page.replace("**BRAND NAME HERE**",brand_name.upper())
            reset_page = reset_page.replace("**RESET LINK**",reset_link)

        # Create a new API Instance
        subject = "Password Reset"
        sender = {"name": brand_name,"email":brand_sender_email}
        destination = [{"email":account_mail,"name":account_mail}]
        response_destination = {"name":brand_name,"email":brand_response_email}

        # Send Mail With SendInBlue
        response = sib_send_mail(
            subject=subject, 
            html_content=reset_page, 
            sender=sender, 
            destination=destination, 
            response_destination=response_destination
            )
        return response

    except Exception as e:
        logger.exception(f"SendResetPasswordMailError: Failed to Send Verification Mail,{e}")
        return "Not Sent"