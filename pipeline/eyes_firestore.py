"""Firestore helpers for Eyes mode cloud backup (project second-sun-faea5).
PUBLIC side (what the book does): create one document per finished round with the public web API key; rules allow create only.
ADMIN side (what Claude's reader does): the service-account key in D:\\second-sun-secrets (NEVER printed, never committed) may read and delete.
Documents are typed values (stringValue, integerValue ...); enc/dec convert them. Used by eyes_scores.py and eyes_rules_test.py."""
import pathlib
import requests

PROJECT = "second-sun-faea5"
API_KEY = "AIzaSyBogX_Jte_4fahJ1Ovp3y-twCmxheLTSxY"          # public web key (every Firebase site exposes it); the security rules are the protection
BASE = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"
KEY_DIR = pathlib.Path(r"D:\second-sun-secrets")
COLLECTION = "eyes_rounds"


def key_path():
    m = sorted(KEY_DIR.glob("*firebase-adminsdk*.json"))
    if not m:
        raise SystemExit(f"service-account key not found in {KEY_DIR}")
    return m[0]


def admin_headers():
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    c = service_account.Credentials.from_service_account_file(str(key_path()), scopes=["https://www.googleapis.com/auth/datastore"])
    c.refresh(Request())
    return {"Authorization": "Bearer " + c.token}


def enc(v):
    if v is None: return {"nullValue": None}
    if isinstance(v, bool): return {"booleanValue": v}
    if isinstance(v, int): return {"integerValue": str(v)}
    if isinstance(v, float): return {"doubleValue": v}
    if isinstance(v, str): return {"stringValue": v}
    if isinstance(v, (list, tuple)): return {"arrayValue": {"values": [enc(x) for x in v]}}
    if isinstance(v, dict): return {"mapValue": {"fields": {k: enc(x) for k, x in v.items()}}}
    raise TypeError(type(v))


def dec(v):
    (t, x), = v.items()
    if t == "nullValue": return None
    if t == "booleanValue": return x
    if t == "integerValue": return int(x)
    if t == "doubleValue": return float(x)
    if t in ("stringValue", "timestampValue", "referenceValue"): return x
    if t == "arrayValue": return [dec(i) for i in x.get("values", [])]
    if t == "mapValue": return {k: dec(i) for k, i in x.get("fields", {}).items()}
    raise ValueError(t)


def doc_body(d):
    return {"fields": {k: enc(v) for k, v in d.items()}}


def public_create(doc_id, d, timeout=30):
    """What the book's uploader does: POST with only the public key. Returns the HTTP response."""
    return requests.post(f"{BASE}/{COLLECTION}", params={"documentId": doc_id, "key": API_KEY}, json=doc_body(d), timeout=timeout)


def list_rounds():
    """Admin read of every round (all pages), decoded."""
    h, out, token = admin_headers(), [], None
    while True:
        params = {"pageSize": 300, **({"pageToken": token} if token else {})}
        r = requests.get(f"{BASE}/{COLLECTION}", headers=h, params=params, timeout=60)
        r.raise_for_status()
        j = r.json()
        for d in j.get("documents", []):
            out.append({k: dec(v) for k, v in d["fields"].items()})
        token = j.get("nextPageToken")
        if not token:
            return out


def admin_delete(doc_id):
    return requests.delete(f"{BASE}/{COLLECTION}/{doc_id}", headers=admin_headers(), timeout=30)
