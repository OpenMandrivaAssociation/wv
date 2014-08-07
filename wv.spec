%define api_version 1.2
%define lib_major 4
%define lib_name %mklibname %{name} %{api_version} %{lib_major}
%define develname %mklibname -d %name

Summary:	MSWord 6/7/8/9 binary file format -> HTML converter
Name:		wv
Version:	1.2.9
Release:	10
Epoch:		1
License:	GPLv2
Group:		Office
URL:		http://www.abisource.com/downloads/wv/
Source:		http://www.abisource.com/downloads/wv/%{version}/wv-%{version}.tar.gz
Patch0: 	%{name}-1.2.4-fix-str-fmt.patch
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	libgsf-devel
BuildRequires:	libxml2-devel
BuildRequires:	zlib-devel
Obsoletes:	mswordview < %{EVRD}
Provides:	mswordview = %{EVRD}
Requires:	tetex-latex
Requires:	tetex-dvips

%description
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

%package -n %{lib_name}
Summary:	Library used by wv
Group:		System/Libraries
Provides:	lib%{name} = %{EVRD}

%description -n %{lib_name}
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

This package provides the library that is used by wv.

%package -n %{develname}
Summary:	MSWord 6/7/8/9 binary file format -> HTML converter (development)
Group:		Development/C
Requires:	%{lib_name} = %{EVRD}}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}wv-1.2_3-devel < %{EVRD}
Obsoletes:	%{_lib}wv-1.2_4-devel < %{EVRD}

%description -n %{develname}
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

This is the development package.

%prep1
%setup -q
%patch0 -p1 -b .strfmt

%build
%configure
%make

%install
%makeinstall_std
# uggly fix for symlink /usr/bin/wvText to wvConvert.
ln -sf wvConvert %{buildroot}%{_bindir}/wvText
# the following file seems not to be used by any wv executable.
#cp $RPM_BUILD_DIR/%{name}/config-mswordview $RPM_BUILD_ROOT/usr/lib/mswordview
rm -f notes/decompress/a.out
# make sure libwv.a is in lib directory
# mv $RPM_BUILD_ROOT%{_datadir}/libwv.a $RPM_BUILD_ROOT%{_libdir}/libwv.a


%files
%doc README
%attr(755,root,root) %{_bindir}/wv[A-Z]*
%attr(755,root,root) %dir %{_datadir}/wv
%attr(644,root,root) %{_datadir}/wv/*.xml
%attr(644,root,root) %{_datadir}/wv/*.dtd
%attr(755,root,root) %dir %{_datadir}/wv/patterns
%attr(644,root,root) %{_datadir}/wv/patterns/*
%attr(755,root,root) %dir %{_datadir}/wv/wingdingfont
%attr(644,root,root) %{_datadir}/wv/wingdingfont/*
%attr(644,root,root) %{_mandir}/man1/*

%files -n %{lib_name}
%attr(755,root,root) %{_libdir}/libwv-%{api_version}.so.%{lib_major}*

%files -n %{develname}
%attr(755,root,root) %dir %{_includedir}/wv
%attr(644,root,root) %{_includedir}/wv/*.h
%attr(755,root,root) %{_libdir}/libwv.so
%attr(644,root,root) %{_libdir}/libwv.*a
%attr(644,root,root) %{_libdir}/pkgconfig/wv-1.0.pc
