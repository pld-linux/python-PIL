#
# Conditional build:
%bcond_without	tk	# build without tkinter support
#
%define		module	PIL

Summary:	Python's own image processing library
Summary(pl):	Biblioteka do przetwarzania obrazu w Pythonie
Name:		python-%{module}
Version:	1.1.5
Release:	2
Epoch:		1
License:	distributable
Group:		Libraries/Python
Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
# Source0-md5:	a64512e39469213ced0d091b9eba76c0
Patch0:		%{name}-lib64.patch
URL:		http://www.pythonware.com/products/pil/index.htm
BuildRequires:	libjpeg-devel >= 6a
BuildRequires:	libpng-devel >= 1.0.8
BuildRequires:	python
BuildRequires:	python-devel >= 2.2.1
%{?with_tk:BuildRequires:	tk-devel}
%{?with_tk:BuildRequires:	python-tkinter}
BuildRequires:	zlib-devel
%pyrequires_eq	python-libs
Obsoletes:	python-Imaging
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python Imaging Library (PIL) adds image processing capabilities to
your Python interpreter. This library provides extensive file format
support, an efficient internal representation, and powerful image
processing capabilities.

%description -l pl
Python Imaging Library (PIL) dodaje mo¿liwo¶æ przetwarzania obrazu do
interpretera Pythona. Biblioteka daje wsparcie dla wielu formatów
plików, wydajn± reprezentacjê wewnêtrzn± i du¿e mo¿liwo¶ci obróbki

%package devel
Summary:	Python's own image processing library header files
Summary(pl):	Pliki nag³ówkowe do biblioteki obróbki obrazu w Pythonie
Group:		Development/Languages/Python
%pyrequires_eq	python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	python-Imaging-devel

%description devel
Python's own image processing library header files.

%description devel -l pl
Pliki nag³ówkowe do biblioteki obróbki obrazu w Pythonie.

%prep
%setup -q -n Imaging-%{version}

%if %{_lib} == "lib64"
%patch0 -p1 
%endif

%build
python setup.py build_ext -i
python selftest.py

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install --root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{py_incdir}
install libImaging/Im{Platform,aging}.h $RPM_BUILD_ROOT%{py_incdir}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/%{module}

rm -f $RPM_BUILD_ROOT%{py_sitedir}/%{module}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES*
%attr(755,root,root) %{_bindir}/*
%{py_sitedir}/PIL.pth
%dir %{py_sitedir}/%{module}
%attr(755,root,root) %{py_sitedir}/%{module}/*.so
%{py_sitedir}/%{module}/*.py?

%files devel
%defattr(644,root,root,755)
%{py_incdir}/*.h
