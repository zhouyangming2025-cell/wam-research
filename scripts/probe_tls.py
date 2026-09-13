"""Diagnose the arXiv TLS chain failure WITHOUT disabling verification.

Read-only. Tries, in order:
  1. urllib with the system default trust store
  2. urllib with an explicit certifi CA bundle
  3. requests (if installed) which uses certifi by default
and prints the peer certificate issuer/subject so an intercepting proxy is visible.
"""
import socket
import ssl
import sys
import urllib.request
import urllib.error

URL = "https://arxiv.org/pdf/2506.24113"
HOST = "arxiv.org"
TIMEOUT = 30
UA = "wam-corpus-ingest/1.0"


def show_peer_cert(host):
    print(f"[cert] connecting to {host}:443 for inspection")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=TIMEOUT) as raw:
            with ctx.wrap_socket(raw, server_hostname=host) as s:
                c = s.getpeercert()
                print(f"[cert] verified OK")
                print(f"[cert] subject={c.get('subject')}")
                print(f"[cert] issuer={c.get('issuer')}")
    except Exception as e:
        print(f"[cert] default-store verification failed: {type(e).__name__}: {e}")
        # re-inspect without verifying, ONLY to identify who signed it
        try:
            ctx = ssl._create_unverified_context()
            with socket.create_connection((host, 443), timeout=TIMEOUT) as raw:
                with ctx.wrap_socket(raw, server_hostname=host) as s:
                    der = s.getpeercert(binary_form=True)
                    print(f"[cert] peer presented cert, DER len={len(der)} (NOT verified)")
                    import hashlib
                    print(f"[cert] sha256={hashlib.sha256(der).hexdigest()}")
        except Exception as e2:
            print(f"[cert] inspection also failed: {type(e2).__name__}: {e2}")


def try_urllib(label, ctx):
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Range": "bytes=0-63"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            print(f"[{label}] OK status={r.status} magic={r.read(5)!r}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[{label}] HTTPError {e.code} {e.reason}")
    except Exception as e:
        print(f"[{label}] FAILED {type(e).__name__}: {e}")
    return False


print(f"python={sys.version.split()[0]}  openssl={ssl.OPENSSL_VERSION}")
print(f"default verify paths: {ssl.get_default_verify_paths()}")
print()

show_peer_cert(HOST)
print()

try_urllib("system-default-store", ssl.create_default_context())

try:
    import certifi
    print(f"[certifi] {certifi.where()}")
    try_urllib("certifi-bundle", ssl.create_default_context(cafile=certifi.where()))
except ImportError:
    print("[certifi] not installed")

try:
    import requests
    print(f"[requests] {requests.__version__}")
    try:
        r = requests.get(URL, headers={"User-Agent": UA, "Range": "bytes=0-63"},
                         timeout=TIMEOUT, allow_redirects=True)
        print(f"[requests] OK status={r.status_code} magic={r.content[:5]!r}")
    except Exception as e:
        print(f"[requests] FAILED {type(e).__name__}: {e}")
except ImportError:
    print("[requests] not installed")
