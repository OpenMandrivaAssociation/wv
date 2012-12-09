%define name wv
%define version 1.2.9
%define real_version %version
%define serial 1

%define api_version 1.2
%define lib_major   4
%define lib_name    %mklibname %{name} %{api_version} %{lib_major}
%define develname   %mklibname -d %name

Summary: MSWord 6/7/8/9 binary file format -> HTML converter
Name: %{name}
Version: %{version}
Release: %mkrel 4
Epoch: %{serial}
License: GPLv2
Group: Office
URL: http://www.abisource.com/downloads/wv/
Source: http://www.abisource.com/downloads/wv/%{version}/wv-%{version}.tar.gz
Patch0: %{name}-1.2.4-fix-str-fmt.patch
BuildRequires: glib2-devel
BuildRequires: libgsf-devel
BuildRequires: libxml2-devel
Buildrequires: zlib-devel
BuildRoot: %{_tmppath}/%{name}-buildroot
Obsoletes: mswordview 
Provides: mswordview
Requires: tetex-latex
Requires: tetex-dvips

%description
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

%package -n %{lib_name}
Summary: Library used by wv
Group: System/Libraries
Provides: lib%{name} = %{serial}:%{version}-%{release}

%description -n %{lib_name}
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

This package provides the library that is used by wv.

%package -n %{develname}
Summary: MSWord 6/7/8/9 binary file format -> HTML converter (development)
Group: Development/C
Requires: %{lib_name} = %{serial}:%{version}
Provides: %{name}-devel = %{serial}:%{version}
Obsoletes: %{_lib}wv-1.2_3-devel
Obsoletes: %{_lib}wv-1.2_4-devel

%description -n %{develname}
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

This is the development package.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .strfmt

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
# uggly fix for symlink /usr/bin/wvText to wvConvert.
ln -sf wvConvert $RPM_BUILD_ROOT/%{_bindir}/wvText
# the following file seems not to be used by any wv executable.
#cp $RPM_BUILD_DIR/%{name}/config-mswordview $RPM_BUILD_ROOT/usr/lib/mswordview
rm -f notes/decompress/a.out
# make sure libwv.a is in lib directory
# mv $RPM_BUILD_ROOT%{_datadir}/libwv.a $RPM_BUILD_ROOT%{_libdir}/libwv.a

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%attr(755,root,root)      %{_bindir}/wv[A-Z]*
%attr(755,root,root) %dir %{_datadir}/wv
%attr(644,root,root)      %{_datadir}/wv/*.xml
%attr(644,root,root)      %{_datadir}/wv/*.dtd
%attr(755,root,root) %dir %{_datadir}/wv/patterns
%attr(644,root,root)      %{_datadir}/wv/patterns/*
%attr(755,root,root) %dir %{_datadir}/wv/wingdingfont
%attr(644,root,root)      %{_datadir}/wv/wingdingfont/*
%attr(644,root,root)      %{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%attr(755,root,root)      %{_libdir}/libwv-%{api_version}.so.%{lib_major}*

%files -n %{develname}
%defattr(-,root,root)
%attr(755,root,root) %dir %{_includedir}/wv
%attr(644,root,root)      %{_includedir}/wv/*.h
%attr(755,root,root)      %{_libdir}/libwv.so
%attr(644,root,root)      %{_libdir}/libwv.*a
%attr(644,root,root)      %{_libdir}/pkgconfig/wv-1.0.pc


%changelog
* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 1:1.2.9-2mdv2011.0
+ Revision: 662444
- system devel package policy

* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 1:1.2.9-1
+ Revision: 662292
- new version 1.2.9
- tighten BR

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-10mdv2011.0
+ Revision: 608175
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-9mdv2010.1
+ Revision: 524359
- rebuilt for 2010.1

* Sun Jun 14 2009 Funda Wang <fwang@mandriva.org> 1:1.2.4-8mdv2010.0
+ Revision: 385829
- fix linakge on libwmf

* Sun Jun 14 2009 Funda Wang <fwang@mandriva.org> 1:1.2.4-7mdv2010.0
+ Revision: 385828
- requires wmf for *.la

* Thu May 21 2009 JÃ©rÃ´me Brenier <incubusss@mandriva.org> 1:1.2.4-6mdv2010.0
+ Revision: 378384
- fix str fmt (1 patch added)
- fix license

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1:1.2.4-5mdv2009.0
+ Revision: 225931
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-4mdv2008.1
+ Revision: 179676
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Tue Jun 12 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1:1.2.4-3mdv2008.0
+ Revision: 38366
- rebuild for expat


* Mon Jan 29 2007 GÃ¶tz Waschk <waschk@mandriva.org> 1.2.4-2mdv2007.0
+ Revision: 115126
- fix major
- drop disabled patches

* Sun Jan 28 2007 JÃ©rÃ´me Soyer <saispo@mandriva.org> 1:1.2.4-1mdv2007.1
+ Revision: 114726
- New release 1.2.4
- Import wv

* Thu Jun 22 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1:1.2.0-5mdv2007.1
- Rebuild

* Wed Jun 21 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1:1.2.0-5mdk
- Rebuild

* Tue Mar 07 2006 GÃ¶tz Waschk <waschk@mandriva.org> 1.2.0-4mdk
- rebuild with new libgsf

* Wed Oct 19 2005 Götz Waschk <waschk@mandriva.org> 1.2.0-3mdk
- fix buildrequires

* Tue Oct 18 2005 Götz Waschk <waschk@mandriva.org> 1.2.0-2mdk
- fix buildrequires

* Tue Oct 18 2005 Marcel Pol <mpol@mandrake.org> 1.2.0-1mdk
- 1.2.0
- mkrel
- update api_version and lib_major
- drop P0, changes upstream
- drop P1, afaik it didn't apply anymore anyway

* Sun Sep 18 2005 Götz Waschk <waschk@mandriva.org> 1.0.3-3mdk
- open ole2 files read only

* Tue Jun 14 2005 Götz Waschk <waschk@mandriva.org> 1.0.3-2mdk
- major 3

* Tue Jun 14 2005 Götz Waschk <waschk@mandriva.org> 1.0.3-1mdk
- fix source URL
- New release 1.0.3

* Tue Aug 10 2004 Marcel Pol <mpol@mandrake.org> 1.0.2-1mdk
- 1.0.2
- drop patch2
- increase major

* Fri Jul 30 2004 Marcel Pol <mpol@mandrake.org> 1.0.0-3mdk
- fix provides of devel package

* Mon Jul 26 2004 Marcel Pol <mpol@mandrake.org> 1.0.0-2mdk
- patch2: buffer overflow bugfix

* Tue Jun 01 2004 Marcel Pol <mpol@mandrake.org> 1.0.0-1mdk
- 1.0.0
- updated files section
- libify
- manually set manonedir in %%makeinstall
- require tetex-latex and tetex-dvips for pdf, ps, etc.

* Fri Feb 27 2004 Stew Benedict <sbenedict@mandrakesoft.com> 0.7.4-3mdk
- fix -devel dependencies (epoch)

* Wed Feb 25 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.7.4-2mdk
- rebuild && reupload

