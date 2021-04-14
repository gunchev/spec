%undefine _debugsource_packages

Name: 		ede
Version: 	2.0
#Version: 	2.1
Release: 	14.9
Source: 	%{name}-%{version}.tar.gz
Summary:	Core programs for the Equinox Desktop Environment
URL: 		http://ede.sourceforge.net/
License: 	GPL
Group: 		Graphical desktop/Other
BuildRequires: fltk13-devel
BuildRequires: gcc-c++, jam, edelib-devel, libpng-devel, libjpeg-devel
BuildRequires: python, libxkbfile-devel, libXext-devel, libXpm-devel
Requires: pekwm

%description
Equinox Desktop Environment (EDE) is desktop environment - the piece of
software that enables you to launch applications in a convenient way,
show what windows you have opened, manages icons and background of your
desktop, etc. This core package provides panel with tasklist, clock,
load status; icon manager that take care of your icons on background,
control panel for easy access to your settings, sound volume control, 
color configuration, panel configuration, menu editor, icons configuration, 
tips, time/date and timezone configuration, fast file search tool and of 
course window manager that manages your windows with config utility.

%prep
%setup -q
sed -i 's|/usr/bin/env python|/usr/bin/python2|' doc/asciidoc/asciidoc.py

%build
sed -i -e 's|-lstdc++|"-lstdc++ -lm -ldl -lX11 -lXext -lpng16"|' -e 's|-Wall|-Wall -Wno-narrowing|' Jamconfig.in
%configure
make prefix=$RPM_BUILD_ROOT%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall docdir=$RPM_BUILD_ROOT%{_datadir}/doc
cd %{buildroot}
rm -rf usr/bin/pekwm etc/pekwm/config etc/pekwm/keys etc/pekwm/menu etc/pekwm/mouse etc/pekwm/start
rm -rf usr/share/pekwm/scripts/pekwm_themeset.sh
rm -rf usr/share/pekwm/themes/default/menuline.png usr/share/pekwm/themes/default/theme usr/share/pekwm/themes/default/title.png
for i in $RPM_BUILD_ROOT%{_datadir}/applications/*
do
echo 'OnlyShowIn=EDE;' >> $i
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/*
%{_datadir}/desktop-directories/*
%{_datadir}/ede
%{_datadir}/doc/*
%{_datadir}/icons/*
%{_datadir}/mime/packages/*
%{_datadir}/pekwm
%{_datadir}/wallpapers/*
%{_datadir}/xsessions/*
%{_sysconfdir}/pekwm
%{_sysconfdir}/xdg/ede
%{_sysconfdir}/xdg/menus/*

%changelog
* Mon May 28 2012 Wei-Lun Chao <bluebat@member.fsf.org> - 2.0
- Rebuilt for Fedora
*  Mon Jan 31 2005 Vedran Ljubovic <vljubovic@smartnet.ba> 1.0.2-1ede
- new build system in EDE
- Better distro-independance
- Patches merged upstream
*  Fri Dec 17 2004 Vedran Ljubovic <vljubovic@smartnet.ba> 1.0.1.1-2
- Patch for GCC 3.4 and a possible typo
- Fix for prefix to make (code uses it and so a bunch of stuff doesn't work)
- Remove locale (doesn't seem to get made?)
- Some mandrake specific stuff
*  Thu Jan 01 2004 nobody <nobody@nobody> 1.0.1.1-1
- Initial autogenerated release
