# -*- coding: utf-8 -*-
#
# This file is part of Flask-Collect.
# Copyright (C) 2014 CERN.
#
# Flask-Collect is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

"""
Symbolic link storage for development mode.

It creates symbolic links to the real files so any changes to them will be
reflected.
"""

import os
from .base import BaseStorage


class Storage(BaseStorage):

    """Storage that creates symlinks to the resources."""

    def run(self):
        """Collect static from blueprints.

        Create the directory tree but will symlink all the files.
        """
        self.log("Collect static from blueprints")
        skipped, total = 0, 0
        destination_list = set()
        for bp, f, o in self:
            destination = os.path.join(self.collect.static_root, o)
            destination_dir = os.path.dirname(destination)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            if destination in destination_list:
                self.log("{0} already linked".format(destination))
                skipped += 1
            elif not os.path.exists(destination):
                # the path is a link, but points to invalid location
                if os.path.islink(destination):
                    os.remove(destination)
                os.symlink(f, destination)
                self.log("{0}:{1} symbolink link created".format(bp.name, o))
                destination_list.add(destination)
            else:
                skipped += 1
            total += 1
        self.log("{0} of {1} files already present".format(skipped, total))
        self.log("Done collecting.")
