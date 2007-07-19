%define	major 11
%define libname	%mklibname idn %{major}

Summary:	Internationalized string processing library
Name:		libidn
Version:	0.6.14
Release:	%mkrel 1
License:	LGPL
Group:		System/Libraries
URL:		http://josefsson.org/libidn/releases/
Source0:	http://josefsson.org/libidn/releases/%{name}-%{version}.tar.gz
Source1:	http://josefsson.org/libidn/releases/%{name}-%{version}.tar.gz.sig
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	texinfo
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package -n	%{libname}
Summary:	Internationalized string processing library
Group:          System/Libraries
Requires(post): info-install
Requires(preun): info-install

%description -n	%{libname}
GNU Libidn is an implementation of the Stringprep, Punycode and
IDNA specifications defined by the IETF Internationalized Domain
Names (IDN) working group, used for internationalized domain
names.

%package -n	%{libname}-devel
Summary:	Development files for the %{libname} library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Provides:	idn-devel = %{version}
Requires:	%{libname} = %{version}
Requires:	pkgconfig

%description -n	%{libname}-devel
Development files for the %{libname} library

%package -n	idn
Summary:	Commandline interface to the %{libname} library
Group:          System/Servers

%description -n	idn
This package provides the commandline interface to the
%{libname} library

%prep

%setup -q


%build
#export WANT_AUTOCONF_2_5=1
#libtoolize --copy --force; aclocal; autoconf

# wierd stuff...
%define __libtoolize /bin/true

%configure2_5x


%make

%check
make check

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# house cleansing
rm -f %{buildroot}%{_libdir}/Libidn.dll

# fix "invalid-lc-messages-dir":
rm -rf %{buildroot}%{_datadir}/locale/en@*quot

# make a nice list for docs
find doc -type f | sed 's/^/%doc /' | \
    grep -v "Makefile*" | \
    grep -v "\.tex*" | \
    grep -v "\.info" | \
    grep -v "\.1" | \
    grep -v "\.3" | \
    grep -v "\.sgml" | \
    grep -v "\.xml" | \
    grep -v "gdoc" | \
    grep -v "mdate-sh" > %{libname}-devel.filelist

find examples -type f -name ".c" | sed 's/^/%doc /' >> %{libname}-devel.filelist

%find_lang libidn

# this fixes a file clash in a mixed arch env
mv %{buildroot}%{_infodir}/%{name}.info %{buildroot}%{_infodir}/%{libname}.info

%post -n %{libname}
%_install_info %{libname}.info
/sbin/ldconfig

%postun -n %{libname}
%_remove_install_info %{libname}.info
/sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n idn -f libidn.lang
%defattr(0644,root,root,755)
%doc ChangeLog FAQ README
%attr(0755,root,root) %{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_datadir}/emacs/site-lisp/*.el

%files -n %{libname}
%defattr(0644,root,root,755)
%doc FAQ README THANKS contrib
%attr(0755,root,root) %{_libdir}/libidn.so.%{major}.*
%attr(0755,root,root) %{_libdir}/libidn.so.%{major}
%{_infodir}/%{libname}.info*

%files -n %{libname}-devel -f %{libname}-devel.filelist
%defattr(0644,root,root,755)
%doc ChangeLog doc/libidn.html TODO libc/example.c examples/README examples/Makefile.*
%{_libdir}/libidn.so
%{_libdir}/libidn.a
%{_libdir}/libidn.la
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*


