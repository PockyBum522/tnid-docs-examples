import requests

# You will need to run this as step one, after which the user will receive an OTP in their email.
# With that OTP, you can request the actual token
def get_bearer_token_otp_for_existing_user(user_phone_number):
    url = "https://api.staging.v2.tnid.com/auth/create_user_otp"

    # Define the headers and body of the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # The payload or data to be sent in the POST request
    data = {
        "telephone_number": user_phone_number
    }

    # Make the POST request to the token endpoint
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Response OK when requesting OTP: {response.status_code} {response.text}")
    else:
        raise Exception(f"Failed to request OTP: {response.status_code} {response.text}")


# This is step two, to request the bearer token once you have an OTP
def get_bearer_token(user_phone_number, otp):
    url = "https://api.staging.v2.tnid.com/auth/token"

    # Define the headers and body of the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # The payload or data to be sent in the POST request
    data = {
        "telephone_number": user_phone_number,
        "otp_code": otp
    }

    # Make the POST request to the token endpoint
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response and extract the access token
        token_data = response.json()
        return token_data.get("access_token")
    else:
        raise Exception(f"Failed to retrieve token: {response.status_code} {response.text}")


# Create a new user, after which you will have to request their OTP, then bearer token using the other provided functions
def create_new_user(phone_number, first_name, last_name, email):
    url = "https://api.staging.v2.tnid.com/auth/create_user_otp"

    # Define the headers of the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # The payload or data to be sent in the POST request
    data = {
        "telephone_number": phone_number,
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }

    # Make the POST request to the token endpoint
    response = requests.post(url, headers=headers, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Response OK when creating new user: {response.status_code} {response.text}")
    else:
        raise Exception(f"Failed to create new user: {response.status_code} {response.text}")


query_phone_number = "14075554530"

get_bearer_token_otp_for_existing_user(query_phone_number)

print("Please check your email and enter the OTP here: ")
otp_from_email = input()

bearer_token = get_bearer_token(query_phone_number, otp_from_email)
print("Bearer Token: ", bearer_token)

# OR:
# new_user_phone_number = "15555555555"
#
# create_new_user(new_user_phone_number, "Firstname", "Lastname", "user@email.com")
#
# get_bearer_token_otp_for_existing_user(new_user_phone_number)
#
# print("Please check your email and enter the OTP here: ")
# otp_from_email = input()
#
# bearer_token = get_bearer_token(new_user_phone_number, otp_from_email)
# print("Bearer Token: ", bearer_token)