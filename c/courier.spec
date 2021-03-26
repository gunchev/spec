#
# Copyright 1998 - 2014 Double Precision, Inc.  See COPYING for
# distribution information.
#

# --- Build behavior defines --------------------------------------------------

%{?_without_fax:    %define with_fax 0}
%{!?_without_fax:   %define with_fax 1}

%{?_without_fam:    %define with_fam 0}
%{!?_without_fam:   %define with_fam 1}

%define _missing_doc_files_terminate_build 1
%define _unpackaged_files_terminate_build 1

%define alternatives %(test -x /usr/sbin/alternatives && echo 1 || echo 0)
%define is_not_mandrake %(test ! -e /etc/mandrake-release && echo 1 || echo 0)

%define using_systemd %(test -d /etc/systemd && echo 1 || echo 0)

%if 0%{!?dist:1}
%if %is_not_mandrake
%define courier_release %(release="`rpm -q --queryformat='.%{VERSION}' redhat-release 2>/dev/null`" ; if test $? != 0 ; then release="`rpm -q --queryformat='.%{VERSION}' fedora-release 2>/dev/null`" ; if test $? != 0 ; then release="" ; fi ; fi ; echo "$release")
%else
%define courier_release mdk
%endif
%else
%define courier_release %{nil}
%endif

%define configure CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ; CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ; FFLAGS="${FFLAGS:-%optflags}" ; export FFLAGS ;  ./configure %{?gpg_option} --host=%{_host} --build=%{_build} --target=%{_target_platform} --program-prefix=%{?_program_prefix} --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} --sharedstatedir=%{_sharedstatedir} --mandir=%{_mandir} --infodir=%{_infodir}


#
#  RH custom locations.
#
#                <7.X               7.x
#  manpages      /usr/man           /usr/share/man
#  httpd         /home/httpd        /var/www
#  initscripts   /etc/rc.d/init.d   /etc/init.d

%{expand:%%define manpagedir %(if test -d %{_prefix}/share/man ; then echo %{_prefix}/share/man ; else echo %{_prefix}/man ; fi)}

%{expand:%%define apacheinstdir %(if test -d /home/httpd ; then echo /home/httpd ; else echo /var/www ; fi)}

%define	_prefix				/usr/lib/courier
%define _localstatedir			/var/spool/courier
%define	_sysconfdir			/etc/courier
%define	_mandir				%{manpagedir}

%define initdir %(if test -d /etc/init.d/. ; then echo /etc/init.d ; else echo /etc/rc.d/init.d ; fi)

# Change the following if your DocumentRoot and cgibindir differ.  This is
# the default redhat build:

%define	apache_cgibindir		%{apacheinstdir}/cgi-bin
%define apache_documentroot		%{apacheinstdir}/html

# -----------------------------------------------------------------------------

Summary:          Courier 0.78.2 mail server
Name:             courier
Version:          0.78.2
Release:          1%{?dist}%{courier_release}

Group:            Applications/Mail
License:          GPL
URL:              http://www.courier-mta.org
Packager:         %{PACKAGER}
Source:           http://download.sourceforge.net/courier/courier-0.78.2.tar.bz2
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:         smtpdaemon server(smtp)
Provides:         config(courier) = %{version}-%{release}
AutoProv:         no

%if %using_systemd
Requires(post):   systemd
Requires(postun):   systemd
Requires(preun):  systemd
%define initscript_courier %{nil}
%else
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/chkconfig
Requires(postun): /sbin/service
%define initscript_courier --initscript courier
%endif

Requires:         fileutils
%if %alternatives
Obsoletes:        courier-sendmail-wrapper
Provides:         /usr/sbin/sendmail /usr/bin/mailq /usr/bin/rmail /usr/bin/newaliases
%endif

BuildRequires:	  courier-authlib-devel >= 0.55
BuildRequires:    rpm >= 4.0.2
BuildRequires:    fileutils
BuildRequires:    binutils
BuildRequires:    sed
BuildRequires:    gawk
BuildRequires:    perl
BuildRequires:    make
BuildRequires:    procps-ng
%{?_with_gpg2:  %define with_gpg2 1}
%{!?_with_gpg2: %define with_gpg2 0}

%if %with_gpg2
BuildRequires: gnupg2
Requires: gnupg2
%define gpg_option --with-gpg2
%else
BuildRequires: gnupg >= 1.0.5
Requires: gnupg >= 1.0.5
%endif
BuildRequires:    expect
BuildRequires:    gdbm-devel
BuildRequires:    pam-devel
BuildRequires:	  libidn-devel
BuildRequires:    courier-unicode-devel
%if %with_fam
BuildRequires:      /usr/include/fam.h
%endif
BuildRequires:	  perl(ExtUtils::Embed)
BuildRequires:	  /etc/mime.types

%define use_openssl %(rpm -q openssl-devel >/dev/null 2>&1 && echo 1 && exit 0; echo 0)

%if %use_openssl
BuildRequires:      openssl
BuildRequires:      openssl-devel
%if %is_not_mandrake
BuildRequires:      openssl-perl
%endif
%else
BuildRequires:      libgcrypt-devel gnutls-devel /usr/bin/certtool
Requires:	  /usr/bin/certtool
%endif

%if %with_fax
BuildRequires:      groff
BuildRequires:      ghostscript
BuildRequires:      mgetty-sendfax
BuildRequires:      netpbm-progs
%endif
BuildRequires:      pcre-devel
Obsoletes:	courier-smtpauth

%define need_perl_generators %(if rpm -q fedora-release >/dev/null 2>/dev/null; then echo "1"; exit 0; fi; echo "1"; exit 1)

%if %need_perl_generators
BuildRequires: perl-generators
%endif

%if ! %alternatives
%package sendmail-wrapper
Summary: Courier 0.78.2 soft links for sendmail
Group: Applications/Mail
%endif

%package ldap
Summary: Courier 0.78.2 LDAP modules and configuration screen
Group: Application/Mail

%package mysql
Summary: Courier 0.78.2 MySQL configuration screen
Group: Application/Mail

%package pgsql
Summary: Courier 0.78.2 PostgreSQL configuration screen
Group: Application/Mail

%package pop3d
Summary: Courier 0.78.2 Integrated POP3 server
Group: Applications/Mail
Requires: courier = 0.78.2 fileutils

%package imapd
Summary: Courier 0.78.2 Integrated IMAP server
Group: Applications/Mail
Requires: courier = 0.78.2 fileutils

%package webmail
Summary: Courier 0.78.2 Integrated HTTP (webmail) server
Group: Applications/Mail
Requires: courier = 0.78.2 %{apache_documentroot} /etc/cron.hourly
%if %with_gpg2
Requires: gnupg2
%define gpg_option --with-gpg2
%else
Requires: gnupg >= 1.0.5
%endif
%if %is_not_mandrake
Requires: %{apache_cgibindir}
%endif

%package webadmin
Summary: Courier 0.78.2 web-based administration tool
Group: Applications/Mail
Requires: courier = 0.78.2 %{apache_documentroot}
%if %is_not_mandrake
Requires: %{apache_cgibindir}
%endif

%package mlm
Summary: Courier 0.78.2 Integrated Mailing List Manager
Group: Applications/Mail
Requires: courier = 0.78.2

%package mlm-web
Summary: Courier 0.78.2 Integrated web-based mailing list interface
Group: Applications/Mail
Requires: courier-mlm = 0.78.2 %{apache_documentroot}
%if %is_not_mandrake
Requires: %{apache_cgibindir}
%endif

%package maildrop
Summary: Courier 0.78.2 Integrated mail filter
Group: Applications/Mail
Requires: courier = 0.78.2

%package fax
Summary: Courier 0.78.2 fax support
Group: Application/Mail
Requires: courier = 0.78.2 groff ghostscript netpbm-progs mgetty-sendfax

%package maildrop-wrapper
Summary: Courier 0.78.2 soft links for maildrop
Group: Applications/Mail
Requires: courier-maildrop = 0.78.2

%description
The Courier mail transfer agent (MTA) is an integrated mail/groupware
server based on open commodity protocols, such as ESMTP, IMAP, POP3, LDAP,
SSL, and HTTP. Courier provides ESMTP, IMAP, POP3, webmail, and mailing list
services within a single, consistent, framework.  Individual components can
be enabled or disabled at will. Courier now implements basic web-based
calendaring and scheduling services integrated in the webmail module.
Advanced groupware calendaring services will follow soon.

After installing this RPM, additional information regarding configuring
and using courier can be found in %{_defaultdocdir}.

Particularly, README.REDHAT describes where everything is installed, and
install.html contains the regular installation instructions, which includes
configuration information.  In particular, the courier-webadmin package
will contain the web-based configuration tool, webadmin.  After installing
apache and courier-webadmin, and using the webadmin password
in %{_sysconfdir}/webadmin/password (which is initialized to a random string
by default), you will be able to configure Courier using any web browser.

Available rpmbuild rebuild options:
--without : fax

%if ! %alternatives
%description sendmail-wrapper
This package contains two soft links from /usr/sbin/sendmail and
/usr/lib/sendmail to %{_bindir}/sendmail.  This allows application
that use sendmail to transparently use Courier for sending mail.
%endif

%description pop3d
This package adds POP3 server access to the Courier mail server.
Courier's POP3 server can only be used to access maildir mailboxes.
This server does not support mailbox files.  If you do not need the
ability to download mail with a POP3 client, you do not need to install
this package.

%description imapd
This package adds IMAP server access to the Courier mail server.
Courier's IMAP server can only be used to access maildir mailboxes.
This server does not support mailbox files.  If you do not need the
ability to access mail with an IMAP client, you do not need to install
this package.

This is a different package than the standalone version of the
Courier IMAP server.  You cannot install both this package, and the
standalone version, called "Courier-IMAP".  If you have the standalone
version already installed, installing this package will automatically
remove the standalone version.

%description webmail
This package adds webmail access to the Courier mail server.  Webmail
access is provided via a CGI module that is installed in the apache's
cgi-bin directory.  You must have apache installed.

%description mlm-web
This package installs the web-based mini-interface to the Courier
mailing list manager.  The web access is provided via a CGI module that
is installed in the apache's cgi-bin directory.  You must have apache
installed.

%description webadmin
This package install the web-based administration tool for the Courier
mail server.  The webadmin tool allows the most common administrative
tasks to be done from any web browser.

After installing this tool, initialize %{_sysconfdir}/webadmin/password
to contain the administrative password.
The default configuration permits non-SSL access only from the same server,
and all external logins must use SSL.  See the installation notes
for information on enabling external non-SSL access.

%description fax
This package adds support for faxing E-mail messages.  You need to install
this package if you want the ability to send fax messages simply by
Sending an E-mail to phonenumber@fax.

%description maildrop
This package adds mail filtering abilities to Courier.  Mail filtering
is provided via a customized version of the maildrop mail filter.

You need to install this package if you want the ability to filter
incoming mail.
%description mlm
This package installs couriermlm - a mailing list manager for the
Courier mail server.  If you do not need the ability to manage
mailing lists, you do not need to install this package.

couriermlm is used to set up, maintain, and run a mailing list.
couriermlm automatically processes subscription and unsubscription
requests, and removes undeliverable addresses from the subscription
rolls.  Mailing lists managed by couriermlm require zero human
administrative oversight. couriermlm supports digests, write-only
posting aliases, and moderated mailing lists.

%description maildrop-wrapper
This package installs several soft links from the /usr/local/bin
directory to Courier's integrated maildrop mail filter.  Maildrop is
available as a standalone package, which installs in /usr/local/bin.
If you have applications that expect to find maildrop in /usr/local/bin
you can install this package to create soft links that point to
Courier's integrated maildrop version instead, in order to continue
to use those applications, without needing to reconfigure them.

%description ldap
This package contains LDAP modules and the webadmin configuration screen
for Courier.

%description mysql
This package contains the webadmin MySQL configuration screen for Courier.

%description pgsql
This package conains the webadmin PostgreSQL configuration screen for Courier.

# -----------------------------------------------------------------------------

%prep
%setup -q

rm -f courier.config.cache
PATH=/usr/bin:$PATH %configure --cache-file=courier.config.cache %{?xflags: %{xflags}}

%{__cat} >README.REDHAT <<EOF

This installation of Courier is configured as follows:

Installation directory:          %{_prefix}
Binary installation directory:   %{_exec_prefix}
Binaries:                        %{_bindir}
Superuser binaries:              %{_sbindir}
Program executables:             %{_libexecdir}
Configuration files:             %{_sysconfdir}
Scripts, other non-binaries:     %{_datadir}
Mail queue, temporary files:     %{_localstatedir}
Manual pages:                    %{_mandir}

EOF

# -----------------------------------------------------------------------------

%build
LANG=C
export LANG
umask 022
%{__make} -s %{_smp_mflags}
%{__make} check
%install
LANG=C
export LANG

umask 022
test "$RPM_BUILD_ROOT" != "" && rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_prefix}
%{__mkdir_p} $RPM_BUILD_ROOT/etc/pam.d

%{__make} -s install DESTDIR=$RPM_BUILD_ROOT

%{__install} -m 0444 libs/imap/imapd.pam $RPM_BUILD_ROOT/etc/pam.d/pop3
%{__install} -m 0444 courier/module.esmtp/esmtp.authpam $RPM_BUILD_ROOT/etc/pam.d/esmtp
%{__install} -m 0444 libs/imap/pop3d.pam $RPM_BUILD_ROOT/etc/pam.d/imap
%{__install} -m 0444 libs/sqwebmail/webmail.authpam $RPM_BUILD_ROOT/etc/pam.d/webmail
%{__install} -m 0444 libs/sqwebmail/webmail.authpam $RPM_BUILD_ROOT/etc/pam.d/calendar
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/*.authpam

# Create permissions.dat

%{__make} install-perms

#
# We're going to create some more config files later, so let's just make
# sure they're processed as all other Courier config files
#

echo '/etc/profile.d/courier.sh 755 bin bin config' >>permissions.dat
echo '/etc/profile.d/courier.csh 755 bin bin config' >>permissions.dat
%if %using_systemd
echo '%{_datadir}/courier.sysvinit 755 bin bin' >>permissions.dat
echo '%{_unitdir}/courier.service 644 root root' >>permissions.dat
%else
echo '%{initdir}/courier 755 bin bin config' >>permissions.dat
%endif

#
#  Translate permissions.dat to spec file format
#

%{__perl} -e '
$buildroot=$ENV{"RPM_BUILD_ROOT"};
$prefix="%{_prefix}";
$exec_prefix="%{_exec_prefix}";

while (<>)
{
	chop if /\n$/;
	my ($file,$mode,$uid,$gid,$special)=split(/ +/);
	$file=$prefix if $file eq "$prefix/.";

	next if $special eq "doc";
	next if $file eq "$prefix/doc";

	# Ignore dir/. entries

	next if $file =~ /\/\.$/;

	# Ignore man directories

	next if $file eq "%{_mandir}";
	next if substr($file, 0, length("%{_mandir}")) eq "%{_mandir}"
		&& substr($file, length("%{_mandir}")) =~ /^\/man[1-9]$/;

	$mode = "-" if $special eq "%doc";
	$special="%config" if $special eq "config";
	$special="%dir" if ! -l "$buildroot/$file" && -d "$buildroot/$file";

	my $islink = -l "$ENV{RPM_BUILD_ROOT}/$file";

	$file .= ".*" if $special eq "man";	# For brp-compress

	$special="" unless $special =~ /%/;

	$special="%attr($mode, $uid, $gid) $special" unless $islink;

	print "$special $file\n";
}

' <permissions.dat >filelist1 || exit 1

############################################################################
#
# Break up a single filelist into multiple packages right here.  This is
# going to be ugly.
#

%{__sed} -n '/imap[\.a-z0-9]*$/p;/imapd-ssl/p' <filelist1 | grep -v authpam >filelist.imap
%{__sed} -n '/pop3[\.a-z0-9]*$/p;/pop3d-ssl/p' <filelist1 | grep -v authpam >filelist.pop3
%{__sed} -n '/couriermlm/p' <filelist1 >filelist.mlm
%{__sed} -n '/webmlmd/p' <filelist1 >filelist.webmlm
%{__sed} -n '/maildrop[^/]*$/p;/mailbot/p;/reformail[^/]*$/p' <filelist1 >filelist.maildrop

%{__sed} -n '/15ldap/p;/ldapsearch/p;/courierldapalias/p' <filelist1 >filelist.ldap

%{__sed} -n '/15mysql/p' <filelist1 >filelist.mysql

%{__sed} -n '/15pgsql/p' <filelist1 >filelist.pgsql

%{__sed} -n '/faxmail/p;/35fax/p;/34fax/p' <filelist1 >filelist.fax

%{__mkdir_p} $RPM_BUILD_ROOT/etc/mgetty+sendfax
%{__ln_s} %{_datadir}/faxmail/new_fax $RPM_BUILD_ROOT/etc/mgetty+sendfax/new_fax

%if ! %with_fax
awk '{print $NF}' filelist.fax |
while read file; do
    rm -f $RPM_BUILD_ROOT$file
done
rm -f $RPM_BUILD_ROOT/etc/mgetty+sendfax/new_fax
%endif

# Delete all of the above, AND ldapaddressbook+webmail from the filelist.
# Do not install esmtp.authpam, taken care of elsewhere.
# Do not install htmldoc, taken care of elsewhere

%{__sed} '/imap[\.a-z0-9]*$/d;/imapd-ssl/d;/pop3[\.a-z0-9]*$/d;/pop3d-ssl/d;/couriermlm/d;/webmail/d;/webmlm/d;/authsystem\.passwd/d;/ldapsearch$/d;/ldapaddressbook.dist$/d;/pcpd/d;/calendar/d;/maildrop[^/]*$/d;/mailbot/d;/reformail[^/]*$/d;/15ldap/d;/47webmail/d;/courierldapalias/d;/15mysql/d;/15pgsql/d;/faxmail/d;/35fax/d;/34fax/d;/esmtp\.authpam/d;/htmldoc/d' <filelist1 >filelist


%{__sed} -n '/47webmail/p;/sqwebmail/p;/sqwebpasswd/p;/authsystem\.passwd/p;/webmail-logincache/p;/ldapaddressbook.dist$/p;/pcpd/p;/calendar/p' <filelist1 | sed '/images/d' | sort | uniq >filelist.webmail
echo "%attr(755, root, bin) %{_sbindir}/webmaild" >>filelist.webmail

# Note that we delete all 'webmail's, but extract only 'sqwebmail's.
# This removes all webmail-related stuff from the main filelist,
# and adds everything except the executable, webmail, to filelist.webmail.
# Here's why, we move the webmail binary directly into the cgibindir.

%{__mkdir_p} $RPM_BUILD_ROOT%{apache_cgibindir}
%{__cp} $RPM_BUILD_ROOT%{_libexecdir}/courier/webmail/webmail \
	$RPM_BUILD_ROOT%{apache_cgibindir}/webmail
%{__cp} $RPM_BUILD_ROOT%{_libexecdir}/courier/webmail/webadmin \
	$RPM_BUILD_ROOT%{apache_cgibindir}/webadmin
%{__cp} $RPM_BUILD_ROOT%{_libexecdir}/courier/webmail/webmlm \
	$RPM_BUILD_ROOT%{apache_cgibindir}/webmlm
rm -rf $RPM_BUILD_ROOT%{_libexecdir}/courier/webmail

# Remove the webadmin wrapper from filelist (but keep all html and pl files
# there.

%{__sed} '/courier\/webmail\/webadmin /d' <filelist >filelist.tmp
%{__mv} filelist.tmp filelist

# For the same reason we delete all images from filelist.webmail:

%{__mkdir_p} $RPM_BUILD_ROOT%{apache_documentroot}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/sqwebmail/images $RPM_BUILD_ROOT%{apache_documentroot}/webmail

# Do we need to install a cron job to clean out webmail's cache?

if test -f libs/sqwebmail/cron.cmd
then
	%{__mkdir_p} $RPM_BUILD_ROOT/etc/cron.hourly
	%{__cat} >$RPM_BUILD_ROOT/etc/cron.hourly/courier-webmail-cleancache <<EOF
#!/bin/sh

su - bin -s /bin/sh -c %{_datadir}/sqwebmail/cleancache.pl
EOF

	echo "%attr(555, root, bin) /etc/cron.hourly/courier-webmail-cleancache" >>filelist.webmail
fi

#
# Move .html documentation back to build dir, so that RPM will move it to
# the appropriate docdir
#

%{__rm} -rf htmldoc
%{__mkdir} htmldoc
%{__chmod} 755 htmldoc
%{__cp} $RPM_BUILD_ROOT%{_datadir}/htmldoc/* htmldoc
%{__chmod} a-wx htmldoc/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/htmldoc

#
# Update /etc/skel

%{__mkdir_p} $RPM_BUILD_ROOT/etc/skel
libs/maildir/maildirmake $RPM_BUILD_ROOT/etc/skel/Maildir

############################################################################
#
# Some configuration file tweaking.
#
# Manually set POP3DSTART and IMAPDSTART to yes, they'll go into a separate
# package, so after it's installed they should be runnable.

%{__sed} 's/^POP3DSTART.*/POP3DSTART=YES/' <$RPM_BUILD_ROOT%{_sysconfdir}/pop3d.dist >$RPM_BUILD_ROOT%{_sysconfdir}/pop3d.new
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/pop3d.new $RPM_BUILD_ROOT%{_sysconfdir}/pop3d.dist

%{__sed} 's/^POP3DSSLSTART.*/POP3DSSLSTART=YES/' <$RPM_BUILD_ROOT%{_sysconfdir}/pop3d-ssl.dist >$RPM_BUILD_ROOT%{_sysconfdir}/pop3d-ssl.new
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/pop3d-ssl.new $RPM_BUILD_ROOT%{_sysconfdir}/pop3d-ssl.dist

%{__sed} 's/^IMAPDSTART.*/IMAPDSTART=YES/' <$RPM_BUILD_ROOT%{_sysconfdir}/imapd.dist >$RPM_BUILD_ROOT%{_sysconfdir}/imapd.new
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/imapd.new $RPM_BUILD_ROOT%{_sysconfdir}/imapd.dist

%{__sed} 's/^IMAPDSSLSTART.*/IMAPDSSLSTART=YES/' <$RPM_BUILD_ROOT%{_sysconfdir}/imapd-ssl.dist >$RPM_BUILD_ROOT%{_sysconfdir}/imapd.new-ssl
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/imapd.new-ssl $RPM_BUILD_ROOT%{_sysconfdir}/imapd-ssl.dist

# Convenient init file.

%if %using_systemd
%{__cp} courier.sysvinit $RPM_BUILD_ROOT%{_datadir}/courier.sysvinit

%{__mkdir_p} $RPM_BUILD_ROOT%{_unitdir}
%{__cp} courier.service $RPM_BUILD_ROOT%{_unitdir}
%else
%{__mkdir_p} $RPM_BUILD_ROOT%{initdir}
%{__cp} courier.sysvinit $RPM_BUILD_ROOT%{initdir}/courier
%endif

# Create an initial default DH paramter file, and install a
# monthly script to generate DH parameters

cat >$RPM_BUILD_ROOT/%{_datadir}/dhparams.pem.dist <<ZZ
This file contains default DH parameters for initial use on a new
installation. The startup script copies this file to dhparams.pem,
unless it already exists.

ZZ

sed 's/^chown/echo/' <libs/imap/mkdhparams >libs/imap/mkdhparams.tmp
TLS_DHPARAMS=$RPM_BUILD_ROOT/%{_datadir}/dhparams.pem.dist.tmp %{__spec_rmbuild_shell} libs/imap/mkdhparams.tmp
rm -f libs/imap/mkdhparams.tmp
cat $RPM_BUILD_ROOT/%{_datadir}/dhparams.pem.dist.tmp >>$RPM_BUILD_ROOT/%{_datadir}/dhparams.pem.dist
rm -f $RPM_BUILD_ROOT/%{_datadir}/dhparams.pem.dist.tmp
courier/courier-config | grep '^mail' >uidgid
. ./uidgid
rm -f uidgid
echo "%attr(600, $mailuser, $mailgroup) %{_datadir}/dhparams.pem.dist" >>filelist

%{__mkdir_p} $RPM_BUILD_ROOT/etc/cron.monthly
%{__ln_s} %{_sbindir}/mkdhparams $RPM_BUILD_ROOT/etc/cron.monthly/courier-mkdhparams
echo "/etc/cron.monthly/courier-mkdhparams" >>filelist

#
# Make up some /etc/profile.d scripts
#

%{__mkdir_p} $RPM_BUILD_ROOT/etc/profile.d
%{__cat} >$RPM_BUILD_ROOT/etc/profile.d/courier.sh <<EOF
case :\${PATH}: in
	*:%{_bindir}:*)
		;;
	*)
		if test \`id -u\` = 0
		then
			PATH="%{_sbindir}:\$PATH"
		fi
		PATH="%{_bindir}:\$PATH"
		export PATH
		;;
esac
EOF

%{__cat} >$RPM_BUILD_ROOT/etc/profile.d/courier.csh <<EOF
switch (:\${PATH}:)
	case *:%{_bindir}:*:
		breaksw
	default:
		test \`id -u\` = 0
		if ( \$? == 0 ) then
			setenv PATH "%{_sbindir}:\$PATH"
		endif
		setenv PATH "%{_bindir}:\$PATH"
		breaksw
endsw
EOF

#
# Create sendmail soft links manually.
#

%{__mkdir_p} $RPM_BUILD_ROOT/usr/sbin
%{__mkdir_p} $RPM_BUILD_ROOT/usr/lib
%{__mkdir_p} $RPM_BUILD_ROOT/usr/bin


%if %alternatives
	%{__ln_s} ../sbin/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail
	%{__ln_s} ../sbin/sendmail $RPM_BUILD_ROOT/usr/bin/sendmail
%else

# Old fashioned stuff

	cat >filelist.sendmail-wrapper <<EOF
%attr(-, root, root) /usr/sbin/sendmail
%attr(-, root, root) /usr/bin/sendmail
%attr(-, root, root) /usr/lib/sendmail
EOF

	%{__ln_s} %{_bindir}/sendmail $RPM_BUILD_ROOT/usr/sbin/sendmail
	%{__ln_s} %{_bindir}/sendmail $RPM_BUILD_ROOT/usr/lib/sendmail
	%{__ln_s} %{_bindir}/sendmail $RPM_BUILD_ROOT/usr/bin/sendmail
%endif

#
# maildrop wrapper soft links (value added for the RPM)
#

%{__mkdir_p} $RPM_BUILD_ROOT/usr/local/bin

for f in maildirmake maildrop makedat reformail reformime mimegpg deliverquota
do
	%{__ln_s} %{_bindir}/$f $RPM_BUILD_ROOT/usr/local/bin/$f
done

#
# The following directories are not created by default, but I want them here.
#

. courier/uidgid || exit 1

#####################
##
## sysconftool support.  Instead of doing make install-configure, grab all
## the %config .dists from the filelists, and arrange to run sysconftool in
## the postinstallation scripts.  This is done by saving the .dists into
## a file that's included in the installation package.  sysconftool is also
## added to the installation package, and we run the whole thing from
## %post-s.

for f in filelist filelist.pop3 filelist.imap filelist.webmail
do
	ff=`echo $f | %{__sed} 's/filelist/configlist/'`

	%{__perl} -e '
		while (<>)
		{
			chop;
			next unless /\%config.* (.*\.dist)$/;
			print "$1\n";
		} ' < $f >$RPM_BUILD_ROOT/%{_datadir}/$ff
done

%{__cp} sysconftool $RPM_BUILD_ROOT%{_datadir}/sysconftool

cat <<ZZ >>filelist.webmail
%%attr(555, root, bin) %{apache_cgibindir}/webmail
%%attr(644, root, root) %%config(noreplace) /etc/pam.d/webmail
%%attr(644, root, root) %%config(noreplace) /etc/pam.d/calendar
%%attr(755, bin, bin) %%dir %{apache_documentroot}/webmail
%%attr(444, bin, bin) %{apache_documentroot}/webmail/*
%%attr(444, bin, bin) %{_datadir}/configlist.webmail
ZZ

echo %{apache_cgibindir}/webmlm >>filelist.webmlm
echo '%%attr(644, root, root) %{_sysconfdir}/webmlmrc.dist' >>filelist.webmlm

echo '%%attr(4511, root, bin) %{apache_cgibindir}/webadmin' >filelist.webadmin


# -----------------------------------------------------------------------------

%post

%if %using_systemd
if test -f %{initdir}/courier
then
	/sbin/chkconfig --del courier
	/bin/systemctl stop courier.service || :
fi
%endif

if test -f %{_sysconfdir}/userdb || test -d %{_sysconfdir}/userdb
then
	:
else
	%{__mkdir_p} %{_sysconfdir}/userdb
	chmod 700 %{_sysconfdir}/userdb
	chown --reference=%{_sysconfdir} %{_sysconfdir}/userdb
fi


# Somehow the systemd macro ends up corrupting with_fax

%if %with_fax
%define with_fax_flag 1
%else
%define with_fax_flag 0
%endif

%if %using_systemd
%systemd_post courier.service
if [ $1 -eq 1 ]
then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --del courier
/sbin/chkconfig --add courier
%endif

%{_datadir}/sysconftool `%{__cat} %{_datadir}/configlist` >/dev/null
%if %alternatives
/usr/sbin/alternatives --install /usr/sbin/sendmail mta %{_bindir}/sendmail 91 \
   --slave /usr/bin/mailq mta-mailq %{_bindir}/mailq \
   --slave /usr/bin/rmail mta-rmail %{_bindir}/rmail \
   --slave /usr/bin/newaliases mta-newaliases %{_sbindir}/makealiases %initscript_courier
%endif

%triggerpostun -- courier-sendmail-wrapper
%if %alternatives
/usr/sbin/alternatives --install /usr/sbin/sendmail mta %{_bindir}/sendmail 91 \
   --slave /usr/bin/mailq mta-mailq %{_bindir}/mailq \
   --slave /usr/bin/rmail mta-rmail %{_bindir}/rmail \
   --slave /usr/bin/newaliases mta-newaliases %{_sbindir}/makealiases %initscript_courier
%endif

%postun
%if %alternatives
if test "$1" = 0 ; then
	/usr/sbin/alternatives --remove mta %{_bindir}/sendmail
fi
%endif

%if %using_systemd
%systemd_postun_with_restart
%endif

if test "$1" != 0
then
%if %using_systemd
	/bin/systemctl try-restart courier.service || :
%else
        /sbin/service courier condrestart >/dev/null 2>&1
%endif
fi

%preun
if test "$1" = "0"
then
%if %using_systemd
	/bin/systemctl stop courier.service
	/bin/systemctl disable courier.service
%else
        %{_sbindir}/esmtpd stop
        %{_sbindir}/esmtpd-msa stop
        %{initdir}/courier stop >/dev/null

        /sbin/chkconfig --del courier
%endif
fi

%preun ldap
if test "$1" = "0"
then
	if test -x %{_sbindir}/courierldapaliasd
	then
		%{_sbindir}/courierldapaliasd stop >/dev/null 2>&1 || /bin/true
	fi
fi

%post imapd
%{_datadir}/sysconftool `%{__cat} %{_datadir}/configlist.imap` >/dev/null

%preun imapd
if test "$1" = "0"
then
	%{_sbindir}/imapd stop
	%{_sbindir}/imapd-ssl stop
fi

%post pop3d
%{_datadir}/sysconftool `%{__cat} %{_datadir}/configlist.pop3` >/dev/null

%preun pop3d
if test "$1" = "0"
then
	%{_sbindir}/pop3d stop
	%{_sbindir}/pop3d-ssl stop
fi

%preun webmail
if test "$1" = "0"
then
	test ! -x %{_sbindir}/webmaild || %{_sbindir}/webmaild stop
fi

%post webmail
%{_datadir}/sysconftool `%{__cat} %{_datadir}/configlist.webmail` >/dev/null

%preun mlm-web

if test "$1" = "0"
then
	%{_bindir}/webmlmd stop %{_sysconfdir}/webmlmrc >/dev/null 2>&1 || :
fi

%post mlm-web

%{_datadir}/sysconftool %{_sysconfdir}/webmlmrc >/dev/null

if test "$1" -gt 1
then
	%{_bindir}/webmlmd restart %{_sysconfdir}/webmlmrc >/dev/null 2>&1 || :
fi

%post webadmin
if test ! -f %{_sysconfdir}/webadmin/password
then
	dd if=/dev/urandom 2>/dev/null | tr -d -c '[A-Za-z0-9]' | dd bs=16 count=1 2>/dev/null >%{_sysconfdir}/webadmin/password
	chmod 400 %{_sysconfdir}/webadmin/password
	chown --reference=%{_sysconfdir}/webadmin %{_sysconfdir}/webadmin/password
fi

%files -f filelist
%if %alternatives
%attr(-, root, root) /usr/bin/sendmail
%attr(-, root, root) /usr/lib/sendmail
%endif
%attr(644, root, root) %config(noreplace) /etc/pam.d/esmtp
%attr(555, bin, bin) %doc README.REDHAT AUTHORS COPYING
%attr(-, bin, bin) %doc htmldoc/*
%attr(555, bin, bin) %{_datadir}/sysconftool
%attr(444, bin, bin) %{_datadir}/configlist

%attr(-, root, root) /etc/skel/Maildir

%if %alternatives

%else
%files sendmail-wrapper -f filelist.sendmail-wrapper
%endif

%files maildrop-wrapper

%attr(-, bin, bin) /usr/local/bin/*

%files pop3d -f filelist.pop3
%attr(644, root, root) %config(noreplace) /etc/pam.d/pop3
%attr(444, bin, bin) %{_datadir}/configlist.pop3

%files imapd -f filelist.imap
%attr(644, root, root) %config(noreplace) /etc/pam.d/imap
%attr(444, bin, bin) %{_datadir}/configlist.imap

%files webmail -f filelist.webmail

%files mlm-web -f filelist.webmlm

%files webadmin -f filelist.webadmin

%files maildrop -f filelist.maildrop

%files mlm -f filelist.mlm

%files ldap -f filelist.ldap

%files mysql -f filelist.mysql

%files pgsql -f filelist.pgsql

%if %with_fax_flag
%files fax -f filelist.fax
%attr(-, root, root) /etc/mgetty+sendfax/new_fax
%endif

# -----------------------------------------------------------------------------

%clean
%{__rm} -rf $RPM_BUILD_ROOT
