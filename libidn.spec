%bcond_with crosscompile
%bcond_with java

%define	major 11
%define libname %mklibname idn %{major}
%define devname %mklibname idn -d

Summary:	Internationalized string processing library
Name:		libidn
Version:	1.29
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gnu.org/software/libidn/
Source0:	http://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
Patch0:		libidn-1.25-automake-1.12.patch
Patch1000:	002-disable-po-docs-examples.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	m4
BuildRequires:	texinfo
BuildRequires:	gettext-devel
%if %{with java}
BuildRequires:	valgrind
BuildRequires:	java-rpmbuild
%endif
# disable on arm for now. test it again on real hardware. qemu doesn't like it
%ifnarch %mips %arm aarch64
BuildRequires:	mono
%endif

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package -n %{libname}
Summary:	Internationalized string processing library
Group:		System/Libraries

%description -n	%{libname}
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package -n %{devname}
Summary:	Development files for the %{libname} library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	idn-devel = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}
Obsoletes:	%{mklibname idn 11 -d} < 1.25

%description -n	%{devname}
Development files for the %{libname} library.

%package -n idn
Summary:	Commandline interface to the %{libname} library
Group:		System/Servers

%description -n idn
This package provides the commandline interface to the
%{libname} library.

%if %{with java}
%package -n %{libname}-java
Summary:	Java support for the %{name}
Group:		Development/Java
Provides:	%{name}-java = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}

%description -n %{libname}-java
Java support for the %{name}.
%endif

%ifnarch %mips %arm aarch64
%package -n %{libname}-mono
Summary:	Mono support for the %{name}
Group:		Development/Other
Provides:	%{name}-mono = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}

%description -n %{libname}-mono
Mono support for the %{name}.
%endif

%prep
%setup -q
%patch0 -p1
%if %{with crosscompile}
%patch1000 -p1
%endif

# bundled, with wrong bytecode
find . -name java/*.jar -delete

# Name directory sections consistently in the info file, rhbz #209491
sed -i '/^INFO-DIR-SECTION/{s/GNU Libraries/Libraries/;s/GNU utilities/Utilities/;}' doc/libidn.info

iconv -f ISO-8859-1 -t UTF-8 doc/libidn.info > iconv.tmp
mv iconv.tmp doc/libidn.info

aclocal -I m4 -I gl/m4 -I lib/gl/m4 --dont-fix
automake -a
autoconf

%build
%configure \
%if %{with java}
	--enable-java \
	--enable-valgrind-tests \
%endif
%ifnarch %arm %mips aarch64
	--enable-csharp=mono \
%endif
	--with-packager="OpenMandriva" \
	--with-packager-bug-reports="http://issues.openmandriva.org" \
	--disable-static

%make

%install
%makeinstall_std

# fix "invalid-lc-messages-dir":
rm -rf %{buildroot}%{_datadir}/locale/en@*quot

# make a nice list for docs
find doc -type f | sed 's/^/%{doc} /' | \
    grep -v "Makefile*" | \
    grep -v "\.tex*" | \
    grep -v "\.info" | \
    grep -v "\.1" | \
    grep -v "\.3" | \
    grep -v "\.sgml" | \
    grep -v "\.xml" | \
    grep -v "gdoc" | \
    grep -v "mdate-sh" > %{libname}-devel.filelist

find examples -type f -name ".c" | sed 's/^/%{doc} /' >> %{devname}.filelist

%find_lang %{name}

#(tpg) really not needed... also got lzma'd :)

rm -rf %{buildroot}%{_infodir}/*.png*

%if !%{with crosscompile}
# this fixes a file clash in a mixed arch env
mv %{buildroot}%{_infodir}/%{name}.info %{buildroot}%{_infodir}/%{libname}.info
%endif

%files -n idn -f %{name}.lang
%doc ChangeLog FAQ README THANKS contrib
%{_bindir}/idn
%{_datadir}/*emacs/site-lisp/*.el
%if !%{with crosscompile}
%{_infodir}/%{libname}.info*
%{_mandir}/man1/idn.1*
%endif

%files -n %{libname}
%{_libdir}/libidn.so.%{major}*

%files -n %{devname} -f %{devname}.filelist
%doc doc/libidn.html TODO libc/example.c examples/README examples/Makefile.*
%{_libdir}/libidn.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%if !%{with crosscompile}
%{_mandir}/man3/*
%endif

%if %{with java}
%files -n %{libname}-java
%{_datadir}/java/*.jar
%endif

%ifnarch %mips %arm aarch64
%files -n %{libname}-mono
%{_libdir}/*.dll
%endif
