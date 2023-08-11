"""Public interface."""

import logging

from ctypes import POINTER, byref, c_bool, c_char_p, c_int32, c_int64, c_ubyte, c_void_p
from typing import Optional
from weakref import finalize

from .lib import do_call

LOGGER = logging.getLogger(__name__)


def _free(method, value):
    do_call(method, value)


class BlsEntity:
    """Base class for BLS Entities."""

    new_handler = None
    from_bytes_handler = None
    as_bytes_handler = None
    free_handler = None

    def __init__(self, c_instance):
        """Initializer."""
        LOGGER.debug("BlsEntity.__init__: >>> self: %r, instance: %r", self, c_instance)

        self.c_instance = c_instance
        finalize(self, _free, self.free_handler, c_instance)

    @classmethod
    def from_bytes(cls, xbytes):
        """
        Create a BLS entity from the binary representation.

        :param xbytes: Bytes representation of Bls entity
        :return: BLS entity intance
        """
        LOGGER.debug("BlsEntity::from_bytes: >>>")

        c_instance = c_void_p()
        do_call(cls.from_bytes_handler, xbytes, len(xbytes), byref(c_instance))

        res = cls(c_instance)

        LOGGER.debug("BlsEntity::from_bytes: <<< res: %r", res)
        return res

    def as_bytes(self):
        """
        Return the BLS entity bytes representation.

        :return: BLS entity bytes representation
        """
        LOGGER.debug("BlsEntity.as_bytes: >>> self: %r", self)

        xbytes = POINTER(c_ubyte)()
        xbytes_len = c_int32()

        do_call(
            self.as_bytes_handler, self.c_instance, byref(xbytes), byref(xbytes_len)
        )
        res = bytes(xbytes[: xbytes_len.value])

        LOGGER.debug("BlsEntity.as_bytes: <<<")
        return res


class Generator(BlsEntity):
    """
    BLS generator point.

    The BLS algorithm requires choosing of generator point that must be known to
    all parties. Most methods require the generator to be provided.
    """

    new_handler = "indy_bls_generator_new"
    from_bytes_handler = "indy_bls_generator_from_bytes"
    as_bytes_handler = "indy_bls_generator_as_bytes"
    free_handler = "indy_bls_generator_free"

    @classmethod
    def new(cls):
        """Create and return a random generator point."""
        LOGGER.debug("Generator::new: >>>")

        c_instance = c_void_p()
        do_call(cls.new_handler, byref(c_instance))

        res = cls(c_instance)

        LOGGER.debug("Generator::new: <<< res: %r", res)
        return res


class SignKey(BlsEntity):
    """BLS signing key."""

    new_handler = "indy_bls_sign_key_new"
    from_bytes_handler = "indy_bls_sign_key_from_bytes"
    as_bytes_handler = "indy_bls_sign_key_as_bytes"
    free_handler = "indy_bls_sign_key_free"

    @classmethod
    def new(cls, seed: Optional[bytes] = None):
        """
        Create and return a random (or seeded from seed) BLS sign key.

        :param: seed - Optional seed.
        :return: BLS sign key
        """
        LOGGER.debug("SignKey::new: >>>")
        if seed and not isinstance(seed, bytes):
            raise ValueError("seed must be a bytes instance")

        c_instance = c_void_p()
        do_call(
            cls.new_handler,
            c_char_p(seed),
            c_int32(len(seed) if seed is not None else 0),
            byref(c_instance),
        )

        res = cls(c_instance)

        LOGGER.debug("SignKey::new: <<< res: %r", res)
        return res


class VerKey(BlsEntity):
    """BLS verification key."""

    new_handler = "indy_bls_ver_key_new"
    from_bytes_handler = "indy_bls_ver_key_from_bytes"
    as_bytes_handler = "indy_bls_ver_key_as_bytes"
    free_handler = "indy_bls_ver_key_free"

    @classmethod
    def new(cls, gen, sign_key):
        """
        Create and return a BLS verification.

        :param: gen - Generator
        :param: sign_key - Sign Key
        :return: BLS verification key
        """
        LOGGER.debug("VerKey::new: >>>")

        c_instance = c_void_p()
        do_call(cls.new_handler, gen.c_instance, sign_key.c_instance, byref(c_instance))

        res = cls(c_instance)

        LOGGER.debug("VerKey::new: <<< res: %r", res)
        return res


class ProofOfPossession(BlsEntity):
    """BLS proof of possession."""

    new_handler = "indy_bls_pop_new"
    from_bytes_handler = "indy_bls_pop_from_bytes"
    as_bytes_handler = "indy_bls_pop_as_bytes"
    free_handler = "indy_bls_pop_free"

    @classmethod
    def new(cls, ver_key, sign_key):
        """
        Create and return a BLS proof of possession.

        :param: ver_key - Ver Key
        :param: sign_key - Sign Key
        :return: BLS proof of possession
        """
        LOGGER.debug("ProofOfPossession::new: >>>")

        c_instance = c_void_p()
        do_call(
            cls.new_handler, ver_key.c_instance, sign_key.c_instance, byref(c_instance)
        )

        res = cls(c_instance)

        LOGGER.debug("ProofOfPossession::new: <<< res: %r", res)
        return res


class Signature(BlsEntity):
    """BLS signature."""

    new_handler = None
    from_bytes_handler = "indy_bls_signature_from_bytes"
    as_bytes_handler = "indy_bls_signature_as_bytes"
    free_handler = "indy_bls_signature_free"


class MultiSignature(BlsEntity):
    """BLS multi signature."""

    new_handler = "indy_bls_multi_signature_new"
    from_bytes_handler = "indy_bls_multi_signature_from_bytes"
    as_bytes_handler = "indy_bls_multi_signature_as_bytes"
    free_handler = "indy_bls_multi_signature_free"

    @classmethod
    def new(cls, signatures):
        """
        Create and return a BLS multi signature.

        :param: signature - List of signatures
        :return: BLS multi signature
        """
        LOGGER.debug("MultiSignature::new: >>>")

        # noinspection PyCallingNonCallable,PyTypeChecker
        signature_c_instances = (c_void_p * len(signatures))()
        for i in range(len(signatures)):
            signature_c_instances[i] = signatures[i].c_instance

        c_instance = c_void_p()
        do_call(
            cls.new_handler,
            signature_c_instances,
            c_int32(len(signatures)),
            byref(c_instance),
        )

        res = cls(c_instance)

        LOGGER.debug("MultiSignature::new: <<< res: %r", res)
        return res


class Bls:
    """Provides BLS methods."""

    @staticmethod
    def sign(message, sign_key):
        """
        Sign the message and return the signature.

        :param: message - Message to sign
        :param: sign_key - Sign key
        :return: Signature
        """
        LOGGER.debug("Bls::sign: >>> message: %r, sign_key: %r", message, sign_key)

        c_instance = c_void_p()
        do_call(
            "indy_bls_sign",
            c_char_p(message),
            c_int64(len(message)),
            sign_key.c_instance,
            byref(c_instance),
        )

        res = Signature(c_instance)

        LOGGER.debug("Bls::sign: <<< res: %r", res)
        return res

    @staticmethod
    def verify(signature, message, ver_key, gen):
        """
        Verify the message signature.

        :param: signature - Signature to verify
        :param: message - Message to verify
        :param: ver_key - Verification key
        :param: gen - Generator point
        :return: true if the signature is valid, false otherwise
        """
        LOGGER.debug(
            "Bls::verify: >>> signature: %r, message: %r, ver_key: %r, gen: %r",
            signature,
            message,
            ver_key,
            gen,
        )

        valid = c_bool()
        do_call(
            "indy_bls_verify",
            signature.c_instance,
            c_char_p(message),
            c_int64(len(message)),
            ver_key.c_instance,
            gen.c_instance,
            byref(valid),
        )

        res = valid
        LOGGER.debug("Bls::verify: <<< res: %r", res)
        return res

    @staticmethod
    def verify_pop(pop, ver_key, gen):
        """
        Verifiy the proof of possession.

        :param: pop - Proof of possession
        :param: ver_key - Verification key
        :param: gen - Generator point
        :return: true if the signature is valid, false otherwise
        """
        LOGGER.debug(
            "Bls::verify_pop: >>> pop: %r, ver_key: %r, gen: %r", pop, ver_key, gen
        )

        valid = c_bool()
        do_call(
            "indy_bls_verify_pop",
            pop.c_instance,
            ver_key.c_instance,
            gen.c_instance,
            byref(valid),
        )

        res = valid
        LOGGER.debug("Bls::verify_pop: <<< res: %r", res)
        return res

    @staticmethod
    def verify_multi_sig(multi_sig, message, ver_keys, gen):
        """
        Verifiy the message multi signature.

                :param: multi_sig - Multi signature to verify
        :param: message - Message to verify
        :param: ver_keys - List of verification keys
        :param: gen - Generator point
        :return: true if the multi signature is valid, false otherwise
        """
        LOGGER.debug(
            (
                "Bls::verify_multi_sig: >>> multi_sig: %r, message: %r, "
                "ver_keys: %r, gen: %r"
            ),
            multi_sig,
            message,
            ver_keys,
            gen,
        )

        # noinspection PyCallingNonCallable,PyTypeChecker
        ver_key_c_instances = (c_void_p * len(ver_keys))()
        for i in range(len(ver_keys)):
            ver_key_c_instances[i] = ver_keys[i].c_instance

        valid = c_bool()
        do_call(
            "indy_bls_verify_multi_sig",
            multi_sig.c_instance,
            c_char_p(message),
            c_int64(len(message)),
            ver_key_c_instances,
            c_int32(len(ver_keys)),
            gen.c_instance,
            byref(valid),
        )

        res = valid

        LOGGER.debug("Bls::verify_multi_sig: <<< res: %r", res)
        return res
