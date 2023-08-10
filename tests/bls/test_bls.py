from indy_bls import (
    Bls,
    SignKey,
    VerKey,
    MultiSignature,
)


def test_sign(signature1):
    assert signature1 is not None


def test_sign_for_seed(signature2):
    assert signature2 is not None


def test_verify(generator, message, ver_key1, signature1):
    valid = Bls.verify(signature1, message, ver_key1, generator)
    assert valid


def test_verify_pop(generator, ver_key1, pop):
    valid = Bls.verify_pop(pop, ver_key1, generator)
    assert valid


def test_verify_for_seed(generator, message, ver_key2, signature2):
    valid = Bls.verify(signature2, message, ver_key2, generator)
    assert valid


def test_verify__multi_sig_works(generator, message, multi_sig, ver_key1, ver_key2):
    valid = Bls.verify_multi_sig(multi_sig, message, [ver_key1, ver_key2], generator)
    assert valid


def test_verify_multi_sig_works_for_invalid_signature(generator, message):
    sign_key1 = SignKey.new(None)
    ver_key1 = VerKey.new(generator, sign_key1)

    sign_key2 = SignKey.new(None)
    ver_key2 = VerKey.new(generator, SignKey.new(None))

    signature1 = Bls.sign(message, sign_key1)
    signature2 = Bls.sign(message, sign_key2)
    multi_signature_invalid = MultiSignature.new([signature1, signature2])

    valid = Bls.verify_multi_sig(
        multi_signature_invalid, message, [ver_key1, ver_key2], generator
    )
    assert not valid
