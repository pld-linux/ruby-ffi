%global gem_name ffi
Summary:	FFI Extensions for Ruby
Name:		ruby-%{gem_name}
Version:	1.4.0
Release:	1
License:	LGPL v3
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Source0-md5:	5ce1c04c23267cb550250f6d94e03c12
URL:		http://wiki.github.com/ffi/ffi
BuildRequires:	libffi-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	ruby-rspec
BuildRequires:	setup.rb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby-FFI is a ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here: <http://wiki.github.com/ffi/ffi/why-use-ffi>.

%prep
%setup -q -n %{gem_name}-%{version}

# ext build
cp -p %{_datadir}/setup.rb .

%build
%{__ruby} setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

%{__ruby} setup.rb setup

%if %{with tests}
%{__make} -f libtest/GNUmakefile
rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
install -p ext/ffi_c/ffi_c.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md History.txt LICENSE
%{ruby_vendorlibdir}/ffi.rb
%{ruby_vendorlibdir}/ffi
%attr(755,root,root) %{ruby_vendorarchdir}/ffi_c.so
