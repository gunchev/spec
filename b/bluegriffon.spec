%global nspr_version 4.8.7
%global nss_version 3.12.9
%global cairo_version 1.10
%global freetype_version 2.1.9
%global lcms_version 1.18
%global sqlite_version 3.7.1

%global mozappdir   %{_libdir}/bluegriffon
%global tarballdir  mozilla-2.0

%global gecko_version   2.0.1-1
%global srcversion      4.0.1

Summary:        The next-generation Web Editor
Summary(fr):    La nouvelle génération d'éditeur web
Name:           bluegriffon
Version:        1.1.1
Release:        1
URL:            http://bluegriffon.org/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Editors

Source0:        ftp://ftp.mozilla.org/pub/firefox/releases/%{version}/source/firefox-%{srcversion}.source.tar.bz2

Source1:        %{name}-%{version}.tar.bz2
Source2:        %{name}-l10n-%{version}.tar.bz2

Source10:       %{name}.sh.in
Source11:       %{name}.sh
Source12:       %{name}.desktop

Patch0:         %{name}-1.1.1-build.patch

# Upstream Firefox patches
Patch30:        firefox-4.0-moz-app-launcher.patch
Patch31:        firefox-4.0-gnome3.patch


BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
BuildRequires:  yasm
BuildRequires:  gecko-devel = %{gecko_version}
BuildRequires:	wireless-tools-devel

%if %{fedora} >= 15
%global xulbin xulrunner
%global grecnf gre
%else
%global xulbin xulrunner2
%global grecnf gre2
%endif
Requires:       gecko-libs%{?_isa} = %{gecko_version}

%description
BlueGriffon is a new WYSIWYG content editor for the World Wide Web.

Powered by Gecko, the rendering engine of Firefox 4, it's a modern
and robust solution to edit Web pages in conformance to the latest
Web Standards.

%description -l fr
BlueGriffon est un nouvel éditeur de page web WYSIWYG.

Basé sur Gecko, le moteur de rendu de Firefox 4, c'est une solution
moderne et fiable pour éditer des pages Web conformes aux dernières
normes w3c.


%prep
echo TARGET %{name}-%{version}-%{release}
%setup -q -n %{tarballdir}

tar xjf %{SOURCE1}
tar xjf %{SOURCE2} --directory %{name}

%patch0  -p0 -b .build

# Upstream patches
%patch30 -p1 -b .moz-app-launcher
%patch31 -p1 -b .gnome3


#See http://bluegriffon.org/pages/Build-BlueGriffon
cat <<EOF_MOZCONFIG > .mozconfig 
mk_add_options MOZ_OBJDIR=@TOPSRCDIR@

ac_add_options --enable-application=%{name}

# --with-system-png is disabled because Mozilla requires APNG support in libpng
#ac_add_options --with-system-png
ac_add_options --prefix="\$PREFIX"
ac_add_options --libdir="\$LIBDIR"
ac_add_options --disable-cpp-exceptions
%if %{fedora} >= 15
ac_add_options --enable-system-sqlite
%endif
%if %{fedora} >= 14
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
%endif
%if %{fedora} >= 11
ac_add_options --enable-system-hunspell
%endif
%if %{fedora} >= 15
ac_add_options --enable-system-cairo
%endif
%if %{fedora} >= 10
ac_add_options --enable-libnotify
%else
ac_add_options --disable-libnotify
%endif
%if %{fedora} >= 9
ac_add_options --enable-system-lcms
%endif
%ifarch ppc ppc64
ac_add_options --disable-necko-wifi
ac_add_options --disable-ipc
%endif
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-bz2
ac_add_options --with-pthreads
ac_add_options --disable-strip
ac_add_options --disable-activex
ac_add_options --disable-activex-scripting
ac_add_options --disable-tests
ac_add_options --disable-airbag
ac_add_options --enable-places
ac_add_options --enable-storage
ac_add_options --enable-shared
ac_add_options --disable-static
ac_add_options --disable-mochitest
ac_add_options --disable-installer
ac_add_options --disable-debug
ac_add_options --enable-optimize="\$MOZ_OPT_FLAGS"
ac_add_options --enable-xinerama
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --disable-xprint
ac_add_options --enable-pango
ac_add_options --enable-svg
ac_add_options --enable-canvas
ac_add_options --enable-startup-notification
ac_add_options --disable-javaxpcom
ac_add_options --disable-crashreporter
ac_add_options --enable-safe-browsing
ac_add_options --disable-updater
ac_add_options --enable-gio
ac_add_options --disable-gnomevfs
ac_add_options --enable-libxul
EOF_MOZCONFIG

echo ""  >> .mozconfig
echo "ac_add_options --with-libxul-sdk=\
$(pkg-config --variable=sdkdir libxul)" >> .mozconfig


%build
MOZ_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | \
                     %{__sed} -e 's/-Wall//' -e 's/-fexceptions/-fno-exceptions/g')
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -gt 1 ] && MOZ_SMP_FLAGS=-j$RPM_BUILD_NCPUS

MOZ_APP_DIR=%{_libdir}/%{name}

export LDFLAGS="-Wl,-rpath,${MOZ_APP_DIR}"
make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"


%install
%{__rm} -rf $RPM_BUILD_ROOT

# No Make install for now :(
mkdir -p $RPM_BUILD_ROOT/%{mozappdir}
tar --create --file - --dereference --directory=dist/bin --exclude xulrunner . \
  | tar --extract --file - --directory $RPM_BUILD_ROOT/%{mozappdir}

# Launcher
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
XULRUNNER_DIR=`pkg-config --variable=libdir libxul | %{__sed} -e "s,%{_libdir},,g"`
%{__cat} %{SOURCE10} | %{__sed} -e "s,XULRUNNER_DIRECTORY,$XULRUNNER_DIR,g" \
                     | %{__sed} -e "s,XULRUNNER_BIN,%{xulbin},g" \
		     | %{__sed} -e "s,GRE_CONFIG,%{grecnf},g"  \
  > $RPM_BUILD_ROOT%{_bindir}/%{name}
%{__chmod} 755 $RPM_BUILD_ROOT%{_bindir}/%{name}

# Shortcut
desktop-file-install  \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category Development \
  --add-category Network \
  %{SOURCE12}

# Icons
install -D -m 644  bluegriffon/app/icons/default16.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/default32.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/default48.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/default50.png  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m 644  bluegriffon/app/icons/%{name}128.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# Use the system hunspell dictionaries
%{__rm} -rf $RPM_BUILD_ROOT/%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{mozappdir}/dictionaries

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{mozappdir}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

%changelog
* Tue Mar 20 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 
- Rebuild for Fedora
* Fri Jun 24 2011 Wei-Lun Chao <bluebat@member.fsf.org> - 1.1.1
- Rebuild for OSSII

* Thu Apr 28 2011 Remi Collet <rpms@famillecollet.com> - 1.0-0.2.svn651
- bluegriffon 1.0pre1, svn 651, locales svn 56
- build against xulrunner 2.0.1
- add Gnome3 patch from Firefox

* Sun Apr 17 2011 Remi Collet <rpms@famillecollet.com> - 1.0-0.1.svn635
- bluegriffon 1.0pre1, svn 635, locales svn 47
- build against xulrunner 2.0.1 build1 candidate

* Mon Mar 29 2011 Remi Collet <rpms@famillecollet.com> - 0.9.1-1
- BlueGriffon 0.9.1 "Coffee Overflow"
  http://bluegriffon.org/post/2011/03/29/BlueGriffon-0.9.1-Coffee-Overflow

* Tue Mar 22 2011 Remi Collet <rpms@famillecollet.com> - 0.9.1-0.svn597.1
- rebuild against xulrunnner 2.0

* Sat Mar 19 2011 Remi Collet <rpms@famillecollet.com> - 0.9.1-0.svn597
- bluegriffon svn 597, locales svn 36
- rebuild against xulrunnner 2.0rc2

* Thu Mar 10 2011 Remi Collet <rpms@famillecollet.com> - 0.9-3.svn584
- bluegriffon svn 584, locales svn 33
- rebuild against xulrunnner 2.0rc1

* Sun Mar 06 2011 Remi Collet <rpms@famillecollet.com> - 0.9-3.svn580
- bluegriffon svn 580, locales svn 33

* Mon Feb 28 2011 Remi Collet <rpms@famillecollet.com> - 0.9-2
- rebuild against xulrunnner 2.0b12

* Fri Feb 23 2011 Remi Collet <rpms@famillecollet.com> - 0.9-1.1
- rebuild against xulrunnner 2.0b12 build 1

* Fri Feb 11 2011 Remi Collet <rpms@famillecollet.com> - 0.9-1
- BlueGriffon 0.9 "Cape Town" (svn = 560, locales = 25)
  http://bluegriffon.org/post/2011/02/11/BlueGriffon-0.9-Cape-Town

* Wed Feb 09 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.6.svn554
- bluegriffon svn 554

* Wed Feb 09 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.5.svn553
- bluegriffon svn 553, locales svn 23
- rebuild against xulrunnner 2.0b11

* Sat Feb 05 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.4.svn541
- rebuild

* Fri Feb 04 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.3.svn540
- add stuff to build against system xulrunner2

* Mon Jan 31 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.2.svn540
- split sources
- more patches from Firefox (fix rawhide build)
- add french sumnary/description

* Fri Jan 28 2011 Remi Collet <rpms@famillecollet.com> - 0.9-0.1.hg20110128
- first work on RPM - BlueGriffon 0.9rc1
