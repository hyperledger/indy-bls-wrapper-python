from ursa.bls import SignKey


def test_new(sign_key1):
    assert sign_key1 is not None


def test_new_for_seed(sign_key2):
    assert sign_key2 is not None


def test_as_bytes(sign_key1):
    xbytes = sign_key1.as_bytes()
    assert len(xbytes) > 0


def test_from_bytes(sign_key1):
    xbytes = sign_key1.as_bytes()

    sign_key12 = SignKey.from_bytes(xbytes)
    assert type(sign_key12) is SignKey

    xbytes2 = sign_key12.as_bytes()
    assert xbytes == xbytes2
