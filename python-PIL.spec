%define pp_subname Imaging
Summary:	Python's own image processing library 
Name:		python-%{pp_subname}
Version:	1.0
Release:	1
Copyright:	distributable
Group:		Development/Languages/Python
Group(pl):	Programowanie/Jêzyki/Python
Source0:	http://www.pythonware.com/downloads/%{pp_subname}-%{version}.tar.gz
#Icon:		linux-python-small.gif 
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	python >= 1.5
BuildRequires:	python-devel >= 1.5
BuildRequires:	sed
BuildRequires:	zlib-devel >= 1.0.4
BuildRequires:	libjpeg-devel >= 6a
BuildRequires:	libpng-devel >= 1.0.1

%description
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.
This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%description -l pl

%prep
%setup -q -n %{pp_subname}-%{version}

%build
cd libImaging
./configure
make "OPT=$RPM_OPT_FLAGS"
cd ..
make -f Makefile.pre.in boot
make

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
install -d $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}
install -d $RPM_BUILD_ROOT/%{_includedir}/python1.5
echo %{pp_subname} > $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}.pth
install -m 755 *.so $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}
install PIL/* $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}
install libImaging/Im{Config,Platform,aging}.h $RPM_BUILD_ROOT/%{_includedir}/python1.5

(
  cd $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/
  ln -sf %{pp_subname} PIL
)

gzip -9nf  README FORMATS CHANGES 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc {README,FORMATS,CHANGES}.gz
%attr(644,root,root) %{_libdir}/python1.5/site-packages/%{pp_subname}/*
%{_libdir}/python1.5/site-packages/PIL
%attr(644,root,root) %{_libdir}/python1.5/site-packages/%{pp_subname}.pth
%attr(644,root,root) %{_includedir}/python1.5/*.h
