import requests

api_key = '3gpZHxFgo-5bH_L6J9R27g'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'linkedin_profile_url': 'https://www.linkedin.com/in/fany-yoana-reyes-barrera-65452b35/'
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)