Name:		cyberprobe
Version:	2.5.2
Release:	1
Summary:	Distrbuted real-time monitoring of networks against attack.
Group:		Applications/Internet
License:	GPLv3
URL:		https://cybermaggedon.github.io/cyberprobe-docs/
Source:		%{name}-%{version}.tar.gz
BuildRequires:  libpcap-devel

%description
The Cyberprobe project is a distrbuted architecture for real-time
monitoring of networks against attack.  The software consists of two components:
- a probe, which collects data packets and forwards it over a network in
standard streaming protocols.
- a monitor, which receives the streamed packets, decodes the protocols,
and interprets the information.

These components can be used together or separately.  For a simple
configuration, they can be run on the same host, for more complex environments,
a number of probes can feed a single monitor.

Please see documentation in /usr/share/doc/cyberprobe.
%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
%make_install

%post
ln -sf %{_docdir}/cyberprobe/cyberprobe-overview.png ${RPM_BUILD_ROOT}%{_infodir}/cyberprobe-overview.png
ln -sf %{_docdir}/cyberprobe/kibana-scaled.png ${RPM_BUILD_ROOT}%{_infodir}/kibana-scaled.png
ln -sf %{_docdir}/cyberprobe/architecture-small.png ${RPM_BUILD_ROOT}%{_infodir}/architecture-small.png
%systemd_post cyberprobe.service cybermon.service

%preun
%systemd_preun cyberprobe.service cybermon.service

%postun
%systemd_postun_with_restart cyberprobe.service cybermon.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%exclude /usr/share/info/dir
%doc /usr/share/doc/cyberprobe
%doc /usr/share/info/
%doc /usr/share/man
/etc/cyberprobe/*.lua
/etc/cyberprobe/util/*.lua
%config /etc/cyberprobe.cfg
/usr/bin/*
/usr/lib/python3.*/site-packages/cyberprobe
%{_libdir}/lib*
/usr/lib/systemd/system/cyberprobe.service
/usr/lib/systemd/system/cybermon.service
/usr/lib/systemd/system/evs-detector.service
/usr/lib/systemd/system/evs-cassandra.service
/usr/lib/systemd/system/evs-elasticsearch.service
/usr/lib/systemd/system/evs-gaffer.service
/usr/lib/systemd/system/evs-geoip.service

%changelog
* Sun Dec 12 2021 Wei-Lun Chao <bluebat@member.fsf.org> - 2.5.2
- Rebuilt for Fedora
