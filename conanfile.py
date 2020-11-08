from conans import ConanFile, CMake, tools
import os
import platform

class ZXingConan(ConanFile):
    name = 'zxing'

    # zxing-cpp has no tagged releases, so just use package_version.
    # https://github.com/glassechidna/zxing-cpp/issues/29#issuecomment-134047119
    source_version = '0'
    package_version = '4'
    version = '%s-%s' % (source_version, package_version)

    build_requires = (
        'llvm/5.0.2-1@vuo/stable',
        'macos-sdk/11.0-0@vuo/stable',
    )
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/glassechidna/zxing-cpp'
    license = 'https://github.com/glassechidna/zxing-cpp/blob/master/COPYING'
    description = 'A library for scanning barcodes'
    source_dir = 'zxing-cpp'
    generators = 'cmake'

    build_dir = '_build'
    install_dir = '_install'

    def source(self):
        self.run("git clone https://github.com/glassechidna/zxing-cpp.git")
        with tools.chdir(self.source_dir):
            self.run("git checkout 5aad474")

        tools.download('https://github.com/glassechidna/zxing-cpp/pull/62.patch', '62.patch')
        tools.patch(patch_file='62.patch', base_path=self.source_dir)

        self.run('mv %s/COPYING %s/%s.txt' % (self.source_dir, self.source_dir, self.name))

    def build(self):
        cmake = CMake(self)
        cmake.definitions['CONAN_DISABLE_CHECK_COMPILER'] = True
        cmake.definitions['CMAKE_BUILD_TYPE'] = 'Release'
        cmake.definitions['CMAKE_CXX_COMPILER'] = self.deps_cpp_info['llvm'].rootpath + '/bin/clang++'
        cmake.definitions['CMAKE_C_COMPILER']   = self.deps_cpp_info['llvm'].rootpath + '/bin/clang'
        cmake.definitions['CMAKE_C_FLAGS'] = cmake.definitions['CMAKE_CXX_FLAGS'] = '-Oz -DNDEBUG'
        cmake.definitions['CMAKE_CXX_FLAGS'] += ' -stdlib=libc++ -I' + ' -I'.join(self.deps_cpp_info['llvm'].include_paths)
        cmake.definitions['CMAKE_INSTALL_PREFIX'] = '%s/%s' % (os.getcwd(), self.install_dir)
        cmake.definitions['CMAKE_OSX_ARCHITECTURES'] = 'x86_64;arm64'
        cmake.definitions['CMAKE_OSX_DEPLOYMENT_TARGET'] = '10.11'
        cmake.definitions['OpenCV_FOUND'] = ''
        cmake.definitions['ICONV_LIBRARY'] = ''

        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            cmake.configure(source_dir='../%s' % self.source_dir,
                            build_dir='.',
                            args=['-Wno-dev', '--no-warn-unused-cli'])
            cmake.build(target='libzxing')
            cmake.install()

    def package(self):
        if platform.system() == 'Darwin':
            libext = 'dylib'
        elif platform.system() == 'Linux':
            libext = 'so'
        else:
            raise Exception('Unknown platform "%s"' % platform.system())

        self.copy('*.h', src='%s/include' % self.install_dir, dst='include')
        self.copy('libzxing.%s' % libext, src='%s/lib' % self.install_dir, dst='lib')

        self.copy('%s.txt' % self.name, src=self.source_dir, dst='license')

    def package_info(self):
        self.cpp_info.libs = ['zxing']
        self.cpp_info.includedirs = ['include', 'include/zxing']
