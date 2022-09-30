%define kversion %(uname -r)

Name:    r8125
Version: 9.009.02
Release: 1
Group:   System Environment/Kernel
License: GPLv2
Summary: %{name} kernel module(s)
URL:     http://www.realtek.com.tw/
Source0:  %{name}-%{version}.tar.bz2
Source5:  GPL-v2.0.txt
BuildRequires:  kernel-headers
BuildRequires:  kernel-devel

%description
%{name} kernel module.

%package kmod
Summary: Kernel module for Realtek RTL8125 2.5GbE controllers
Requires: kernel = %(uname -r|sed 's/-.*//')

%description kmod
This package provides the %{name} kernel module(s) for Realtek RTL8125 2.5GbE controller.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q
%{__cp} -a %{SOURCE5} .
echo "blacklist r8169" > blacklist-r8125.conf

%build
KSRC=%{_usrsrc}/kernels/%{kversion}
%{__make} -C "${KSRC}" %{?_smp_mflags} modules M=$PWD/src

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{name}/
%{__install} src/%{name}.ko %{buildroot}/lib/modules/%{kversion}/extra/%{name}/
%{__install} -d %{buildroot}%{_prefix}/lib/modprobe.d/
%{__install} blacklist-r8125.conf %{buildroot}%{_prefix}/lib/modprobe.d/
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

%post
depmod -a > /dev/null 2> /dev/null

%postun
depmod -a > /dev/null 2> /dev/null

%clean
%{__rm} -rf %{buildroot}

%files kmod
%doc GPL-v2.0.txt README
/lib/modules/%{kversion}/extra/r8125/r8125.ko
/usr/lib/modprobe.d/blacklist-r8125.conf

%changelog
* Sun Sep 25 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 9.009.02
- Update to new version
* Thu Jun 12 2014 Alan Bartlett <ajb@elrepo.org> - 8.038.00-1
- Updated to version 8.038.00
* Thu Jun 12 2014 Alan Bartlett <ajb@elrepo.org> - 8.037.00-3
- Updated to the GA RHEL7 base kernel.
* Fri May 23 2014 Philip J Perry <phil@elrepo.org> - 8.037.00-2
- Fix blacklist location.
- Corrected the kmodtool file.
* Tue Jan 14 2014 Alan Bartlett <ajb@elrepo.org> - 8.037.00-1
- Initial el7 build of the kmod package.
