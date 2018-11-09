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
    #requires = ("a52dec/0.7.4@user/channel","bzip2/1.0.6@user/channel","expat/2.2.5@user/channel",
    #            "gtk-doc-lite/1.27@user/channel","libdvdread/5.0.0@user/channel","libffi/3.99999@user/channel",
    #            "libjpeg-turbo/1.5.3@user/channel","libmpeg2/0.5.1@user/channel","libogg/1.3.3@user/channel",
    #            "libvisual/0.4.0@user/channel","opencore-amr/0.1.5@user/channel","opus/1.2.1@user/channel",
    #            "orc/0.4.28@bincrafters/stable","pixman/0.34.0@user/channel","x264/20161218-2245@user/channel",
    #            "zlib/1.2.11@user/channel","glib/2.54.3@bincrafters/stable","libpng/1.6.34@user/channel",
    #            "libvorbis/1.3.5@user/channel","libxml2/2.9.7@user/channel","freetype/2.9@user/channel",
    #            "gobject-introspection/1.54.1@bincrafters/stable","libtheora/1.1.1@user/channel","fontconfig/2.12.6@user/channel",
    #            "graphene/1.4.0@bincrafters/stable","gstreamer/1.14.3@bincrafters/stable","cairo/1.14.12@bincrafters/stable",
    #            "harfbuzz/1.7.5@bincrafters/stable","pango/1.40.14@bincrafters/stable","gst-plugins-base/1.14.3@bincrafters/stable",)
    requires = ("gstreamer-1.0/1.14.4@conanos/dev","gst-plugins-base-1.0/1.14.4@conanos/dev","a52dec/0.7.4@conanos/dev",
                "opencore-amr/0.1.5@conanos/dev","libdvdread/5.0.0@conanos/dev","libmpeg2/0.5.1@conanos/dev","x264/20181108-2245@conanos/dev",
                "orc/0.4.28@conanos/dev")

    source_subfolder = "source_subfolder"

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = "gst-plugins-ugly-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        #vars = {'C_INCLUDE_PATH': '%s/include'%(self.deps_cpp_info["opencore-amr"].rootpath),
        #        'LD_LIBRARY_PATH':'%s/lib:%s/lib'%(self.deps_cpp_info["libffi"].rootpath,self.deps_cpp_info["glib"].rootpath)
        #       }
        #with tools.environment_append(vars):

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

