%define pp_subname Imaging
Summary:       Python's own image processing library 
Name:          python-%{pp_subname}
Version:       1.0
Release:       1
Copyright:     distributable
Group:         Development/Languages/Python
Group(pl):     Programowanie/Jêzyki/Python
Source0:       %{pp_subname}-%{version}.tar.gz
Icon:          linux-python-small.gif 
BuildRoot:	   /tmp/%{name}-%{version}-root
Requires:      python >= 1.5
BuildRequires: python-devel >= 1.5, sed, zlib-devel >= 1.0.4 , libjpeg-devel >= 6a, libpng-devel >= 1.0.1

%description
The Python Imaging Library (PIL) adds image processing capabilities 
to your Python interpreter.
This library provides extensive file format support, an efficient
internal representation, and powerful image processing capabilities.

%prep
%setup -n %{pp_subname}-%{version}

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
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}
echo %{pp_subname} > $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}.pth
install -m 755 *.so $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}
install -m 644 PIL/* $RPM_BUILD_ROOT%{_libdir}/python1.5/site-packages/%{pp_subname}
install -d -m 755 $RPM_BUILD_ROOT/%{_includedir}/python1.5
install -m 644 libImaging/Im{Config,Platform,aging}.h $RPM_BUILD_ROOT/%{_includedir}/python1.5
gzip -9nf README FORMATS CHANGES 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc {README,FORMATS,CHANGES}.gz
%{_libdir}/python1.5/site-packages/%{pp_subname}
%{_libdir}/python1.5/site-packages/%{pp_subname}.pth
%{_includedir}/python1.5/*
