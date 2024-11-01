﻿import aiohttp
import pprint
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Please note that this basic example won't work if you have an asyncio event loop running.
# In some python environments (as with Jupyter which uses IPython) an asyncio event loop is created for you.
# In that case you should use instead https://gql.readthedocs.io/en/latest/async/async_usage.html#async-usage
def get_full_company_endpoint_schema(bearer_token):
    transport = AIOHTTPTransport(
        url="https://api.staging.v2.tnid.com/company",
        headers=
        {
            "Authorization": f"Bearer {bearer_token}"
        }
    )

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Make a valid query so that gql can fetch the full schema
    query = gql(
        """
        query (
            $name: String
            $taxId: String
            $email: String
            $telephoneNumber: String
            $webpage: String
            $limit: Int
          ) {
            companies (
            name: $name
            taxId: $taxId
            email: $email
            telephoneNumber: $telephoneNumber
            webpage: $webpage
            limit: $limit
            ) {
            id
            legalName
            brandName
            profileName
            taxId
            }
          }
        """
    )

    params = { "name": "schema query" }

    try:
        # Execute the query on the transport
        response = client.execute(query, params)

        # Working with the schema GQL gave us from the server
        schema = client.introspection

        print(f"Response OK: {response}")

        # Pretty print out the schema to the console
        print("Schema: ")
        pprint.pp(schema)

        return response
    except Exception as e:
        print(f"Exception: {e}")


def get_full_user_endpoint_schema(bearer_token, query_name = None, tax_id = None, email = None, phone_number = None, webpage = None, limit_count = 10):
    transport = AIOHTTPTransport(
        url="https://api.staging.v2.tnid.com/user",
        headers=
        {
            "Authorization": f"Bearer {bearer_token}"
        }
    )

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Make a valid query so that gql can fetch the full schema
    query = gql(
        """
        query (
            $channelType: SpamReportChannelType
            $issueType: SpamReportIssueType
            $includedStatus: SpamReportStatus
            $excludedStatus: SpamReportStatus
            $limit: Int
          ) {
            spamReports (
            channelType: $channelType
            issueType: $issueType
            includedStatus: $includedStatus
            excludedStatus: $excludedStatus
            limit: $limit
            ) {
            id
            fromNumber
            toNumber
            userNote
            messageContent
            channelType
            issueType
            status
            createdAt
            updatedAt
            timestamp
            metadata
            user {
                id
            }
            }
          }
        """
    )

    params = { "limit": 1 }

    try:
        # Execute the query on the transport
        response = client.execute(query, params)

        # Working with the schema GQL gave us from the server
        schema = client.introspection

        print(f"Response OK: {response}")

        # Pretty print out the schema to the console
        print("Schema: ")
        pprint.pp(schema)

        return response
    except Exception as e:
        print(f"Exception: {e}")


# Example usage:
token = "your_company_token"
get_full_company_endpoint_schema(token)

# OR
# token = "your_user_token"
# get_full_user_endpoint_schema(token)