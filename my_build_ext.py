# this code has been taken from gevent's setup.py file. it provides a
# build_ext command that puts .so/.pyd files in-place (like "setup.py
# build_ext -i"). it uses symlinks if possible and will rebuild when
# changing the python version (unlike "setup.py build_ext -i")

import sys, os, glob, shutil

from distutils.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    def build_extension(self, ext):
        result = _build_ext.build_extension(self, ext)
        if self.inplace:
            return result
        modpath = self.get_ext_fullname(ext.name).split('.')
        filename = self.get_ext_filename(ext.name)
        filename = os.path.split(filename)[-1]
        filename = os.path.join(*modpath[:-1] + [filename])
        build_path = os.path.abspath(os.path.join(self.build_lib, filename))
        src_path = os.path.abspath(os.path.basename(build_path))
        if build_path != src_path:
            try:
                os.unlink(src_path)
            except OSError:
                pass

            if self.verbose:
                sys.stderr.write('Linking %s to %s\n' % (build_path, src_path))

            if hasattr(os, 'symlink'):
                os.symlink(build_path, src_path)
            else:
                shutil.copyfile(build_path, src_path)

        return result