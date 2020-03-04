%define keepstatic 1
%define gcc_target %{_arch}-generic-linux
%define libstdcxx_maj 6
%define libstdcxx_full 6.0.21
%define isl_version 0.16.1

%define debug_package %{nil}


# Highest optimisation ABI we target
%define mtune haswell

Name     : libgfortran-avx
Version  : 9.2.0
Release  : 49
URL      : http://www.gnu.org/software/gcc/
Source0  : https://gcc.gnu.org/pub/gcc/releases/gcc-9.2.0/gcc-9.2.0.tar.xz
Source1  : https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.16.1.tar.bz2
Summary  : AVX optinuzed libgfortran
Group    : Development/Tools
License  : BSD-3-Clause BSL-1.0 GFDL-1.2 GFDL-1.3 GPL-2.0 GPL-3.0 LGPL-2.1 LGPL-3.0 MIT
Patch0   : 0001-Fix-stack-protection-issues.patch
Patch1   : gcc-stable-branch.patch
Patch2   : openmp-vectorize.patch
Patch3   : gomp-relax.patch
Patch4   : fixup-9-branch.patch

BuildRequires : bison
BuildRequires : flex
BuildRequires : gmp-dev
BuildRequires : libstdc++
BuildRequires : libunwind-dev
BuildRequires : mpc-dev
BuildRequires : mpfr-dev
BuildRequires : pkgconfig(zlib)
BuildRequires : sed
BuildRequires : texinfo
BuildRequires : dejagnu
BuildRequires : expect
BuildRequires : autogen
BuildRequires : guile
BuildRequires : tcl
BuildRequires : valgrind-dev
BuildRequires : libxml2-dev
BuildRequires : libxslt
BuildRequires : graphviz
BuildRequires : gdb-dev

Requires: glibc-lib-avx2
Requires: gcc-libs-math
Requires: libstdc++

Provides:       gcc-symlinks
Provides:       cpp
Provides:       cpp-symlinks
Provides:       gcov
Provides:       gfortran-symlinks
Provides:       g77
Provides:       g77-symlinks
Provides:       g++-symlinks
Provides:       g++
Provides:       gfortran

%description
GNU cc and gcc C compilers.


%prep
%setup -q -n gcc-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1


%build

# Live in the gcc source tree
tar xf %{SOURCE1} && ln -sf isl-%{isl_version} isl

rm -rf ../gcc-build
mkdir ../gcc-build
pushd ../gcc-build
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=ivybridge -g -O3 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000"
export CXXFLAGS="-march=ivybridge -g -O3  -Wl,-z,max-page-size=0x1000"
export CFLAGS_FOR_TARGET="$CFLAGS -march=haswell -mtune=skylake -fno-semantic-interposition "
export CXXFLAGS_FOR_TARGET="$CXXFLAGS -march=haswell -mtune=skylake -fno-semantic-interposition "
export FFLAGS_FOR_TARGET="$FFLAGS -march=haswell -mtune=skylake -fno-semantic-interposition "

export CPATH=/usr/include
export LIBRARY_PATH=%{_libdir}

../gcc-%{version}/configure \
    --prefix=%{_prefix} \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=/usr/lib64 \
    --enable-libstdcxx-pch\
    --libexecdir=/usr/lib64 \
    --with-system-zlib\
    --enable-shared\
    --enable-gnu-indirect-function \
    --disable-vtable-verify \
    --enable-threads=posix\
    --enable-__cxa_atexit\
    --enable-plugin\
    --enable-ld=default\
    --enable-clocale=gnu\
    --disable-multiarch\
    --disable-multilib\
    --enable-lto\
    --enable-linker-build-id \
    --build=%{gcc_target}\
    --target=%{gcc_target}\
    --enable-languages="c,c++,fortran" \
    --with-ppl=yes \
    --with-isl \
    --includedir=%{_includedir} \
    --with-gxx-include-dir=%{_includedir}/c++/ \
    --exec-prefix=%{_prefix} \
    --with-glibc-version=2.19 \
    --with-system-libunwind \
    --with-gnu-ld \
    --with-tune=haswell \
    --with-arch=haswell \
    --disable-bootstrap \
    --enable-cet \
    --disable-libmpx \
    --with-gcc-major-version-only \
    --enable-default-pie

make %{?_smp_mflags}

popd


rm -rf ../gcc-build-avx512
mkdir ../gcc-build-avx512
pushd ../gcc-build-avx512
unset CFLAGS
unset CXXFLAGS
export CFLAGS="-march=ivybridge -g -O3 -fstack-protector -Wl,-z -Wl,now -Wl,-z -Wl,relro  -Wl,-z,max-page-size=0x1000"
export CXXFLAGS="-march=ivybridge -g -O3  -Wl,-z,max-page-size=0x1000"
export CFLAGS_FOR_TARGET="$CFLAGS -march=skylake-avx512 -mtune=skylake -fno-semantic-interposition "
export CXXFLAGS_FOR_TARGET="$CXXFLAGS -march=skylake-avx512 -mtune=skylake -fno-semantic-interposition "
export FFLAGS_FOR_TARGET="$FFLAGS -march=skylake-avx512 -mtune=skylake -fno-semantic-interposition "

export CPATH=/usr/include
export LIBRARY_PATH=%{_libdir}

../gcc-%{version}/configure \
    --prefix=%{_prefix} \
    --with-pkgversion='Clear Linux OS for Intel Architecture'\
    --libdir=/usr/lib64 \
    --enable-libstdcxx-pch\
    --libexecdir=/usr/lib64 \
    --with-system-zlib\
    --enable-shared\
    --enable-gnu-indirect-function \
    --disable-vtable-verify \
    --enable-threads=posix\
    --enable-__cxa_atexit\
    --enable-plugin\
    --enable-ld=default\
    --enable-clocale=gnu\
    --disable-multiarch\
    --disable-multilib\
    --enable-lto\
    --enable-linker-build-id \
    --build=%{gcc_target}\
    --target=%{gcc_target}\
    --enable-languages="c,c++,fortran" \
    --with-ppl=yes \
    --with-isl \
    --includedir=%{_includedir} \
    --with-gxx-include-dir=%{_includedir}/c++/ \
    --exec-prefix=%{_prefix} \
    --with-glibc-version=2.19 \
    --with-system-libunwind \
    --with-gnu-ld \
    --with-tune=skylake-avx512 \
    --with-arch=skylake-avx512 \
    --disable-bootstrap \
    --enable-cet \
    --disable-libmpx \
    --with-gcc-major-version-only \
    --enable-default-pie

make %{?_smp_mflags}

popd

%install
export CPATH=%{_includedir}
export LIBRARY_PATH=%{_libdir}

pushd ../gcc-build-avx512
%make_install
popd
rm -rf %{buildroot}/usr/share
rm -rf %{buildroot}/usr/bin
rm -rf %{buildroot}/usr/lib64/gcc/
rm -rf %{buildroot}/usr/lib64/*.a
rm -rf %{buildroot}/usr/lib64/*.so
rm -rf %{buildroot}/usr/lib64/*.spec
mkdir -p %{buildroot}/usr/lib64/haswell/avx512_1
mv %{buildroot}/usr/lib64/*so*  %{buildroot}/usr/lib64/haswell/avx512_1


pushd ../gcc-build
%make_install
popd
rm -rf %{buildroot}/usr/share
rm -rf %{buildroot}/usr/bin
rm -rf %{buildroot}/usr/lib64/gcc/
rm -rf %{buildroot}/usr/lib64/*.a
rm -rf %{buildroot}/usr/lib64/*.so
rm -rf %{buildroot}/usr/lib64/*.spec
mkdir -p %{buildroot}/usr/lib64/haswell
mv %{buildroot}/usr/lib64/*so*  %{buildroot}/usr/lib64/haswell/

%files
%exclude /usr/lib64/haswell/libgcc_s.so.1
/usr/lib64/haswell/libgfortran.so.5
/usr/lib64/haswell/libgfortran.so.5.0.0
/usr/lib64/haswell/libgomp.so.1
/usr/lib64/haswell/libgomp.so.1.0.0
/usr/lib64/haswell/libquadmath.so.0
/usr/lib64/haswell/libquadmath.so.0.0.0
%exclude /usr/include
%exclude /usr/lib64/haswell/libitm.so.1
%exclude /usr/lib64/haswell/libitm.so.1.0.0
%exclude /usr/lib64/haswell/liblsan.so.0
%exclude /usr/lib64/haswell/liblsan.so.0.0.0
%exclude /usr/lib64/haswell/libtsan.so.0
%exclude /usr/lib64/haswell/libtsan.so.0.0.0
%exclude /usr/lib64/libasan_preinit.o
%exclude /usr/lib64/libtsan_preinit.o

%exclude    /usr/lib64/haswell/avx512_1/libgcc_s.so.1
/usr/lib64/haswell/avx512_1/libgfortran.so.5
/usr/lib64/haswell/avx512_1/libgfortran.so.5.0.0
%exclude    /usr/lib64/haswell/avx512_1/libgomp.so.1
%exclude    /usr/lib64/haswell/avx512_1/libgomp.so.1.0.0
%exclude    /usr/lib64/haswell/avx512_1/liblsan.so.0
%exclude    /usr/lib64/haswell/avx512_1/liblsan.so.0.0.0
/usr/lib64/haswell/avx512_1/libquadmath.so.0
/usr/lib64/haswell/avx512_1/libquadmath.so.0.0.0
%exclude    /usr/lib64/haswell/avx512_1/libtsan.so.0
%exclude    /usr/lib64/haswell/avx512_1/libtsan.so.0.0.0
%exclude    /usr/lib64/haswell/avx512_1/libasan.so.5
%exclude    /usr/lib64/haswell/avx512_1/libasan.so.5.0.0
   /usr/lib64/haswell/avx512_1/libstdc++.so.6
   /usr/lib64/haswell/avx512_1/libstdc++.so.6.0.*
%exclude    /usr/lib64/haswell/avx512_1/libubsan.so.1
%exclude    /usr/lib64/haswell/avx512_1/libubsan.so.1.0.0
%exclude    /usr/lib64/haswell/libasan.so.5
%exclude    /usr/lib64/haswell/libasan.so.5.0.0
   /usr/lib64/haswell/libstdc++.so.6
   /usr/lib64/haswell/libstdc++.so.6.0.*
%exclude    /usr/lib64/haswell/libubsan.so.1
%exclude    /usr/lib64/haswell/libubsan.so.1.0.0
%exclude    /usr/lib64/liblsan_preinit.o
