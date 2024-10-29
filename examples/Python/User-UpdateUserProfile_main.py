from datetime import datetime

import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Please note that this basic example won't work if you have an asyncio event loop running.
# In some python environments (as with Jupyter which uses IPython) an asyncio event loop is created for you.
# In that case you should use instead https://gql.readthedocs.io/en/latest/async/async_usage.html#async-usage
def user_update_profile(bearer_token, username = None, first_name = None, last_name = None, middle_name = None, birthdate = None, about_me = None, metadata = None):
    transport = AIOHTTPTransport(
        url="https://api.staging.v2.tnid.com/user",
        headers=
        {
            "Authorization": f"Bearer {bearer_token}"
        }
    )

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
            """
             mutation (
                $username: String
                $firstName: String
                $lastName: String
                $middleName: String
                $birthdate: Date
                $aboutMe: String
                $metadata: Json
              ) {
                updateUser (
                username: $username
                firstName: $firstName
                lastName: $lastName
                middleName: $middleName
                birthdate: $birthdate
                aboutMe: $aboutMe
                metadata: $metadata
                ) {
                id
                username
                firstName
                lastName
                middleName
                birthdate
                aboutMe
                metadata
                }
              }
            """
    )

    params = { "username": username,
               "firstName": first_name,
               "lastName": last_name,
               "middleName": middle_name,
               "birthdate": birthdate,
               "aboutMe": about_me,
               "metadata": metadata }

    try:
        # Execute the query on the transport
        response = client.execute(query, params)
        print(f"Response OK: {response}")
        return response
    except Exception as e:
        print(f"Exception: {e}")


# Example usage:
token = "your_user_token"
user_update_profile(token, "username", "John", "Smith")