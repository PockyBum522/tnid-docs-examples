from datetime import datetime

import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Please note that this basic example won't work if you have an asyncio event loop running.
# In some python environments (as with Jupyter which uses IPython) an asyncio event loop is created for you.
# In that case you should use instead https://gql.readthedocs.io/en/latest/async/async_usage.html#async-usage
def user_list_spam_reports(bearer_token, channel_type = None, issue_type = None, included_status = None, excluded_status = None, limit_count = 10):
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

    params = { "channelType": channel_type,
               "issueType": issue_type,
               "includedStatus": included_status,
               "excludedStatus": excluded_status,
               "limit": limit_count }

    try:
        # Execute the query on the transport
        response = client.execute(query, params)
        print(f"Response OK: {response}")
        return response
    except Exception as e:
        print(f"Exception: {e}")


# Example usage:
token = "your_user_token"
user_list_spam_reports(token, "MMS")