%undefine _debugsource_packages

Summary: Macintosh-like Virtual Window Manager
Name: mlvwm
Version: 0.9.1
Release: 1
License: MIT
Group: User Interface/X
Source0: http://www2u.biglobe.ne.jp/~y-miyata/mlvwm/mlvwm091.tar.gz
Source1: http://www2u.biglobe.ne.jp/~y-miyata/mlvwm/mini-icons.tar.gz
URL: http://www2u.biglobe.ne.jp/~y-miyata/mlvwm.html
#URL: https://sourceforge.net/projects/mazewm/
BuildRequires: imake
BuildRequires: libXext-devel
BuildRequires: libXpm-devel

%description
Release of Macintosh-like virtual window manager
(MLVWM). This products is an window manager on X11R6. This window
manager is developed under SunOS 4.1.4 with X11R6. This window manager
needs XPM library and Shape Extension.

%prep
%setup -q -n mlvwm091
sed -i -e 's|$(BINDIR)|%{_bindir}|' -e 's|$(USRLIBDIR)/X11/mlvwm|%{_datadir}/mlvwm|' -e 's|/usr/X11R6/include/pixmaps|%{_datadir}/pixmaps|' configure.h
sed -i -e 's|/usr/local/include/X11/pixmaps:/home2/tak/bin/pixmap|%{_datadir}/pixmaps:%{_datadir}/%{name}|' -e 's|kterm|xterm|' -e 's|mule|emacs|' sample_rc/Mlvwmrc
sed -i 's|-adobe-\*-\*-r-\*-\*-14-\*-\*-\*-p-\*-\*-\*|-misc-*-*-r-*-*-*-*-*-*-p-*-iso10646-1|' mlvwm/mlvwm.h

%build
xmkmf -a
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -s -m755 mlvwm/mlvwm $RPM_BUILD_ROOT%{_bindir}
install -m644 man/mlvwm.man $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
install -m644 pixmap/*.xpm $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m644 sample_rc/Mlvwmrc* $RPM_BUILD_ROOT%{_datadir}/%{name}

tar -zxf $RPM_SOURCE_DIR/mini-icons.tar.gz -C $RPM_BUILD_ROOT%{_datadir}/%{name}/
cd $RPM_BUILD_ROOT%{_datadir}/%{name}/
ln -s Mlvwmrc .mlvwmrc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc CHANGELOG* FAQ.jp README* CONFIGURATION*
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man1/mlvwm.1*

%changelog
* Mon Dec 23 2019 Wei-Lun Chao <bluebat@member.fsf.org> - 0.9.1
- Rebuilt for Fedora
