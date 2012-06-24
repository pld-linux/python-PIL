
%define module Imaging

Summary:	Python's own image processing library
Summary(pl):	Biblioteka do przetwarzania obrazu w Pythonie
Name:		python-%{module}
Version:	1.1.2
Release:	2
License:	distributable
Group:		Development/Languages/Python
Group(de):	Entwicklung/Sprachen/Python
Group(pl):	Programowanie/J�zyki/Python
Source0:	http://www.pythonware.com/downloads/%{module}-%{version}.tar.gz
Patch0:		Imaging-libver.patch
BuildRequires:	libjpeg-devel >= 6a
BuildRequires:	libpng >= 1.0.8
BuildRequires:	python-devel >= 2.1
BuildRequires:	sed
BuildRequires:	tk-devel
BuildRequires:	zlib-devel
%requires_eq	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%include /usr/lib/rpm/macros.python

%description
The Python Imaging Library (PIL) adds image processing capabilities to
your Python interpreter. This library provides extensive file format
support, an efficient internal representation, and powerful image
processing capabilities.

%description -l pl
Python Imaging Library (PIL) dodaje mo�liwo�� przetwarzania obrazu do
interpretera Pythona. Biblioteka daje wsparcie dla wielu format�w
plik�w, wydajn� reprezentacj� wewn�trzn� i du�e mo�liwo�ci obr�bki

%package devel
Summary:	Python's own image processing library header files
Summary(pl):	Pliki nag��wkowe do biblioteki obr�bki obrazu w Pythonie
Group:		Development/Languages/Python
Group(de):	Entwicklung/Sprachen/Python
Group(pl):	Programowanie/J�zyki/Python
%requires_eq	python
Requires:	%{name} = %{version}

%description devel
Python's own image processing library header files.

%description devel -l pl
Pliki nag��wkowe do biblioteki obr�bki obrazu w Pythonie.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
cd libImaging
%configure2_13
%{__make} "OPT=%{rpmcflags}"
cd ..
%{__make} -f Makefile.pre.in boot
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}/%{module} \
	$RPM_BUILD_ROOT/%{_includedir}/python%{py_ver}

echo %{module} > $RPM_BUILD_ROOT%{py_sitedir}/%{module}.pth
install *.so $RPM_BUILD_ROOT%{py_sitedir}/%{module}
install PIL/* $RPM_BUILD_ROOT%{py_sitedir}/%{module}
install libImaging/Im{Config,Platform,aging}.h $RPM_BUILD_ROOT/%{_includedir}/python%{py_ver}

ln -sf %{module} $RPM_BUILD_ROOT%{py_sitedir}/PIL
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

gzip -9nf  README FORMATS CHANGES 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %{py_sitedir}/%{module}
%{py_sitedir}/PIL
%{py_sitedir}/%{module}.pth

%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py?

%files devel
%defattr(644,root,root,755)
%{_includedir}/python%{py_ver}/*.h
