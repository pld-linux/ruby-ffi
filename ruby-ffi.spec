#
# Conditional build:
%bcond_without	tests		# build without tests

%define	pkgname ffi
Summary:	FFI Extensions for Ruby
Summary(pl.UTF-8):	Rozszerzenia FFI dla języka Ruby
Name:		ruby-%{pkgname}
Version:	1.9.6
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	8606c263037322ae957e1959245841be
Patch0:		%{name}-platform.patch
URL:		http://wiki.github.com/ffi/ffi
BuildRequires:	libffi-devel
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-devel
BuildRequires:	setup.rb
%if %{with tests}
BuildRequires:	ruby-rspec
BuildRequires:	ruby-rspec-mocks
%endif
ExclusiveArch:	%{ix86} %{x8664} arm ia64 mips mipsel ppc s390 s390x sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby-FFI is a Ruby extension for programmatically loading dynamic
libraries, binding functions within them, and calling those functions
from Ruby code. Moreover, a Ruby-FFI extension works without changes
on Ruby and JRuby. Discover why should you write your next extension
using Ruby-FFI here: <http://wiki.github.com/ffi/ffi/why-use-ffi>.

%description -l pl.UTF-8
Ruby-FFI to rozszerzenie języka Ruby do programowego ładowania
bibliotek dynamicznych, wiązania obecnych w nich funkcji oraz
wywoływania tych funkcji z kodu w języku Ruby. Co więcej, rozszerzenie
Ruby-FFI działa bez zmian w implementacji Ruby oraz JRuby. Informacje,
dlaczego nowe rozszerzenia powinny używać Ruby-FFI, można znaleźć na
stronie <http://wiki.github.com/ffi/ffi/why-use-ffi>.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

# be sure to use system ffi
%{__rm} -r ext/ffi_c/libffi

# drop not our targets
%{__rm} -r lib/ffi/platform/*-{aix,cygwin,darwin,gnu,*bsd,solaris,windows}
# provide only definitions for package architecture
%ifnarch arm
%{__rm} -r lib/ffi/platform/arm-*
%endif
%ifnarch %{ix86}
%{__rm} -r lib/ffi/platform/i386-*
%endif
%ifnarch ia64
%{__rm} -r lib/ffi/platform/ia64-*
%endif
%ifnarch mips
%{__rm} -r lib/ffi/platform/mips-*
%endif
%ifnarch mipsel
%{__rm} -r lib/ffi/platform/mipsel-*
%endif
%ifnarch powerpc
%{__rm} -r lib/ffi/platform/powerpc-*
%endif
%ifnarch s390
%{__rm} -r lib/ffi/platform/s390-*
%endif
%ifnarch s390x
%{__rm} -r lib/ffi/platform/s390x-*
%endif
%ifnarch sparc
%{__rm} -r lib/ffi/platform/sparc-*
%endif
%ifnarch %{x8664}
%{__rm} -r lib/ffi/platform/x86_64-*
%endif

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
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_vendorarchdir}/ffi,%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
install -p ext/ffi_c/ffi_c.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}
%{__mv} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/ffi/platform $RPM_BUILD_ROOT%{ruby_vendorarchdir}/ffi
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE
%{ruby_vendorlibdir}/ffi.rb
%{ruby_vendorlibdir}/ffi
%attr(755,root,root) %{ruby_vendorarchdir}/ffi_c.so
%dir %{ruby_vendorarchdir}/ffi
%{ruby_vendorarchdir}/ffi/platform
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
