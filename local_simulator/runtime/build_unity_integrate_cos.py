"""Build the bundled x64 integration cosine DLL without fused operations."""
import argparse
from pathlib import Path
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cc', default='gcc')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    subprocess.run([args.cc, '-std=c11', '-O2', '-shared', '-static-libgcc',
        '-msse2', '-mno-avx', '-mno-fma', '-ffp-contract=off', '-fno-fast-math',
        '-fno-associative-math', '-frounding-math', '-Wl,--no-insert-timestamp',
        str(root/'unity_integrate_cos.c'), '-o', str(root/'unity_integrate_cos.dll')], check=True)

if __name__ == '__main__':
    main()
