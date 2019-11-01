import pubhost from '../assets/pubhost.json'
const callbackUrl = 'https://' + pubhost[0].PUBHOST_URL

export const AUTH_CONFIG = {
  clientId: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  domain: 'xxxxxxxxxx.auth0.com',
  callbackUrl: callbackUrl,
  audience: 'https://xxxxxxxx',
  apiUrl: 'https://xxxxxxxx'
}
