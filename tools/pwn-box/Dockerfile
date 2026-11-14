# Linux pwn/RE box for an Apple Silicon Mac.
# gdb can't debug natively on macOS arm64, and gdb under x86 emulation is unreliable.
# This is a native arm64 container: x86-64 binaries run under qemu-user, and
# gdb-multiarch / pwndbg attach to qemu's gdb stub.
#
# Build:  docker build -t ctf-pwn-box tools/pwn-box
# Run:    docker run --rm -it -v "$PWD":/work ctf-pwn-box
# Debug an x86-64 binary:
#   qemu-x86_64 -L /usr/x86_64-linux-gnu -g 1234 ./chall &
#   gdb-multiarch -q ./chall -ex 'target remote :1234'
FROM ubuntu:24.04

ARG PWNDBG_VERSION=2026.10.28
ENV DEBIAN_FRONTEND=noninteractive TERM=xterm-256color

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl file binutils binutils-x86-64-linux-gnu \
        gdb-multiarch qemu-user libc6-amd64-cross \
        python3 python3-venv python3-dev build-essential \
        checksec steghide netcat-openbsd patchelf less vim-tiny \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /tmp/pwndbg.deb \
        "https://github.com/pwndbg/pwndbg/releases/download/${PWNDBG_VERSION}/pwndbg_${PWNDBG_VERSION}_arm64.deb" \
    && apt-get update && apt-get install -y /tmp/pwndbg.deb \
    && rm -rf /tmp/pwndbg.deb /var/lib/apt/lists/*

RUN python3 -m venv /opt/pwn && /opt/pwn/bin/pip install --no-cache-dir pwntools
ENV PATH="/opt/pwn/bin:${PATH}"

WORKDIR /work
CMD ["bash"]
