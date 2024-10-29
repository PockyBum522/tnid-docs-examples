from datetime import datetime

import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Please note that this basic example won't work if you have an asyncio event loop running.
# In some python environments (as with Jupyter which uses IPython) an asyncio event loop is created for you.
# In that case you should use instead https://gql.readthedocs.io/en/latest/async/async_usage.html#async-usage
def user_create_spam_report(bearer_token, from_number = None, to_number = None, channel_type = None, timestamp = None, issue_type = None, user_note = None, message_content = None, metadata = None):
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
                $fromNumber: String!
                $toNumber: String!
                $channelType: SpamReportChannelType!
                $timestamp: NaiveDateTime!
                $issueType: SpamReportIssueType
                $userNote: String
                $messageContent: String
                $metadata: Json
              ) {
                createSpamReport (
                fromNumber: $fromNumber
                toNumber: $toNumber
                channelType: $channelType
                timestamp: $timestamp
                issueType: $issueType
                userNote: $userNote
                messageContent: $messageContent
                metadata: $metadata
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

    params = { "fromNumber": from_number,
               "toNumber": to_number,
               "channelType": channel_type,
               "timestamp": timestamp,
               "issueType": issue_type,
               "userNote": user_note,
               "messageContent": message_content,
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
user_create_spam_report(token,
                        "15555555555",
                        "16666666666",
                        "MMS",
                        "2023-10-31 11:30:00",
                        "SPAM",
                        "Note about the report",
                        "Original message content",
                        "{ \"customField\": \"custom value\" }" )