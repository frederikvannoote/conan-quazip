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
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = (
        "qt/5.12.6@bincrafters/stable",
        "zlib/1.2.11"
    )

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.configure(source_folder=".")
        cmake.build()
        cmake.install()

    def package_info(self):
        lib_name = "quazip_static" if tools.os_info.is_windows and not self.options.shared else "quazip5"
        lib_name += "d" if self.settings.build_type == "Debug" else ""
        self.cpp_info.libs = [lib_name]
        self.cpp_info.defines = ["QUAZIP_STATIC"] if not self.options.shared else []
