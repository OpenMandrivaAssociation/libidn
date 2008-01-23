%define	major 11
%define libname	%mklibname idn %{major}
%define develname %mklibname idn -d

Summary:	Internationalized string processing library
Name:		libidn
Version:	1.4
Release:	%mkrel 1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://josefsson.org/libidn/releases/
Source0:	http://josefsson.org/libidn/releases/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
BuildRequires:	texinfo
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
Requires:	%{libname} = %{version}-%{release}
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

%prep
%setup -q


%build
%configure2_5x \
	--disable-rpath

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

%post -n %{libname}
%_install_info %{libname}.info
/sbin/ldconfig
 
%postun -n %{libname}
%_remove_install_info %{libname}.info
/sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n idn -f %{name}.lang
%defattr(0644,root,root,755)
%doc ChangeLog FAQ README THANKS contrib
%attr(0755,root,root) %{_bindir}/idn
%{_mandir}/man1/idn.1*
%{_datadir}/emacs/site-lisp/*.el

%files -n %{libname}
%defattr(0644,root,root,755)
%attr(0755,root,root) %{_libdir}/libidn.so.%{major}*
%{_infodir}/%{libname}.info*

%files -n %{develname} -f %{develname}.filelist
%defattr(0644,root,root,755)
%doc ChangeLog doc/libidn.html TODO libc/example.c examples/README examples/Makefile.*
%{_libdir}/libidn.so
%{_libdir}/libidn.a
%{_libdir}/libidn.la
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
