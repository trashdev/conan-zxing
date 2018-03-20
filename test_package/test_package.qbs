import qbs 1.0

Project {
	minimumQbsVersion: '1.6'
	references: [ buildDirectory + '/../conanbuildinfo.qbs' ]
	Product {
		type: 'application'
		consoleApplication: true

		Depends { name: 'ConanBasicSetup' }

		Depends { name: 'cpp' }
		property string binDirectory: {
			return buildDirectory.substr(0, buildDirectory.lastIndexOf('/', buildDirectory.lastIndexOf('/') - 1)) + "/bin";
		}
		cpp.cxxStandardLibrary: 'libstdc++'
		cpp.rpaths: [ buildDirectory + '/../../lib' ]

		Depends {
			condition: qbs.targetOS.contains('macos')
			name: 'xcode'
		}
		Properties {
			condition: qbs.targetOS.contains('macos')
			cpp.compilerPathByLanguage: ({
				c: binDirectory + '/clang',
				cpp: binDirectory + '/clang++',
			})
			cpp.linkerPath: binDirectory + '/clang++'
			cpp.linkerWrapper: undefined
			cpp.minimumMacosVersion: '10.10'
			cpp.target: 'x86_64-apple-macosx10.10'
			cpp.stripPath: '/usr/bin/true'
			xcode.sdk: 'macosx10.11'
		}
		Properties {
			condition: qbs.targetOS.contains('linux')
			cpp.compilerPathByLanguage: ({
				c: '/opt/llvm-3.8.0/bin/clang',
				cpp: '/opt/llvm-3.8.0/bin/clang++',
			})
			cpp.cxxFlags: [ '-fblocks' ]
			cpp.linkerPath: '/opt/llvm-3.8.0/bin/clang++'
			cpp.target: 'x86_64-unknown-linux-gnu'
		}

		files: [ 'test_package.cc' ]
	}
}
