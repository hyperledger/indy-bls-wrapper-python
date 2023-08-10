# indy-bls-wrapper-python

A Python wrapper for [Hyperledger Indy BLS Signatures Rust] as used by [Hyperledger Indy Node].

This package implements a version of the BLS signature scheme. The implementation doesn't match up with the [BLS signatures specification at the IETF]. It uses the [BN254 curve defined here](https://neuromancer.sk/std/bn/bn254) (sometimes called BN254N), and should not to be confused with the one used in Ethereum.

This package is NOT recommended for new projects. It would be preferable to use a BLS signatures implementation based on the IETF draft, on a curve with a stronger security estimation (such as BLS12-381).

[BLS signatures specification at the IETF]: https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-bls-signature-05
[Hyperledger Indy BLS Signatures Rust]: https://github.com/hyperledger/indy-blssignatures-rs
[Hyperledger Indy Node]: https://github.com/hyperledger/indy-node

## Installation

The package may be installed by using:

```sh
pip install indy_bls
```

No additional dependencies are required for installation. Python 3.6 and higher are currently supported.

## Building

The primary build dependency is the Rust crate: [Hyperledger Indy BLS Signatures Rust], which requires a Rust compiler toolchain. Python packaging requires `setuptools` and `wheel`.

## Contributing

Pull requests are welcome! Please read our [contributions guide](https://github.com/hyperledger/indy-bls-wrapper-python/blob/main/CONTRIBUTING.md) and submit your PRs. We enforce [developer certificate of origin](https://developercertificate.org/) (DCO) commit signing. See guidance [here](https://github.com/apps/dco).

We also welcome issues submitted about problems you encounter in using `indy_bls`.

## Acknowledgements

This code is based on the original Ursa Python wrapper contributed by Cam Parra.

## License

Licensed under the Apache License, Version 2.0. ([LICENSE-APACHE](https://github.com/hyperledger/indy-bls-wrapper-python/blob/main/LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0).
