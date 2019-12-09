# -*- coding: utf-8 -*-
"""
Generate linter documentation page
"""

import argparse
import io
import logging
import os
import sys

import cmake_format
from cmake_format.doc.gendoc_sources import format_directive
from cmake_lint import lintdb

HEADER = """
===================
Lint Code Reference
===================

"""


def setup_argparse(argparser):
  argparser.add_argument('-v', '--version', action='version',
                         version=cmake_format.VERSION)
  argparser.add_argument(
      '-l', '--log-level', default="info",
      choices=["error", "warning", "info", "debug"])

  argparser.add_argument(
      '-o', '--outfile-path', default=None,
      help='Write output to this file. Default is stdout.')

  argparser.add_argument(
      '-c', '--config-files', nargs='+',
      help='path to configuration file(s)')
  argparser.add_argument('infilepaths', nargs='*')


def write_title(outfile, title, rulerchar=None, numrule=1):
  if rulerchar is None:
    rulerchar = '-'

  if numrule == 2:
    outfile.write(rulerchar * len(title))
    outfile.write("\n")
  outfile.write(title)
  outfile.write("\n")
  outfile.write(rulerchar * len(title))
  outfile.write("\n\n")


def gendocs(outfile):
  outfile.write(HEADER)
  for idstr, msgfmt, kwargs in lintdb.LINT_DB:
    write_title(outfile, idstr, numrule=2)
    write_title(outfile, "message")
    outfile.write(format_directive(msgfmt))
    outfile.write("\n\n")
    description = kwargs.pop("description", None)
    if description:
      write_title(outfile, "description")
      outfile.write(description)
      outfile.write("\n\n")

    explain = kwargs.pop("explain", None)
    if explain:
      write_title(outfile, "explanation")
      outfile.write(explain)
      outfile.write("\n\n")
    outfile.write("\n\n")


def main():
  """Parse arguments, open files, start work."""

  argparser = argparse.ArgumentParser(
      description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)

  setup_argparse(argparser)
  args = argparser.parse_args()
  logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))

  if args.outfile_path is None:
    args.outfile_path = '-'

  if args.outfile_path == '-':
    outfile = io.open(os.dup(sys.stdout.fileno()),
                      mode='w', encoding="utf-8", newline='')
  else:
    outfile = io.open(args.outfile_path, 'w', encoding="utf-8", newline='')

  gendocs(outfile)
  outfile.close()
  return 0


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
  sys.exit(main())