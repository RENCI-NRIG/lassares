import secrets from '../assets/secrets.json'
import pubhost from '../assets/pubhost.json'

const clientId = secrets[0].CLIENT_ID
const domain = secrets[0].AUTH0_DOMAIN
const callbackUrl = 'https://' + pubhost[0].PUBHOST_URL
const apiIdentifier = secrets[0].API_IDENTIFIER

export const AUTH_CONFIG = {
  clientId: clientId,
  domain: domain,
  callbackUrl: callbackUrl,
  audience: apiIdentifier,
  apiUrl: apiIdentifier
}
