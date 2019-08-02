from ursa.bls import MultiSignature


def test_new(multi_sig):
    assert multi_sig is not None


def test_as_bytes(multi_sig):
    xbytes = multi_sig.as_bytes()
    assert len(xbytes) > 0


def test_from_bytes(multi_sig):
    xbytes = multi_sig.as_bytes()

    multi_sig2 = MultiSignature.from_bytes(xbytes)
    assert type(multi_sig2) is MultiSignature

    xbytes2 = multi_sig2.as_bytes()
    assert xbytes == xbytes2
