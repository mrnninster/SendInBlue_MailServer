# Flask Email Sever With SendInBlue

![alt text](https://img.shields.io/badge/SendInBlue-7.6.2-blue?style=for-the-badge&$logo=SendInBlue)
![alt text](https://img.shields.io/badge/Flask-2.2.3-000000?style=for-the-badge&$logo=Flask)

I tend to think my desire tonot repeat oinga task more than once drives me to create code snippets
all ovet the place. More recently I have decide to build all these features into either simple django apps
that are self contained or apis easily served with flask.

This is one such examples. This is a simple email server built with flask, and It can be easily customized 
for your specific needs. It i built using SendInBlue, so you need a send in blue api key.

To run the app you will need an .env file in the mail_app folder containing the following values

```bash
DEBUG=False
PORT=5000
SECRET_KEY=youSECRETkey
SENDINBLUE_API_KEY=yourSIBkey
JWT_KEY=yourJWTENCODINGkey
```
The data sent to the api is a payload of a JWT encoded token, a sample would look like this

```python
    payload={
        "active_color": color,                  # Used in formatting the html
        "background_light": light_color,        # Used in formatting the html
        "background_dark": dark_colour,         # Used in formatting the html
        "email": email,                         
        "user_type": account,
        "brand_logo": logo_url,
        "brand_name": brand_name,
        "brand_message": brand_message,
        "verification_link": f"http://127.0.0.1:8000/verify_mail/{encoded_user_id_payload}",
        "sender_name": sender_name,
        "closing_remark": closing_remark,
        "brand_sender_email": brand_sender_email,
        "brand_response_email": brand_response_email,
        "closure":"A hearty welcome!"
        }

    encoded_payload = jwt.encode(payload, encoding_key, "HS256")
```

This data is then decoded and used to create the email before it is sent.


This repo comes with an account verification and password reset template which are in the [templates](mail_app/templates/)
folder. These html files are formatted using the functions defined in [Functions](mail_app/functions.py).


To start the app simply run

```bash
python app.py
```

I do hope you find this useful

:star: I'd be delighted ifyou starred this project.

Enjoy!