from indy_bls import (
    Bls,
    Generator,
    SignKey,
    VerKey,
    ProofOfPossession,
    Signature,
    MultiSignature,
)

import pytest


@pytest.fixture
def generator():
    gen = Generator.new()

    assert type(gen) is Generator
    assert gen.c_instance is not None
    return gen


@pytest.fixture
def sign_key1():
    sign_key = SignKey.new(None)

    assert type(sign_key) is SignKey
    assert sign_key.c_instance is not None
    return sign_key


@pytest.fixture
def sign_key2():
    seed = bytes(
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            21,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            31,
            32,
        ]
    )
    sign_key = SignKey.new(seed)

    assert type(sign_key) is SignKey
    assert sign_key.c_instance is not None
    return sign_key


@pytest.fixture
def ver_key1(generator, sign_key1):
    ver_key = VerKey.new(generator, sign_key1)

    assert type(ver_key) is VerKey
    assert ver_key.c_instance is not None
    return ver_key


@pytest.fixture
def ver_key2(generator, sign_key2):
    ver_key = VerKey.new(generator, sign_key2)

    assert type(ver_key) is VerKey
    assert ver_key.c_instance is not None
    return ver_key


@pytest.fixture
def message():
    return bytes([1, 2, 3, 4, 5])


@pytest.fixture
def signature1(message, sign_key1):
    signature = Bls.sign(message, sign_key1)

    assert type(signature) is Signature
    assert signature.c_instance is not None
    return signature


@pytest.fixture
def signature2(message, sign_key2):
    signature = Bls.sign(message, sign_key2)

    assert type(signature) is Signature
    assert signature.c_instance is not None
    return signature


@pytest.fixture
def pop(ver_key1, sign_key1):
    pop = ProofOfPossession.new(ver_key1, sign_key1)

    assert type(pop) is ProofOfPossession
    assert pop.c_instance is not None
    return pop


@pytest.fixture
def multi_sig(signature1, signature2):
    multi_sig = MultiSignature.new([signature1, signature2])

    assert type(multi_sig) is MultiSignature
    assert multi_sig.c_instance is not None
    return multi_sig
