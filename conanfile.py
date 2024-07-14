from conan import ConanFile
from conan.tools.cmake import CMakeToolchain
from conan.tools.files import rmdir, rename
import os


required_conan_version = ">=2.0"


class LibJpegTurboConan(ConanFile):
    name = "libjpeg-turbo"
    version = "3.0.1"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaCmakeBase"
    ignore_cpp_standard = True

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["ENABLE_SHARED"] = self.options.shared
        tc.variables["ENABLE_STATIC"] = not self.options.shared
        tc.variables["WITH_JPEG8"] = True
        tc.generate()

    def package(self):
        super().package()

        rmdir(self, os.path.join(self.package_folder, "bin"))
        rmdir(self, os.path.join(self.package_folder, "share"))

        if self.settings.os != "Windows":
            rename(self, os.path.join(self.package_folder, "lib64"), os.path.join(self.package_folder, "lib"))

        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_module_file_name", "JPEG")

        self.cpp_info.components["turbojpeg"].libs = ["turbojpeg"]
        self.cpp_info.components["turbojpeg"].set_property("cmake_file_name", "libjpeg-turbo")
        self.cpp_info.components["turbojpeg"].set_property("cmake_target_name", "libjpeg-turbo::turbojpeg-static")

        self.cpp_info.components["jpeg8"].libs = ["jpeg"]
        self.cpp_info.components["jpeg8"].set_property("cmake_file_name", "JPEG")
        self.cpp_info.components["jpeg8"].set_property("cmake_target_name", "JPEG::JPEG")
