%undefine _debugsource_packages

Summary: Virtual console hex editor
Name: vche
Version: 1.7.2
Release: 5.1
License: GPL
Group: Applications/Editors
URL: http://www.grigna.com/diego/linux/vche/
Source: http://www.grigna.com/diego/linux/vche/vche-%{version}.tar.gz

%description
vche is an ncurses hex editor that lets you edit hard drives, cdroms, RAM,
and everything else that can be read.

%prep
%setup -q
%{__perl} -pi.orig -e 's|-[og] root ||g;' src/Rules.make
sed -i 's|-Wall|-Wall -Wl,--allow-multiple-definition|' src/Rules.make

%build
%{__make} -C src %{?_smp_mflags}

%install
%{__install} -d -m0755 %{buildroot}%{_bindir}
%{__install} -d -m0755 %{buildroot}%{_mandir}/man1/
%{__install} -d -m0755 %{buildroot}%{_mandir}/man5/
%{__make} -C src install BASEDIR="%{buildroot}%{_prefix}" \
    MANDIR1="%{buildroot}%{_mandir}/man1" \
    MANDIR5="%{buildroot}%{_mandir}/man5" \
    LIBDIR="%{buildroot}%{_sysconfdir}"
%{__install} -Dp -m0644 doc/vche.conf %{buildroot}%{_sysconfdir}/vche.conf
sed -i 's|%{buildroot}||' %{buildroot}%{_mandir}/man?/vche*

%files
%doc doc/Changelog doc/COPYING doc/CREDITS doc/INSTALL doc/LSM doc/README doc/vche.conf
%doc %{_mandir}/man1/vche.1*
%doc %{_mandir}/man1/vche-nc.1*
%doc %{_mandir}/man1/vche-raw.1*
%doc %{_mandir}/man5/vche.conf.5*
%config %{_sysconfdir}/vche.conf
%{_bindir}/vche
%{_bindir}/vche-nc
%{_bindir}/vche-raw

%changelog
* Mon Jan 13 2014 Wei-Lun Chao <bluebat@member.fsf.org> - 1.7.2
- Rebuilt for Fedora
* Sun Nov 09 2008 Dag Wieers <dag@wieers.com> - 1.7.2-1 - +/
- Initial package. (using DAR)
