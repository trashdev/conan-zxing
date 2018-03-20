from conans import ConanFile, CMake, tools

class ZXingConan(ConanFile):
    name = 'zxing'

    # zxing-cpp has no tagged releases, so just use package_version.
    # https://github.com/glassechidna/zxing-cpp/issues/29#issuecomment-134047119
    source_version = '0'
    package_version = '1'
    version = '%s-%s' % (source_version, package_version)

    requires = 'llvm/3.3-1@vuo/stable'
    settings = 'os', 'compiler', 'build_type', 'arch'
    url = 'https://github.com/glassechidna/zxing-cpp'
    license = 'https://github.com/glassechidna/zxing-cpp/blob/master/COPYING'
    description = 'A library for scanning barcodes'
    source_dir = 'zxing-cpp'
    build_dir = '_build'
    generators = 'cmake'

    def source(self):
        self.run("git clone https://github.com/glassechidna/zxing-cpp.git")
        with tools.chdir(self.source_dir):
            self.run("git checkout 5aad474")

        tools.download('https://github.com/glassechidna/zxing-cpp/pull/62.patch', '62.patch')
        tools.patch(patch_file='62.patch', base_path=self.source_dir)

    def build(self):
        tools.mkdir(self.build_dir)
        with tools.chdir(self.build_dir):
            cmake = CMake(self)

            cmake.definitions['CMAKE_BUILD_TYPE'] = 'Release'
            cmake.definitions['CMAKE_CXX_COMPILER'] = self.deps_cpp_info['llvm'].rootpath + '/bin/clang++'
            cmake.definitions['CMAKE_C_COMPILER']   = self.deps_cpp_info['llvm'].rootpath + '/bin/clang'
            cmake.definitions['CMAKE_C_FLAGS'] = cmake.definitions['CMAKE_CXX_FLAGS'] = '-Oz -DNDEBUG'
            cmake.definitions['CMAKE_CXX_FLAGS'] += ' -stdlib=libstdc++'
            cmake.definitions['CMAKE_OSX_ARCHITECTURES'] = 'x86_64'
            cmake.definitions['CMAKE_OSX_DEPLOYMENT_TARGET'] = '10.10'
            cmake.definitions['OpenCV_FOUND'] = ''
            cmake.definitions['ICONV_LIBRARY'] = ''

            cmake.configure(source_dir='../%s' % self.source_dir,
                            build_dir='.')
            cmake.build(target='libzxing')

    def package(self):
        self.copy('*.h', src='%s/core/src/zxing' % self.source_dir, dst='include/zxing')
        self.copy('*.h', src=self.build_dir, dst='include/zxing')
        self.copy('libzxing.dylib', src='%s' % self.build_dir, dst='lib')

    def package_info(self):
        self.cpp_info.libs = ['zxing']
        self.cpp_info.includedirs = ['include', 'include/zxing']
