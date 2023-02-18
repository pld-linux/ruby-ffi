#
# Conditional build:
%bcond_without	tests	# testing

%define	ffi_req	7:3.2
%define	pkgname ffi
Summary:	FFI Extensions for Ruby
Summary(pl.UTF-8):	Rozszerzenia FFI dla języka Ruby
Name:		ruby-%{pkgname}
Version:	1.15.5
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	026cce18ef8ffc713be29c2ffc9d335b
Patch0:		%{name}-platform.patch
Patch1:		ffi-x32.patch
URL:		https://wiki.github.com/ffi/ffi
BuildRequires:	libffi-devel >= %{ffi_req}
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	ruby-devel
%if %{with tests}
BuildRequires:	ruby-rspec
BuildRequires:	ruby-rspec-mocks
%endif
Requires:	libffi >= %{ffi_req}
ExclusiveArch:	%{ix86} %{x8664} x32 aarch64 %{arm} ia64 mips mipsel mips64 mips64el powerpc64 powerpc64le ppc s390 s390x riscv64 sparc sparcv9 sparc64
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
%patch1 -p1

# be sure to use system ffi
%{__rm} -r ext/ffi_c/libffi

# drop not our targets
%{__rm} -r lib/ffi/platform/*-{aix,cygwin,darwin,freebsd12,*bsd,gnu,haiku,msys,solaris,windows}
# provide only definitions for package architecture
%ifnarch aarch64
%{__rm} -r lib/ffi/platform/aarch64-*
%endif
%ifnarch %{arm}
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
%{__rm} -r lib/ffi/platform/mipsisa32r6-*
%endif
%ifnarch mipsel
%{__rm} -r lib/ffi/platform/mipsel-*
%{__rm} -r lib/ffi/platform/mipsisa32r6el-*
%endif
%ifnarch mips64
%{__rm} -r lib/ffi/platform/mips64-*
%{__rm} -r lib/ffi/platform/mipsisa64r6-*
%endif
%ifnarch mips64el
%{__rm} -r lib/ffi/platform/mips64el-*
%{__rm} -r lib/ffi/platform/mipsisa64r6el-*
%endif
%ifnarch powerpc
%{__rm} -r lib/ffi/platform/powerpc-*
%endif
%ifnarch powerpc64
%{__rm} -r lib/ffi/platform/powerpc64-*
%endif
%ifnarch powerpc64le
%{__rm} -r lib/ffi/platform/powerpc64le-*
%endif
%ifnarch s390
%{__rm} -r lib/ffi/platform/s390-*
%endif
%ifnarch s390x
%{__rm} -r lib/ffi/platform/s390x-*
%endif
%ifnarch riscv64
%{__rm} -r lib/ffi/platform/riscv64-*
%endif
%ifnarch sparc sparcv9
%{__rm} -r lib/ffi/platform/sparc-*
%endif
%ifnarch sparc64
%{__rm} -r lib/ffi/platform/sparc64-*
%endif
%ifnarch %{x8664}
%{__rm} -r lib/ffi/platform/x86_64-linux
%endif
%ifnarch x32
%{__rm} -r lib/ffi/platform/x86_64-linux-gnux32
%endif

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%{__tar} xf %{SOURCE0} metadata.gz

%build
%__gem_helper spec

cd ext/ffi_c
%{__ruby} extconf.rb
%{__make} \
	CC="%{__cc}" \
	ldflags="%{rpmldflags}" \
	optflags="%{rpmcflags} -fPIC"
cd -

%if %{with tests}
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
