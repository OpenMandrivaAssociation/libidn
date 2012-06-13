%define	major 11
%define libname	%mklibname idn %{major}
%define develname %mklibname idn -d

Summary:	Internationalized string processing library
Name:		libidn
Version:	1.25
Release:	2
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnu.org/software/libidn/
Source0:	http://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
Source1:	http://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz.sig
Patch0:		libidn-1.25-automake-1.12.patch
BuildRequires:	autoconf automake libtool m4 intltool pkgconfig perl
BuildRequires:	texinfo gtk-doc gettext gettext-devel
%ifnarch %mips %arm
BuildRequires:	valgrind
BuildRequires:	java-rpmbuild
%endif
# disable on arm for now. test it again on real hardware. qemu doesn't like it
%ifnarch %mips %arm
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
Requires(post):	info-install
Requires(preun): info-install

%description -n	%{libname}
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package -n %{develname}
Summary:	Development files for the %{libname} library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	idn-devel = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}
Requires:	pkgconfig
Obsoletes:	%mklibname idn 11 -d

%description -n	%{develname}
Development files for the %{libname} library.

%package -n idn
Summary:	Commandline interface to the %{libname} library
Group:		System/Servers

%description -n idn
This package provides the commandline interface to the
%{libname} library.

%ifnarch %mips %arm
%package -n %{libname}-java
Summary:	Java support for the %{name}
Group:		Development/Java
Provides:	%{name}-java = %{version}-%{release}
Requires:	%{libname} >= %{version}-%{release}

%description -n %{libname}-java
Java support for the %{name}.

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

# Name directory sections consistently in the info file, rhbz #209491
sed -i '/^INFO-DIR-SECTION/{s/GNU Libraries/Libraries/;s/GNU utilities/Utilities/;}' doc/libidn.info

iconv -f ISO-8859-1 -t UTF-8 doc/libidn.info > iconv.tmp
mv iconv.tmp doc/libidn.info

%build
autoreconf -fi

%configure2_5x \
%ifnarch %mips %arm
	--enable-java \
	--enable-valgrind-tests \
%endif
%ifnarch %mips %arm
	--enable-csharp=mono \
%endif
	--disable-rpath

%make

#%%check
#make check

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

find examples -type f -name ".c" | sed 's/^/%{doc} /' >> %{develname}.filelist

%find_lang %{name}

#(tpg) really not needed... also got lzma'd :)

rm -rf %{buildroot}%{_infodir}/*.png*

# this fixes a file clash in a mixed arch env
mv %{buildroot}%{_infodir}/%{name}.info %{buildroot}%{_infodir}/%{libname}.info

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n idn -f %{name}.lang
%doc ChangeLog FAQ README THANKS contrib
%{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_datadir}/emacs/site-lisp/*.el

%files -n %{libname}
%{_libdir}/libidn.so.%{major}*
%{_infodir}/%{libname}.info*

%files -n %{develname} -f %{develname}.filelist
%doc doc/libidn.html TODO libc/example.c examples/README examples/Makefile.*
%{_libdir}/libidn.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%ifnarch %mips %arm
%files -n %{libname}-java
%{_datadir}/java/*.jar
%endif

%ifnarch %mips %arm
%files -n %{libname}-mono
%{_libdir}/*.dll
%endif
