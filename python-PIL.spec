
%bcond_without	tk	# build without tkinter support

%define		module	Imaging

Summary:	Python's own image processing library
Summary(pl):	Biblioteka do przetwarzania obrazu w Pythonie
Name:		python-%{module}
Version:	1.1.5a3
Release:	3
License:	distributable
Group:		Libraries/Python
Source0:	http://effbot.org/downloads/%{module}-%{version}.tar.gz
# Source0-md5:	6c004e0232e5a2ac2468467793dcadbb
Patch0:		Imaging-libver.patch
Patch1:		%{name}-EXTRA_ARGS.patch
Patch2:		%{name}-freetype.patch
URL:		http://www.pythonware.com/products/pil/index.htm
BuildRequires:	libjpeg-devel >= 6a
BuildRequires:	libpng >= 1.0.8
BuildRequires:	python
BuildRequires:	python-devel >= 2.2.1
BuildRequires:	rpm-pythonprov
%{?with_tk:BuildRequires:	tk-devel}
%{?with_tk:BuildRequires:	python-tkinter}
BuildRequires:	zlib-devel
%pyrequires_eq	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%pyrequires_eq	python
Requires:	%{name} = %{version}

%description devel
Python's own image processing library header files.

%description devel -l pl
Pliki nag��wkowe do biblioteki obr�bki obrazu w Pythonie.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd libImaging
%configure2_13
%{__make} \
	OPT="%{rpmcflags} -fPIC"
cd ..
#%%{__make} -f Makefile.pre.in boot
#%%{__make}
python setup.py build_ext -i

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{py_sitedir}/%{module},%{py_incdir}}

echo %{module} > $RPM_BUILD_ROOT%{py_sitedir}/%{module}.pth
# install *.so $RPM_BUILD_ROOT%{py_sitedir}/%{module}
install PIL/* $RPM_BUILD_ROOT%{py_sitedir}/%{module}
install libImaging/Im{Config,Platform,aging}.h $RPM_BUILD_ROOT%{py_incdir}

ln -sf %{module} $RPM_BUILD_ROOT%{py_sitedir}/PIL
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES*
%dir %{py_sitedir}/%{module}
%{py_sitedir}/PIL
%{py_sitedir}/%{module}.pth

%attr(755,root,root) %{py_sitedir}/%{module}/_imaging.so
%attr(755,root,root) %{py_sitedir}/%{module}/_imagingft.so
%{?with_tk:%attr(755,root,root) %{py_sitedir}/%{module}/_imagingtk.so}
%{py_sitedir}/%{module}/*.py?

%files devel
%defattr(644,root,root,755)
%{py_incdir}/*.h
