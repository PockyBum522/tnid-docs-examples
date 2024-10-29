import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Please note that this basic example won't work if you have an asyncio event loop running.
# In some python environments (as with Jupyter which uses IPython) an asyncio event loop is created for you.
# In that case you should use instead https://gql.readthedocs.io/en/latest/async/async_usage.html#async-usage
def invite_company(bearer_token, company_to_invite = None, company_representatives = None, connection_type = None):
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
            mutation (
                $company: CompanyInput!
                $representatives: [InviteUserInput!]!
                $connectionType: B2bConnectionType!
              ) {
                createB2bInvite (
                company: $company
                representatives: $representatives
                connectionType: $connectionType
                ) {
                id
                status
                type
                insertedAt
                respondedAt
                updatedAt
                company {
                    id
                }
                user {
                    id
                }
                invitedCompany {
                    id,
                    legalName,
                    brandName,
                    taxId
                  }
                }
              }
        """
    )

    params = { "company": company_to_invite, "representatives": company_representatives, "connectionType": connection_type }

    try:
        # Execute the query on the transport
        response = client.execute(query, params)
        print(f"Response OK: {response}")
        return response
    except Exception as e:
        print(f"Exception: {e}")


# Example usage:
company_to_invite = { "legalName": "Acme Metals" }
company_representative = { "email": "user@acme-metals-domain.com", "first_name": "Jane", "last_name": "Smith" }

token = "your_company_token"
invite_company(token, company_to_invite, company_representative, "PARTNER")
