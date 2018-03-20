from conans import ConanFile
import platform

class ZXingTestConan(ConanFile):
    generators = 'qbs'

    def build(self):
        self.run('qbs -f "%s"' % self.source_folder)

    def imports(self):
        self.copy('*', src='bin', dst='bin')
        self.copy('*', dst='lib', src='lib')

    def test(self):
        self.run('qbs run')

        # Ensure we only link to system libraries and our own libraries.
        if platform.system() == 'Darwin':
            self.run('! (otool -L lib/*.dylib | grep -v "^lib/" | egrep -v "^\s*(/usr/lib/|/System/|@rpath/)")')
        elif platform.system() == 'Linux':
            self.run('! (ldd lib/*.so | grep -v "^lib/" | grep "/" | egrep -v "\s/lib64/")')
        else:
            raise Exception('Unknown platform "%s"' % platform.system())
