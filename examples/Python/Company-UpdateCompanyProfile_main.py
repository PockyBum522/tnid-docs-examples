import aiohttp
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Please note that this basic example won't work if you have an asyncio event loop running.
# In some python environments (as with Jupyter which uses IPython) an asyncio event loop is created for you.
# In that case you should use instead https://gql.readthedocs.io/en/latest/async/async_usage.html#async-usage
def update_company_profile(bearer_token, legal_name = None, brand_name = None, profile_name = None, tax_id = None, year_founded = None, about_us = None, metadata = None):
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
                $legalName: String
                $brandName: String
                $profileName: String
                $taxId: String
                $yearFounded: Int
                $aboutUs: String
                $metadata: Json
              ) {
                updateCompany (
                legalName: $legalName
                brandName: $brandName
                profileName: $profileName
                taxId: $taxId
                yearFounded: $yearFounded
                aboutUs: $aboutUs
                metadata: $metadata
                ) {
                id
                legalName
                brandName
                profileName
                taxId
                yearFounded
                aboutUs
                metadata
                }
              }
        """
    )

    params = { "legalName": legal_name,
               "brandName": brand_name,
               "profileName": profile_name,
               "taxId": tax_id,
               "yearFounded": year_founded,
               "aboutUs": about_us,
               "metadata": metadata }

    try:
        # Execute the query on the transport
        response = client.execute(query, params)
        print(f"Response OK: {response}")
        return response
    except Exception as e:
        print(f"Exception: {e}")


# Example usage:
token = "your_company_token"
update_company_profile(token,
                       "Company new legal name",
                       "Company new brand name",
                       "Company new profile name",
                       "44-555555",
                       2003,
                       "New about us",
                       "{\"companyNumEmployees\": \"5\"}")
