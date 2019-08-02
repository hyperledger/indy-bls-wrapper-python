FROM ubuntu:18.04


RUN apt-get update -y && apt-get install -y \
	wget \
	python3.5 \
	python3-pip \
	python-setuptools \
	python3-nacl \
	apt-transport-https \
	ca-certificates \
	supervisor \
	curl \
	sudo \
	nano \
	git \
	cmake \
	autoconf \
	libtool \
      	pkg-config \
      	libssl-dev

ENV RUST_VERSION=${RUST_VERSION:-1.36.0}

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --no-modify-path --default-toolchain $RUST_VERSION \
    && chmod -R a+w $RUSTUP_HOME $CARGO_HOME \
    && rustup --version \
    && cargo --version \
    && rustc --version

WORKDIR /home/

RUN curl -fsSL https://github.com/jedisct1/libsodium/releases/download/1.0.14/libsodium-1.0.14.tar.gz | tar -xz

WORKDIR libsodium-1.0.14

RUN ./autogen.sh && ./configure && make && sudo make install

ENV SODIUM_LIB_DIR=/usr/local/lib \
    LD_LIBRARY_PATH=/usr/local/lib

WORKDIR /home/

RUN git clone https://github.com/hyperledger/ursa.git 

WORKDIR /home/ursa/

RUN  cargo build --release 

RUN cp /home/ursa/target/release/libursa.so /usr/lib/.

RUN pip3 install -U  pytest
