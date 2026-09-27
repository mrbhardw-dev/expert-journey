"""Minimal Zoho OAuth + REST client. Defaults to the EU data centre (Irish accounts)."""
import logging
import os
import time

import requests

log = logging.getLogger(__name__)

RETRY_STATUSES = {429, 500, 502, 503, 504}


class ZohoError(RuntimeError):
    pass


class ZohoClient:
    """Talks to one Zoho API domain. Writes are skipped (and logged) when dry_run is on."""

    def __init__(self, client_id, client_secret, refresh_token, api_domain,
                 accounts_url="https://accounts.zoho.eu", dry_run=True, session=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.api_domain = api_domain.rstrip("/")
        self.accounts_url = accounts_url.rstrip("/")
        self.dry_run = dry_run
        self.session = session or requests.Session()
        self._access_token = None

    @classmethod
    def from_env(cls, api_domain_var, default_domain, dry_run=True):
        required = ["ZOHO_CLIENT_ID", "ZOHO_CLIENT_SECRET", "ZOHO_REFRESH_TOKEN"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            raise ZohoError("Missing environment variables: " + ", ".join(missing))
        return cls(
            os.environ["ZOHO_CLIENT_ID"],
            os.environ["ZOHO_CLIENT_SECRET"],
            os.environ["ZOHO_REFRESH_TOKEN"],
            api_domain=os.environ.get(api_domain_var) or default_domain,
            accounts_url=os.environ.get("ZOHO_ACCOUNTS_URL") or "https://accounts.zoho.eu",
            dry_run=dry_run,
        )

    def _refresh(self):
        r = self.session.post(f"{self.accounts_url}/oauth/v2/token", params={
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
        }, timeout=30)
        body = r.json() if r.content else {}
        token = body.get("access_token")
        if not token:
            # Never log the request: it contains the secret.
            raise ZohoError(f"Zoho token refresh failed: {body.get('error', r.status_code)}")
        self._access_token = token

    def request(self, method, path, params=None, json=None):
        method = method.upper()
        if method != "GET" and self.dry_run:
            log.info("[dry-run] would %s %s", method, path)
            return None
        if self._access_token is None:
            self._refresh()
        url = self.api_domain + path
        for attempt in range(5):
            r = self.session.request(method, url, params=params, json=json, timeout=60, headers={
                "Authorization": f"Zoho-oauthtoken {self._access_token}",
            })
            if r.status_code == 401 and attempt == 0:
                self._refresh()
                continue
            if r.status_code in RETRY_STATUSES and attempt < 4:
                time.sleep(2 ** (attempt + 1))
                continue
            break
        if r.status_code == 204:
            return {}
        try:
            body = r.json()
        except ValueError:
            body = {"raw": r.text[:500]}
        if r.status_code >= 400:
            raise ZohoError(f"{method} {path} -> HTTP {r.status_code}: {body}")
        return body

    def get(self, path, params=None):
        return self.request("GET", path, params=params)

    def post(self, path, params=None, json=None):
        return self.request("POST", path, params=params, json=json)

    def put(self, path, params=None, json=None):
        return self.request("PUT", path, params=params, json=json)
