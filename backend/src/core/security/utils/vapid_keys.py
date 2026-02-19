"""
Generate VAPID key pair for Web Push notifications.
Run: python -c "from core.security.utils.vapid_keys import generate_vapid_keys; generate_vapid_keys()"
Or via manage.py: python src/manage.py generate-vapid-keys
"""


def generate_vapid_keys() -> dict:
    """Generate a VAPID key pair and print them for .env configuration."""
    from py_vapid import Vapid

    vapid = Vapid()
    vapid.generate_keys()

    # Get the raw key bytes
    private_key = vapid.private_pem()
    public_key = vapid.public_key

    # For applicationServerKey we need the raw uncompressed point
    import base64
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        PublicFormat,
    )

    raw_public = public_key.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    public_key_b64 = base64.urlsafe_b64encode(raw_public).rstrip(b"=").decode("ascii")

    # Private key in PEM (single-line for .env)
    private_key_str = private_key.decode("utf-8").strip()
    # For pywebpush, use the raw private number as base64url
    from cryptography.hazmat.primitives.serialization import (
        load_pem_private_key,
    )

    priv = load_pem_private_key(private_key, password=None)
    priv_numbers = priv.private_numbers()
    priv_bytes = priv_numbers.private_value.to_bytes(32, "big")
    private_key_b64 = base64.urlsafe_b64encode(priv_bytes).rstrip(b"=").decode("ascii")

    result = {
        "public_key": public_key_b64,
        "private_key": private_key_b64,
    }

    print("\n" + "=" * 60)
    print("  VAPID Keys Generated — Add these to your .env file")
    print("=" * 60)
    print(f"\nVAPID_PUBLIC_KEY={public_key_b64}")
    print(f"VAPID_PRIVATE_KEY={private_key_b64}")
    print(f"VAPID_CLAIMS_EMAIL=mailto:your-email@example.com")
    print("\n" + "=" * 60 + "\n")

    return result
