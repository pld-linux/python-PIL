
%define module Imaging
%define python_sitepkgsdir %(echo `python -c "import sys; print (sys.prefix + '/lib/python' + sys.version[:3] + '/site-packages/')"`)
%define python_dir %(echo `python -c "import sys; print ('python' + sys.version[:3])"`)

Summary:	Python's own image processing library 
Name:		python-%{module}
Version:	1.1.1
Release: 1
Copyright:	distributable
Group:		Development/Languages/Python
Group(pl):	Programowanie/Jêzyki/Python
Source0:	http://www.pythonware.com/downloads/%{module}-%{version}.tar.gz
Patch0:	Imaging-libver.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	python >= 1.5
BuildRequires:	python-devel >= 1.5
BuildRequires:	tk-devel
BuildRequires:	sed
BuildRequires:	zlib-devel >= 1.0.4
BuildRequires:	libjpeg-devel >= 6a
BuildRequires:	libpng >= 1.0.8

%description
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.
This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%description -l pl

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
cd libImaging
%configure
%{__make} "OPT=$RPM_OPT_FLAGS"
cd ..
%{__make} -f Makefile.pre.in boot
%{__make}

cd PIL

python -O *.py

python - <<END
import py_compile, os, fnmatch

for f in os.listdir("."):
	if fnmatch.fnmatch(f, "*.py"):
		print "Byte compiling "+f+"..."
		py_compile.compile(f)
END

%install
install -d $RPM_BUILD_ROOT%{python_sitepkgsdir}/%{module}
install -d $RPM_BUILD_ROOT/%{_includedir}/%{python_dir}
echo %{module} > $RPM_BUILD_ROOT%{python_sitepkgsdir}/%{module}.pth
install -m 755 *.so $RPM_BUILD_ROOT%{python_sitepkgsdir}/%{module}
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
%doc {README,FORMATS,CHANGES}.gz
%attr(644,root,root) %{python_sitepkgsdir}/%{module}/*
%{python_sitepkgsdir}/PIL
%attr(644,root,root) %{python_sitepkgsdir}/%{module}.pth
%attr(644,root,root) %{_includedir}/%{python_dir}/*.h
