
%define module Imaging
%define python_sitepkgsdir %(echo `python -c "import sys; print (sys.prefix + '/lib/python' + sys.version[:3] + '/site-packages/')"`)
%define python_dir %(echo `python -c "import sys; print ('python' + sys.version[:3])"`)
%define python_compile_opt python -O -c "import compileall; compileall.compile_dir('.')"
%define python_compile python -c "import compileall; compileall.compile_dir('.')"

Summary:	Python's own image processing library 
Name:		python-%{module}
Version:	1.1.2
Release:	2
License:	Distributable
Group:		Development/Languages/Python
Group(de):	Entwicklung/Sprachen/Python
Group(pl):	Programowanie/Jêzyki/Python
Source0:	http://www.pythonware.com/downloads/%{module}-%{version}.tar.gz
Patch0:		Imaging-libver.patch
BuildRequires:	libjpeg-devel >= 6a
BuildRequires:	libpng >= 1.0.8
BuildRequires:	python-devel >= 2.1
BuildRequires:	sed
BuildRequires:	tk-devel
Requires:	python >= 2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python Imaging Library (PIL) adds image processing capabilities to
your Python interpreter. This library provides extensive file format
support, an efficient internal representation, and powerful image
processing capabilities.

%package devel
Summary:	Python's own image processing library header files
Group:		Development/Languages/Python
Group(de):	Entwicklung/Sprachen/Python
Group(pl):	Programowanie/Jêzyki/Python
Requires:	%{name} = %{version}

%description devel
Python's own image processing library header files.

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

( cd PIL
  %python_compile_opt python
  %python_compile
)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{python_sitepkgsdir}/%{module} \
	$RPM_BUILD_ROOT/%{_includedir}/%{python_dir}

echo %{module} > $RPM_BUILD_ROOT%{python_sitepkgsdir}/%{module}.pth
install *.so $RPM_BUILD_ROOT%{python_sitepkgsdir}/%{module}
install PIL/* $RPM_BUILD_ROOT%{python_sitepkgsdir}/%{module}
install libImaging/Im{Config,Platform,aging}.h $RPM_BUILD_ROOT/%{_includedir}/%{python_dir}

(
  cd $RPM_BUILD_ROOT%{python_sitepkgsdir}/
  ln -sf %{module} PIL
)

gzip -9nf  README FORMATS CHANGES 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %{python_sitepkgsdir}/%{module}
%{python_sitepkgsdir}/PIL
%{python_sitepkgsdir}/%{module}.pth

%attr(755,root,root) %{python_sitepkgsdir}/%{module}/*.so
%{python_sitepkgsdir}/%{module}/*.py?

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{python_dir}/*.h
