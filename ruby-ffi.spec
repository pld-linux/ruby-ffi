#
# Conditional build:
%bcond_without	tests		# build without tests

%define	pkgname ffi
Summary:	FFI Extensions for Ruby
Name:		ruby-%{pkgname}
Version:	1.8.1
Release:	2
License:	LGPL v3
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	b3b511cfa03083b0ed078e28f9556517
URL:		http://wiki.github.com/ffi/ffi
BuildRequires:	libffi-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	setup.rb
%if %{with tests}
BuildRequires:	ruby-rspec
BuildRequires:	ruby-rspec-mocks
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here: <http://wiki.github.com/ffi/ffi/why-use-ffi>.

%prep
%setup -q -n %{pkgname}-%{version}

# ext build
cp -p %{_datadir}/setup.rb .

%build
%__gem_helper spec

%{__ruby} setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir} \
	--makeprog=true

%{__ruby} setup.rb setup

%{__make} -C ext/ffi_c \
	CC="%{__cc}"

%if %{with tests}
%{__make} -f libtest/GNUmakefile \
	CCACHE= \
	CC="%{__cc}"
ruby -Ilib:ext/ffi_c -S \
	rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
install -p ext/ffi_c/ffi_c.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md History.txt LICENSE
%{ruby_vendorlibdir}/ffi.rb
%{ruby_vendorlibdir}/ffi
%attr(755,root,root) %{ruby_vendorarchdir}/ffi_c.so
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
