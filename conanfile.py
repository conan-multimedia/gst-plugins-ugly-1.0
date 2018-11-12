from conans import ConanFile, CMake, tools, Meson
import os

class GstpluginsuglyConan(ConanFile):
    name = "gst-plugins-ugly-1.0"
    version = "1.14.4"
    description = "'Ugly' GStreamer plugins and helper libraries"
    url = "https://github.com/conan-multimedia/gst-plugins-ugly-1.0"
    homepage = "https://github.com/GStreamer/gst-plugins-ugly"
    license = "GPLv2+"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    requires = ("gstreamer-1.0/1.14.4@conanos/dev","gst-plugins-base-1.0/1.14.4@conanos/dev","a52dec/0.7.4@conanos/dev",
                "opencore-amr/0.1.5@conanos/dev","libdvdread/5.0.0@conanos/dev","libmpeg2/0.5.1@conanos/dev","x264/20181108-2245@conanos/dev",
                "orc/0.4.28@conanos/dev")

    source_subfolder = "source_subfolder"
    remotes = {'origin': 'https://github.com/GStreamer/gst-plugins-ugly.git'}

    def source(self):
        #tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        #extracted_dir = "gst-plugins-ugly-" + self.version
        #os.rename(extracted_dir, self.source_subfolder)
        tools.mkdir(self.source_subfolder)
        with tools.chdir(self.source_subfolder):
            self.run('git init')
            for key, val in self.remotes.items():
                self.run("git remote add %s %s"%(key, val))
            self.run('git fetch --all')
            self.run('git reset --hard %s'%(self.version))
            self.run('git submodule update --init --recursive')

    def build(self):
        with tools.chdir(self.source_subfolder):
            with tools.environment_append({
                'LIBRARY_PATH' : '%s/lib'%(self.deps_cpp_info["a52dec"].rootpath),
                'C_INCLUDE_PATH' : '%s/include'%(self.deps_cpp_info["a52dec"].rootpath),
                }):
                meson = Meson(self)
                meson.configure(
                    defs={'prefix':'%s/builddir/install'%(os.getcwd()), 'libdir':'lib',},
                    source_dir = '%s'%(os.getcwd()),
                    build_dir= '%s/builddir'%(os.getcwd()),
                    pkg_config_paths=['%s/lib/pkgconfig'%(self.deps_cpp_info["gstreamer-1.0"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["gst-plugins-base-1.0"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["a52dec"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["opencore-amr"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libdvdread"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["libmpeg2"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["x264"].rootpath),
                                      '%s/lib/pkgconfig'%(self.deps_cpp_info["orc"].rootpath),
                                      ]
                                )
                meson.build(args=['-j4'])
                self.run('ninja -C {0} install'.format(meson.build_dir))


    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir/install"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

