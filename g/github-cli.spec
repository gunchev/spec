%undefine _missing_build_ids_terminate_build
%undefine _debugsource_packages
%global import_path github.com/cli/cli

Name:     github-cli
Version:  2.9.0
Release:  1
Summary:  GitHub's official command line tool
License:  MIT
Group:    Other
URL:      https://github.com/cli/cli
Source:   cli-%version.tar.gz
BuildRequires: golang

%description
gh is GitHub on the command line. It brings pull requests, issues, and other
GitHub concepts to the terminal next to where you are already working with git
and your code.

%prep
%setup -q -n cli-%{version}

%build
#export GOFLAGS="${GOFLAGS-} -mod=vendor"
make GH_VERSION="v%version" bin/gh manpages
mkdir completions
bin/gh completion -s bash > completions/bash
bin/gh completion -s zsh > completions/zsh
bin/gh completion -s fish > completions/fish

%install
install -Dm 755 bin/gh %buildroot/%_bindir/gh
install -Dm644 completions/bash %buildroot/%_datadir/bash-completion/completions/gh
install -Dm644 completions/zsh %buildroot/%_datadir/zsh/site-functions/_gh
install -Dm644 completions/fish %buildroot/%_datadir/fish/vendor_completions.d/gh.fish
cp -r share/man -T %buildroot/%_mandir

%files
%_bindir/gh
%_datadir/bash-completion/completions/gh
%_datadir/zsh/site-functions/_gh
%_datadir/fish/vendor_completions.d/gh.fish
%_mandir/man1/*
%doc *.md

%changelog
* Sun Apr 24 2022 Wei-Lun Chao <bluebat@member.fsf.org> - 2.9.0
- Rebuilt for Fedora
* Wed Oct 28 2020 Mikhail Gordeev <obirvalger@altlinux.org> 1.2.0-alt1
- update to 1.2.0
* Fri Sep 18 2020 Mikhail Gordeev <obirvalger@altlinux.org> 1.0.0-alt1
- Initial build for Sisyphus
