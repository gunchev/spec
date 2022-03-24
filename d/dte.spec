%undefine _debugsource_packages

Summary: A small and easy to use console text editor
Name: dte
Version: 1.10
Release: 1
License: GPLv2
Group: Applications/Editors
Source: https://github.com/craigbarnes/dte/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
URL: https://github.com/craigbarnes/dte

%description
Features:
* Multiple buffers/tabs
* Unlimited undo/redo
* Search and replace
* Syntax highlighting
* Customizable color schemes
* Customizable key bindings
* Command language with auto-completion
* Jump to definition (using ctags)
* Jump to compiler error

%prep
%setup -q
sed -i 's|/usr/local|/usr|' GNUmakefile

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=%{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc LICENSE *.md
%{_bindir}/*
%{_datadir}/man/man?/*

%changelog
* Sun Mar 20 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 1.10
- Rebuilt for Fedora
