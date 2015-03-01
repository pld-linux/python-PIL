#
# Conditional build:
%bcond_without	tk	# build without tkinter support

%define		module	PIL
Summary:	Python's own image processing library
Summary(pl.UTF-8):	Biblioteka do przetwarzania obrazu w Pythonie
Name:		python-%{module}
Version:	1.1.7
Release:	7
Epoch:		1
License:	BSD-like
Group:		Libraries/Python
Source0:	http://effbot.org/downloads/Imaging-%{version}.tar.gz
# Source0-md5:	fc14a54e1ce02a0225be8854bfba478e
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-viewer.patch
Patch2:		python-imaging-1.1.6-sane-types.patch
Patch3:		python-imaging-giftrans.patch
URL:		http://www.pythonware.com/products/pil/
BuildRequires:	freetype-devel >= 1:2.3.9
BuildRequires:	lcms-devel >= 1.1.5
BuildRequires:	libjpeg-devel >= 6a
BuildRequires:	python >= 1:2.5
BuildRequires:	python-devel >= 1:2.5
%{?with_tk:BuildRequires:	python-tkinter}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sane-backends-devel
%{?with_tk:BuildRequires:	tk-devel}
BuildRequires:	zlib-devel >= 1.2.3
%pyrequires_eq	python-libs
Requires:	freetype >= 1:2.3.9
Requires:	lcms >= 1.1.5
Requires:	zlib >= 1.2.3
Obsoletes:	python-Imaging
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python Imaging Library (PIL) adds image processing capabilities to
your Python interpreter. This library provides extensive file format
support, an efficient internal representation, and powerful image
processing capabilities.

%description -l pl.UTF-8
Python Imaging Library (PIL) dodaje możliwość przetwarzania obrazu do
interpretera Pythona. Biblioteka ma obsługę wielu formatów plików,
wydajną reprezentację wewnętrzną i duże możliwości obróbki.

%package sane
Summary:	Python Module for using scanners
Summary(pl.UTF-8):	Moduły Pythona do używania skanerów
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description sane
This package contains the sane module for Python which provides access
to various raster scanning devices such as flatbed scanners and
digital cameras.

%description sane -l pl.UTF-8
Ten pakiet zawiera moduł sane dla Pythona, dający dostęp do wielu
rastrowych urządzeń skanujących, takich jak skanery płaskie i aparaty
cyfrowe.

%package tk
Summary:	Tk interface for python-imaging
Summary(pl.UTF-8):	Interfejs Tk do modułów python-imaging
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-tkinter
Conflicts:	%{name} < 1:1.1.6-6

%description tk
This package contains a Tk interface for python-imaging.

%description tk -l pl.UTF-8
Ten pakiet zawiera interfejs Tk do modułów python-imaging.

%package devel
Summary:	Python's own image processing library header files
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki obróbki obrazu w Pythonie
Group:		Development/Languages/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libjpeg-devel
Requires:	python-devel
Requires:	zlib-devel
Obsoletes:	python-Imaging-devel

%description devel
Python's own image processing library header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe do biblioteki obróbki obrazu w Pythonie.

%prep
%setup -q -n Imaging-%{version}
%if %{_lib} == "lib64"
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1

# fix the interpreter path for Scripts/*.py
sed -i -e "s|/usr/local/bin/python|%{_bindir}/python|" Scripts/*.py

%build
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build_ext -i
%{__python} selftest.py

cd Sane
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

cd Sane
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
cd ..

install -d $RPM_BUILD_ROOT%{py_incdir}
cp -a libImaging/Im{Platform,aging}.h $RPM_BUILD_ROOT%{py_incdir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT{%{_bindir}/pil*.py,%{_examplesdir}/%{name}-%{version}}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/%{module}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%{py_sitedir}/%{module}.pth
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_imaging*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}/%{module}-*.egg-info
%endif

%{_examplesdir}/%{name}-%{version}

%if %{with tk}
%exclude %{py_sitedir}/%{module}/ImageTk.py[co]
%exclude %{py_sitedir}/%{module}/SpiderImagePlugin.py[co]
%exclude %{py_sitedir}/%{module}/_imagingtk.so
%endif

%files sane
%defattr(644,root,root,755)
%doc Sane/CHANGES Sane/demo*.py Sane/sanedoc.txt
%{py_sitedir}/sane.py[co]
%attr(755,root,root) %{py_sitedir}/_sane.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/pysane-*.egg-info
%endif

%if %{with tk}
%files tk
%defattr(644,root,root,755)
%{py_sitedir}/%{module}/ImageTk.py[co]
%{py_sitedir}/%{module}/SpiderImagePlugin.py[co]
%attr(755,root,root) %{py_sitedir}/%{module}/_imagingtk.so
%endif

%files devel
%defattr(644,root,root,755)
%{py_incdir}/ImPlatform.h
%{py_incdir}/Imaging.h
