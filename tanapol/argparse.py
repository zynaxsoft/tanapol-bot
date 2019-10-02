import argparse


p = argparse.ArgumentParser()
p.add_argument('--secrets-file', '-f',
               help='location of the secrets file')
args = p.parse_args()
