"""Connectivity probe for Batch 0A canonical PDF acquisition.

Read-only. Issues HEAD then a bounded ranged GET. No file is written.
Purpose: determine which TLS stack on this host can reach the canonical
sources, BEFORE any downloader is implemented.
"""
import ssl
import sys
import urllib.request
import urllib.error

TIMEOUT = 25
UA = "wam-corpus-ingest/1.0 (research asset acquisition; contact: local)"


def probe(url):
    print(f"--- {url}")
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            print(f"    HEAD status={r.status} type={r.headers.get('Content-Type')} "
                  f"len={r.headers.get('Content-Length')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"    HEAD HTTPError {e.code} {e.reason}")
    except Exception as e:
        print(f"    HEAD FAILED {type(e).__name__}: {e}")
    # bounded ranged GET fallback (some hosts reject HEAD)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Range": "bytes=0-63"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            head = r.read(16)
            print(f"    GET  status={r.status} type={r.headers.get('Content-Type')} "
                  f"magic={head[:5]!r}")
            return True
    except urllib.error.HTTPError as e:
        print(f"    GET  HTTPError {e.code} {e.reason}")
    except Exception as e:
        print(f"    GET  FAILED {type(e).__name__}: {e}")
    return False


def main():
    print(f"python      : {sys.version.split()[0]}")
    print(f"ssl         : {ssl.OPENSSL_VERSION}")
    print(f"TLS verify  : ON (default context)")
    try:
        import certifi
        print(f"certifi     : {certifi.where()}")
    except Exception as e:
        print(f"certifi     : not installed ({type(e).__name__})")
    print()
    urls = sys.argv[1:]
    for u in urls:
        probe(u)


if __name__ == "__main__":
    main()
