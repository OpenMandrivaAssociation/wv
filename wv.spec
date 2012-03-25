%define api		1.2
%define major	4
%define libname		%mklibname %{name} %{api} %{major}
%define develname	%mklibname -d %{name}

Summary:	MSWord 6/7/8/9 binary file format -> HTML converter
Name:		wv
Epoch:		1
Version:	1.2.9 
Release:	3
License:	GPLv2
Group:		Office
URL:		http://www.abisource.com/downloads/wv/
Source0:	http://www.abisource.com/downloads/wv/%{version}/wv-%{version}.tar.gz
Patch0:		%{name}-1.2.4-fix-str-fmt.patch

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libgsf-1)
BuildRequires: pkgconfig(libxml-2.0)
Buildrequires: pkgconfig(zlib)

Requires: tetex-latex
Requires: tetex-dvips

%description
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

%package -n %{libname}
Summary: Library used by wv
Group: System/Libraries
Obsoletes: %{_lib}wv1.2_3

%description -n %{libname}
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

This package provides the library that is used by wv.

%package -n %{develname}
Summary: MSWord 6/7/8/9 binary file format -> HTML converter (development)
Group: Development/C
Requires: %{libname} = %{EVRD}
Provides: %{name}-devel = %{EVRD}
Obsoletes: %{_lib}wv1.2_4-devel

%description -n %{develname}
Wv is a program that understands the Microsoft Word 6/7/8/9
binary file format and is able to convert Word
documents into HTML, which can then be read with a browser.

This is the development package.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static
%make

%install
%makeinstall_std

# uggly fix for symlink /usr/bin/wvText to wvConvert.
ln -sf wvConvert %{buildroot}/%{_bindir}/wvText
rm -f notes/decompress/a.out

%files
%doc README
%{_bindir}/wv[A-Z]*
%dir %{_datadir}/wv
%{_datadir}/wv/*.xml
%{_datadir}/wv/*.dtd
%dir %{_datadir}/wv/patterns
%{_datadir}/wv/patterns/*
%dir %{_datadir}/wv/wingdingfont
%{_datadir}/wv/wingdingfont/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libwv-%{api}.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/wv
%{_includedir}/wv/*.h
%{_libdir}/libwv.so
%{_libdir}/pkgconfig/wv-1.0.pc

