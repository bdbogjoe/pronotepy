from bs4 import BeautifulSoup
import requests
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def atrium_sud(username, password):
    """
    ENT for Atrium Sud
    :param username:
    :param password:
    :return:
    """
    # ENT / PRONOTE required URLs
    ent_login = 'https://www.atrium-sud.fr/connexion/login?service=https:%2F%2F0060013G.index-education.net%2Fpronote%2F'

    # Required Headers
    headers = {
        'connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'}

    # ENT Connection
    session = requests.Session()
    response = session.get(ent_login, headers=headers)

    log.debug('[ENT Atrium] Logging in with ' + username)

    # Login payload
    soup = BeautifulSoup(response.text, 'html.parser')
    input_ = soup.find('input', {'type': 'hidden', 'name': 'lt'})
    lt = input_.get('value')

    input_ = soup.find('input', {'type': 'hidden', 'name': 'execution'})
    execution = input_.get('value')

    payload = {
        'execution': execution,
        '_eventId': 'submit',
        'submit': '',
        'lt': lt,
        'username': username,
        'password': password}

    # Send user:pass to the ENT
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    response = session.post(ent_login, headers=headers, data=payload, cookies=cookies)
    return requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))


def occitanie_montpellier(username, password):
    """
    ENT for Occitanie Montpellier
    :param username:
    :param password:
    :return:
    """
    # Required Headers
    headers = {
        'connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'}
    # Login payload
    payload = {
        'auth_mode': 'BASIC',
        'orig_url': '%2Ffim42%2Fsso%2FSSO%3FSPEntityID%3Dsp-ent-entmip-prod',
        'user': username,
        'password': password}
    # ENT / PRONOTE required URLs
    ent_login = 'https://famille.ac-montpellier.fr/login/ct_logon_vk.jsp?CT_ORIG_URL=/fim42/sso/SSO?SPEntityID=sp-ent-entmip-prod&ct_orig_uri=/fim42/sso/SSO?SPEntityID=sp-ent-entmip-prod'
    ent_verif = 'https://famille.ac-montpellier.fr/aten-web/connexion/controlesConnexion?CT_ORIG_URL=%2Ffim42%2Fsso%2FSSO%3FSPEntityID%3Dsp-ent-entmip-prod&amp;ct_orig_uri=%2Ffim42%2Fsso%2FSSO%3FSPEntityID%3Dsp-ent-entmip-prod'
    pronote_verif = 'https://cas.mon-ent-occitanie.fr/saml/SAMLAssertionConsumer'
    # ENT Connection
    session = requests.Session()
    response = session.get(ent_login, headers=headers)
    log.debug('[ENT Occitanie] Logging in with ' + username)
    # Send user:pass to the ENT
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    response = session.post(ent_login, headers=headers, data=payload, cookies=cookies)
    # Get the CAS verification shit
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    response = session.get(ent_verif, headers=headers, cookies=cookies)
    # Get the actual values
    soup = BeautifulSoup(response.text, 'html.parser')
    cas_infos = dict()
    inputs = soup.findAll('input', {'type': 'hidden'})
    for input_ in inputs:
        cas_infos[input_.get('name')] = input_.get('value')
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    session.cookies.update({'SERVERID': 'entmip-prod-web4', 'preselection': 'MONTP-ATS_parent_eleve'})
    response = session.post(pronote_verif, headers=headers, data=cas_infos, cookies=cookies)
    # Get Pronote
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    return cookies
