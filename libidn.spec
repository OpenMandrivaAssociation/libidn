%define	major 11
%define libname	%mklibname idn %{major}
%define develname %mklibname idn -d

Summary:	Internationalized string processing library
Name:		libidn
Version:	1.25
Release:	3
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnu.org/software/libidn/
Source0:	http://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz
Source1:	http://ftp.gnu.org/gnu/libidn/%{name}-%{version}.tar.gz.sig
Patch0:		libidn-1.25-automake-1.12.patch
BuildRequires:	autoconf automake libtool m4 intltool
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
Obsoletes:	%{mklibname idn 11 -d} < 1.25

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
	--disable-rpath \
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

find examples -type f -name ".c" | sed 's/^/%{doc} /' >> %{develname}.filelist

%find_lang %{name}

#(tpg) really not needed... also got lzma'd :)

rm -rf %{buildroot}%{_infodir}/*.png*

# this fixes a file clash in a mixed arch env
mv %{buildroot}%{_infodir}/%{name}.info %{buildroot}%{_infodir}/%{libname}.info

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

%changelog
* Wed Jun 13 2012 Andrey Bondrov <abondrov@mandriva.org> 1.25-2
+ Revision: 805325
- Fix automake 1.12 patch, drop more legacy junk
- Drop some legacy junk

* Fri Jun 01 2012 Oden Eriksson <oeriksson@mandriva.com> 1.25-1
+ Revision: 801751
- fix build
- 1.25

* Thu Jan 12 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.24-1
+ Revision: 760567
- version update 1.24

* Sat Dec 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.23-2
+ Revision: 737453
- various fixes

* Sun Nov 27 2011 Oden Eriksson <oeriksson@mandriva.com> 1.23-1
+ Revision: 733707
- fix deps
- fix build (probably...)
- 1.23
- various cleanups
- nuke static and libtool *.la files

* Sat May 07 2011 Funda Wang <fwang@mandriva.org> 1.22-1
+ Revision: 672243
- add sig
- update to new version 1.22

* Sun May 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.21-1
+ Revision: 661171
- disable make check for now
- sync some fixes from fedora

  + Funda Wang <fwang@mandriva.org>
    - new version 1.21

* Wed Mar 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.20-1
+ Revision: 641245
- 1.20

* Mon Jul 12 2010 Oden Eriksson <oeriksson@mandriva.com> 1.19-1mdv2011.0
+ Revision: 551247
- 1.19

* Mon Feb 15 2010 Frederik Himpe <fhimpe@mandriva.org> 1.18-1mdv2010.1
+ Revision: 506370
- Update to new version 1.18

* Fri Jan 15 2010 Emmanuel Andry <eandry@mandriva.org> 1.16-1mdv2010.1
+ Revision: 491778
- New version 1.16

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 1.15-2mdv2010.0
+ Revision: 449884
- disable mono/java/valgrind on mips & arm (from Arnaud Patard)

* Mon Jun 08 2009 Frederik Himpe <fhimpe@mandriva.org> 1.15-1mdv2010.0
+ Revision: 384104
- Update to new version 1.15

* Sat May 02 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.14-1mdv2010.0
+ Revision: 370768
- update to new version 1.14

* Sat Mar 07 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.13-2mdv2009.1
+ Revision: 350829
- update to new version 1.13

* Tue Dec 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1.11-2mdv2009.1
+ Revision: 314889
- rebuild

* Sun Nov 16 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.11-1mdv2009.1
+ Revision: 303615
- update to new version 1.11

  + Oden Eriksson <oeriksson@mandriva.com>
    - fix url

* Mon Sep 01 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.10-1mdv2009.0
+ Revision: 278163
- update to new version 1.10

* Fri Jul 11 2008 Oden Eriksson <oeriksson@mandriva.com> 1.9-1mdv2009.0
+ Revision: 233845
- 1.9

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun May 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.8-1mdv2009.0
+ Revision: 205890
- new version
- enable valgrind tests
- add java and mono subpackages
- fix file list

* Sun Apr 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1.7-1mdv2009.0
+ Revision: 192656
- 1.7

* Thu Feb 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5-1mdv2008.1
+ Revision: 173451
- new version

* Wed Jan 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4-1mdv2008.1
+ Revision: 157102
- new version
- remove buildrequires on libtool and autoconf
- add *.sig file
- mode docs to the binary package
- spec file clean

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 12 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3-1mdv2008.1
+ Revision: 117624
- new version

* Tue Oct 16 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2-1mdv2008.1
+ Revision: 98832
- new version
- new license policy

* Tue Sep 18 2007 Thierry Vignaud <tv@mandriva.org> 1.0-2mdv2008.0
+ Revision: 89677
- rebuild

* Tue Jul 31 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2008.0
+ Revision: 57251
- 1.0

* Thu Jul 19 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.6.14-1mdv2008.0
+ Revision: 53647
- new devel library policy
- remove not needed files
- disable rpath
- spec file clean
- new version


* Mon Mar 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 0.6.9-3mdv2007.1
+ Revision: 146601
- move devel doc in -devel

* Mon Mar 05 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.9-2mdv2007.1
+ Revision: 133202
- fix a libname dependant file clash

* Sun Mar 04 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.9-1mdv2007.1
+ Revision: 132136
- second try...
- 0.6.9
- prevent future mess with major

* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.8-1mdv2007.1
+ Revision: 74284
- 0.6.8
- misc spec file fixes
- Import libidn

* Sat Jul 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.5-1mdk
- 0.6.5

* Tue Feb 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.2-1mdk
- 0.6.2 (Minor feature enhancements)

* Fri Jan 20 2006 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-1mdk
- 0.6.1

* Thu Dec 22 2005 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-2mdk
- install-info/info-install (duh!)

* Thu Dec 22 2005 Oden Eriksson <oeriksson@mandriva.com> 0.6.0-1mdk
- 0.6.0

* Tue Oct 25 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.20-1mdk
- 0.5.20 (Minor bugfixes)

* Sat Oct 08 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.19-1mdk
- 0.5.19

* Thu Aug 11 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.18-2mdk
- fix #77181

* Tue Jul 19 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.18-1mdk
- 0.5.18 (Minor bugfixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.17-1mdk
- 0.5.17

* Tue May 10 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.16-1mdk
- 0.5.16

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 0.5.15-1mdk
- 0.5.15
- use the %%mkrel macro
- fix requires-on-release

* Sun Jan 30 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.13-1mdk
- 0.5.13

* Sun Dec 05 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.12-1mdk
- 0.5.12

* Tue Nov 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.10-1mdk
- 0.5.10

* Mon Nov 08 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.9-1mdk
- 0.5.9

* Mon Oct 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.6-1mdk
- 0.5.6

* Mon Aug 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.4-1mdk
- 0.5.4

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.2-1mdk
- 0.5.2

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.1-1mdk
- 0.5.1

* Mon Jun 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.5.0-1mdk
- 0.5.0

* Mon Jun 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.4.9-1mdk
- 0.4.9

* Sun Jun 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.4.8-1mdk
- 0.4.8

* Wed Jun 02 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.4.7-1mdk
- 0.4.7

* Wed May 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.4.6-1mdk
- 0.4.6

* Tue May 25 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.4.5-1mdk
- 0.4.5

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.4.4-1mdk
- 0.4.4, thanks to Michael Scherer for helping with the locale stuff

