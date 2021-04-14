Name: unnethack
Version: 5.1.0
Release: 2.1
Summary: An enhancement to the dungeon exploration game NetHack
Source: %name-%version.tar.gz
Group: Games/Adventure
URL: http://sourceforge.net/apps/trac/unnethack/
License: NethackGPL
BuildRequires: flex groff-base gsl-devel ncurses-devel

%description
UnNetHack is a variant of NetHack.

It features more randomness, more levels, more challenges and more fun
than vanilla NetHack.

%prep
%setup -q
sed -i 's/[$](LFLAGS) \(.*\)[$](LIBS)/\1 $(LFLAGS) $(LIBS)/' sys/autoconf/Makefile.src 

%build
export CC="gcc -Wl,--allow-multiple-definition"
LIBS=-lgsl %configure --enable-curses-graphics
make

%install
make install DESTDIR=%buildroot CHOWN=echo CHGRP=echo CHMOD=echo
mv %buildroot%_datadir/unnethack/recover %buildroot%_bindir/recover.bin && ln -s %_bindir/recover.bin %buildroot%_datadir/unnethack/recover
mv %buildroot%_datadir/unnethack/unnethack %buildroot%_bindir/unnethack.bin && ln -s %_bindir/unnethack.bin %buildroot%_datadir/unnethack/unnethack

%files
%doc doc README
%_bindir/*.bin
%_bindir/*[^n]
%_datadir/%name
%_defaultdocdir/%name
%_localstatedir/%name

%changelog
* Sun Feb 22 2015 Wei-Lun Chao <bluebat@member.fsf.org> - 5.1.0
- Rebuilt for Fedora
* Thu Feb 27 2014 Fr. Br. George <george@altlinux.ru> 5.1.0-alt1
- Autobuild version bump to 5.1.0
- Fix build
* Thu Apr 19 2012 Fr. Br. George <george@altlinux.ru> 4.0.0-alt1
- Autobuild version bump to 4.0.0
* Thu Mar 01 2012 Fr. Br. George <george@altlinux.ru> 3.6.1-alt1
- Autobuild version bump to 3.6.1
* Sun Nov 27 2011 Fr. Br. George <george@altlinux.ru> 3.6.0-alt1
- Autobuild version bump to 3.6.0
- Snapshot version corrected manually
- Patchset fix
* Sun Nov 27 2011 Fr. Br. George <george@altlinux.ru> 3.5.3-alt20101010.1
- Initial build from scratch
