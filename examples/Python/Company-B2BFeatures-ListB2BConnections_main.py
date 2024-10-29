import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Please note that this basic example won't work if you have an asyncio event loop running.
# In some python environments (as with Jupyter which uses IPython) an asyncio event loop is created for you.
# In that case you should use instead https://gql.readthedocs.io/en/latest/async/async_usage.html#async-usage
def list_b2b_connections(bearer_token, include_type = None, exclude_type = None, limit_count = 10):
    transport = AIOHTTPTransport(
        url="https://api.staging.v2.tnid.com/company",
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
                $includedType: B2bConnectionType
                $excludedType: B2bConnectionType
                $limit: Int
              ) {
                b2bConnect ions (
                includedType: $includedType
                excludedType: $excludedType
                limit: $limit
                ) {
                id
                type
                createdAt
                updatedAt
                startedAt
                company {
                    id
                }
                connectedCompany {
                    id
                }
                }
              }
        """
    )

    params = { "includedType": include_type, "excludedType": exclude_type, "limit": limit_count }

    try:
        # Execute the query on the transport
        response = client.execute(query, params)
        print(f"Response OK: {response}")
        return response
    except Exception as e:
        print(f"Exception: {e}")


# Example usage:
token = "your_company_token"
list_b2b_connections(token)
