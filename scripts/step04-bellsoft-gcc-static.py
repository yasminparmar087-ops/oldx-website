#!/usr/bin/env python3
"""One-shot OLDX BellSoft GCC-95619 evidence collection. Local D: only, NO code execution of image binaries.

No Docker, cloud, image deployment, or vulnerability scan. The presence/absence of
symbols or relocation calls alone CANNOT establish CVE-2026-95619 NOT_AFFECTED.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile

INDEX = 'ef00ba8e634402e8dd3b374643fdbc178e876c7a312c9d55e4734efaa1e93d94'
CHILD = '3862d478c2737d8386911b777d713e56a26e182f7c107e702be23a7b1cfe4799'
LAYER = '9a8ef1a013e7d69968347b5d280a27c153444b9c878488a27ff1a76079aa6d8c'
LAYER_SIZE = 38_437_417
ROOT = Path('/mnt/d/OLDX/G2')
OUTPUT = ROOT / 'bellsoft-cve-95619-static-20261120-a1'
ORAS = ROOT / 'oras-v1.3.6-pinned-a1/oras'
TARGET = f'docker.io/bellsoft/hardened-nodejs@sha256:{LAYER}'
MATCH = re.compile(r'(^|/)libstdc\+\+\.so\.6(?:\.\d+)*$')


def stop(why):
    print('STOP_' + why, flush=True)
    sys.exit(2)


def run_readonly(cmd, timeout=40):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        stop('STATIC_TOOL_UNAVAILABLE_OR_TIMEOUT')
    if p.returncode:
        stop('STATIC_TOOL_FAILED')
    return p.stdout


def main():
    if not ROOT.is_dir() or ROOT.is_symlink() or not ORAS.is_file():
        stop('LOCAL_PATH')
    if OUTPUT.exists() or OUTPUT.is_symlink():
        stop('OUTPUT_ALREADY_EXISTS_DO_NOT_OVERWRITE')
    if shutil.disk_usage(ROOT).free < 256 * 1024 * 1024:
        stop('D_DRIVE_SPACE_BELOW_256_MIB')
    readelf = shutil.which('readelf')
    objdump = shutil.which('objdump')
    if not readelf or not objdump:
        stop('BINUTILS_MISSING_NO_DOWNLOAD')

    print('SCOPE=LOCAL_D_DRIVE_ONE_NEW_PUBLIC_LAYER', flush=True)
    print('IMAGE_INDEX=sha256:' + INDEX, flush=True)
    print('IMAGE_AMD64_CHILD=sha256:' + CHILD, flush=True)
    print('EXPECTED_LAYER=sha256:' + LAYER, flush=True)
    # Never delete or overwrite existing evidence; create a new exclusive output.
    OUTPUT.mkdir(mode=0o700, exist_ok=False)
    try:
        p = subprocess.run([str(ORAS), 'blob', 'fetch', '--output', '-', TARGET],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=240, check=False)
    except (OSError, subprocess.TimeoutExpired):
        stop('ORAS_FETCH_UNKNOWN_NO_RETRY')
    if p.returncode:
        stop('ORAS_FETCH_FAILED_NO_RETRY')
    data = p.stdout
    if len(data) != LAYER_SIZE or hashlib.sha256(data).hexdigest() != LAYER:
        stop('LAYER_SIZE_OR_DIGEST_MISMATCH')
    print('LAYER_SHA256=PASS', flush=True)
    layer_file = OUTPUT / 'verified-layer.tar.gz'
    with layer_file.open('xb') as fh:
        fh.write(data)
    os.chmod(layer_file, 0o600)

    selected = []
    candidate_names = []
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode='r|gz') as tf:
            count = 0
            total_declared = 0
            for member in tf:
                count += 1
                total_declared += max(0, member.size)
                if count > 60000 or total_declared > 1_000_000_000:
                    stop('ARCHIVE_TOO_LARGE')
                if 'libstdc++.so' in member.name:
                    candidate_names.append(member.name[:240])
                if not member.isfile() or not MATCH.search(member.name):
                    continue
                if member.size > 32 * 1024 * 1024 or member.size < 100000:
                    stop('ELF_SIZE_UNEXPECTED')
                if len(selected) >= 3:
                    stop('TOO_MANY_ELF_CANDIDATES')
                handle = tf.extractfile(member)
                if handle is None:
                    stop('TAR_ELF_NOT_READABLE')
                blob = handle.read(32 * 1024 * 1024 + 1)
                if len(blob) != member.size or not blob.startswith(b'\x7fELF'):
                    stop('ELF_BYTES_INVALID')
                out = OUTPUT / f'libstdcxx-{len(selected)+1}.elf'
                with out.open('xb') as f:
                    f.write(blob)
                os.chmod(out, 0o600)
                selected.append((out, member.name, hashlib.sha256(blob).hexdigest()))
    except (tarfile.TarError, EOFError, OSError, ValueError):
        stop('TAR_FORMAT_OR_IO')
    if not selected:
        print('LIBSTDCXX_CANDIDATE_PATHS=' + json.dumps(candidate_names[:12]))
        stop('LIBSTDCXX_BINARY_NOT_FOUND_IN_LAYER')

    reports = []
    for file, original_name, elf_hash in selected:
        hdr = run_readonly([readelf, '-h', str(file)])
        if 'ELF64' not in hdr or 'Advanced Micro Devices X86-64' not in hdr:
            stop('WRONG_ELF_ARCHITECTURE')
        symbols = run_readonly([readelf, '-Ws', str(file)])
        imports = {symbol: any(symbol in line and 'UND' in line
                               for line in symbols.splitlines())
                   for symbol in ('posix_memalign', 'aligned_alloc')}
        operator_symbols = [line.strip()[:260] for line in symbols.splitlines()
                            if ('_ZnwmSt11align_val_t' in line or '_ZnamSt11align_val_t' in line)]
        # Symbol-versioned functions are often NOT found by objdump
        # --disassemble=<mangled-name>. Resolve their exact .dynsym address
        # and size, then disassemble only that bounded function address range.
        disassemblies = {}
        for fn in ('_ZnwmSt11align_val_t', '_ZnamSt11align_val_t'):
            funcs = []
            for line in symbols.splitlines():
                fields = line.split()
                if (len(fields) >= 8 and fields[0].endswith(':')
                    and fields[3] == 'FUNC' and fields[7].startswith(fn + '@')):
                    try:
                        addr = int(fields[1], 16)
                        size = int(fields[2])
                    except ValueError:
                        continue
                    if addr and 0 < size <= 65536:
                        funcs.append((addr, size))
            if funcs:
                addr, size = funcs[0]
                s = run_readonly([objdump, '-drwC',
                                  '--start-address=' + hex(addr),
                                  '--stop-address=' + hex(addr + size), str(file)])
                disassemblies[fn] = s[:250000]
            else:
                disassemblies[fn] = 'FUNCTION_SYMBOL_UNAVAILABLE_FOR_STATIC_DISASSEMBLY'
        calls = [line.strip() for s in disassemblies.values()
                 for line in s.splitlines()
                 if '\tcall' in line or '\tjmp' in line]
        reports.append({
            'tar_member': original_name, 'saved_file': file.name,
            'elf_sha256': elf_hash, 'elf_amd64': True,
            'undefined_dynamic_symbols': imports,
            'aligned_operator_symbols': operator_symbols[:16],
            'aligned_new_call_or_jump_lines': calls[:35],
            'full_aligned_new_disassembly': disassemblies,
            'decision': 'EVIDENCE_ONLY_CVE_2026_95619_NOT_CLEARED',
        })
        print('LIBSTDCXX_ELF=' + original_name, flush=True)
        print('LIBSTDCXX_SHA256=sha256:' + elf_hash, flush=True)
        print('ELF_X86_64=PASS', flush=True)
        print('POSIX_MEMALIGN_IMPORT=' + str(imports['posix_memalign']), flush=True)
        print('ALIGNED_ALLOC_IMPORT=' + str(imports['aligned_alloc']), flush=True)
        print('ALIGNED_OPERATOR_SYMBOL_COUNT=' + str(len(operator_symbols)), flush=True)
        print('ALIGNED_OPERATOR_CALLS=' + json.dumps(calls[:12]), flush=True)

    record = {
        'index_sha256': INDEX, 'amd64_child_sha256': CHILD,
        'verified_layer_sha256': LAYER, 'layer_compressed_bytes': LAYER_SIZE,
        'selected_elfs': reports,
        'scope': 'ONE LOCAL STATIC COLLECTION_ONLY_NO_RUNTIME_EXECUTION',
        'overall_decision': 'GCC_CVE_2026_95619_REQUIRES_BINARY_EXPERT_OR_VENDOR_VEX',
    }
    with (OUTPUT / 'review.json').open('x', encoding='utf-8') as fh:
        json.dump(record, fh, indent=2)
    print('STATIC_EVIDENCE_SAVED=' + str(OUTPUT / 'review.json'), flush=True)
    print('GCC_95619_STATUS=UNVERIFIED_DO_NOT_CLAIM_NOT_AFFECTED', flush=True)
    print('LOCAL_STATIC_REVIEW=COMPLETE', flush=True)


if __name__ == '__main__':
    main()
