%define name wv
%define version 1.2.4
%define real_version %version
%define serial 1

%define api_version 1.2
%define lib_major   3
%define lib_name    %mklibname %{name}- %{api_version} %{lib_major}

Summary: MSWord 6/7/8/9 binary file format -> HTML converter
Name: %{name}
Version: %{version}
Release: %mkrel 8
Epoch: %{serial}
License: GPLv2
Group: Office
URL: http://sourceforge.net/projects/wvware/
Source: http://prdownloads.sourceforge.net/wvware/%{name}-%{real_version}.tar.bz2
Patch0: %{name}-1.2.4-fix-str-fmt.patch
Patch1: wv-1.2.4-linkage.patch
BuildRequires: X11-devel
BuildRequires: glib2-devel
BuildRequires: libwmf-devel >= 0.2.8
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel 
BuildRequires: libxml2-devel
BuildRequires: libgsf-devel
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

%package -n %{lib_name}-devel
Summary: MSWord 6/7/8/9 binary file format -> HTML converter (development)
Group: Development/C
Requires: %{lib_name} = %{serial}:%{version}
Provides: %{name}-devel = %{serial}:%{version}

%description -n %{lib_name}-devel
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

This is the development package.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .strfmt
%patch1 -p0 -b .linkage

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

%files -n %{lib_name}-devel
%defattr(-,root,root)
%attr(755,root,root) %dir %{_includedir}/wv
%attr(644,root,root)      %{_includedir}/wv/*.h
%attr(755,root,root)      %{_libdir}/libwv.so
%attr(644,root,root)      %{_libdir}/libwv.*a
%attr(644,root,root)      %{_libdir}/pkgconfig/wv-1.0.pc
