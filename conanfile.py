from conans import ConanFile, CMake, tools
import os


class QuazipConan(ConanFile):
    name = "quazip"
    description = "Qt/C++ wrapper over minizip"
    topics = ("conan", "quazip")
    url = "https://github.com/bincrafters/conan-quazip"
    homepage = "https://github.com/stachenov/quazip"
    license = " LGPL-2.1-only"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "qt/5.14.1@bincrafters/stable",
        "zlib/1.2.11"
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        if tools.os_info.is_windows:
            cmake.definitions["ZLIB_INCLUDE_DIRS"] = ";".join(self.deps_cpp_info["zlib"].include_paths)
            cmake.definitions["ZLIB_LIBRARIES"] = ";".join(self.deps_cpp_info["zlib"].lib_paths)
        else:
            cmake.definitions["ZLIB_ROOT"] = self.deps_cpp_info["zlib"].rootpath

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        if self.options.shared:
            cmake.build(target="quazip5")
        else:
            cmake.build(target="quazip_static")

    def package(self):
        self.copy(pattern="*.h", dst="include/quazip", src=os.path.join(self._source_subfolder, "quazip"))
        if self.options.shared:
            self.copy(pattern="*.so", dst="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            self.copy(pattern="*.dll", dst="bin", keep_path=False)
        else:
            self.copy(pattern="*.lib", dst="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="COPYING", dst='licenses', src=self._source_subfolder, ignore_case=True, keep_path=False)

    def package_info(self):
        lib_name = "quazip_static" if tools.os_info.is_windows and not self.options.shared else "quazip5"
        lib_name += "d" if self.settings.build_type == "Debug" else ""
        self.cpp_info.libs = [lib_name]
        self.cpp_info.defines = ["QUAZIP_STATIC"] if not self.options.shared else []
