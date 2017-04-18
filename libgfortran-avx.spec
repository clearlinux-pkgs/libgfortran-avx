%define keepstatic 1
%define gcc_target %{_arch}-generic-linux
%define libstdcxx_maj 6
%define libstdcxx_full 6.0.21
%define isl_version 0.14

%define debug_package %{nil}


# Highest optimisation ABI we target
%define mtune haswell

Name     : libgfortran-avx
Version  : 6.3.0
Release  : 6
URL      : http://www.gnu.org/software/gcc/
Source0  : http://ftp.gnu.org/gnu/gcc/gcc-6.3.0/gcc-6.3.0.tar.bz2
Source1  : ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Summary  : AVX optinuzed libgfortran
Group    : Development/Tools
License  : BSD-3-Clause BSL-1.0 GFDL-1.2 GFDL-1.3 GPL-2.0 GPL-3.0 LGPL-2.1 LGPL-3.0 MIT
Patch0   : 0001-Fix-stack-protection-issues.patch
Patch2   : openmp-vectorize.patch

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

Requires: gcc-libubsan

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

%package -n gcc-dev
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Provides:       libgcov-dev
Provides:       libssp-dev
Provides:       libssp-staticdev
Provides:       libgomp-dev
Provides:       libgomp-staticdev
Provides:       libgcc-s-dev
Provides:       gcc-plugin-dev

Provides:       libstdc++-dev

%description -n gcc-dev
GNU cc and gcc C compilers dev files


%package -n libgcc1
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Requires:       filesystem
Provides:       libssp0
Provides:       libgomp1

%description -n libgcc1
GNU cc and gcc C compilers.

%package libubsan
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel

%description libubsan
Address sanitizer runtime libs

%package -n libstdc++
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          devel
Provides:       libstdc++-extra

%description -n libstdc++
GNU cc and gcc C compilers.

%package -n gcc-doc
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          doc

%package go
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU Compile Collection GO compiler
Group:          devel

%description go
GNU Compile Collection GO compiler

%package go-lib
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU Compile Collection GO runtime
Group:          devel

%description go-lib
GNU Compile Collection GO runtime

%description -n gcc-doc
GNU cc and gcc C compilers.

%package -n gcc-locale
License:        GPL-3.0-with-GCC-exception and GPL-3.0
Summary:        GNU cc and gcc C compilers
Group:          libs

%description -n gcc-locale
GNU cc and gcc C compilers.


%prep
%setup -q -n gcc-%{version}
%patch0 -p1
%patch2 -p1

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
export CFLAGS_FOR_TARGET="$CFLAGS"

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
    --enable-languages="fortran" \
    --with-ppl=yes \
    --with-isl \
    --includedir=%{_includedir} \
    --with-gxx-include-dir=%{_includedir}/c++/ \
    --exec-prefix=%{_prefix} \
    --with-glibc-version=2.19 \
    --with-system-libunwind \
    --with-gnu-ld \
    --with-tune=haswell \
    --with-arch=ivybridge \
    --disable-bootstrap \
    --enable-libmpx

make %{?_smp_mflags}

popd



%install
export CPATH=%{_includedir}
export LIBRARY_PATH=%{_libdir}
pushd ../gcc-build
%make_install
cd -
rm -rf %{buildroot}/usr/share
rm -rf %{buildroot}/usr/bin
rm -rf %{buildroot}/usr/lib64/gcc/
rm -rf %{buildroot}/usr/lib64/*.a
rm -rf %{buildroot}/usr/lib64/*.so
rm -rf %{buildroot}/usr/lib64/*.spec
mkdir -p %{buildroot}/usr/lib64/haswell
mv %{buildroot}/usr/lib64/*so*  %{buildroot}/usr/lib64/haswell/

%files
%exclude /usr/lib64/haswell/libatomic.so.1
%exclude /usr/lib64/haswell/libatomic.so.1.2.0
%exclude /usr/lib64/haswell/libcc1.so.0
%exclude /usr/lib64/haswell/libcc1.so.0.0.0
%exclude /usr/lib64/haswell/libgcc_s.so.1
/usr/lib64/haswell/libgfortran.so.3
/usr/lib64/haswell/libgfortran.so.3.0.0
/usr/lib64/haswell/libgomp.so.1
/usr/lib64/haswell/libgomp.so.1.0.0
%exclude /usr/lib64/haswell/libmpx.so.2
%exclude /usr/lib64/haswell/libmpx.so.2.0.0
%exclude /usr/lib64/haswell/libmpxwrappers.so.2
%exclude /usr/lib64/haswell/libmpxwrappers.so.2.0.0
/usr/lib64/haswell/libquadmath.so.0
/usr/lib64/haswell/libquadmath.so.0.0.0
%exclude /usr/lib64/haswell/libssp.so.0
%exclude /usr/lib64/haswell/libssp.so.0.0.0
