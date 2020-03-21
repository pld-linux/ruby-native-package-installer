#
# Conditional build:
%bcond_without	doc	# ri/rdoc documentation

%define pkgname native-package-installer
Summary:	Helps installing native packages on "gem install"
Summary(pl.UTF-8):	Pomoc przy instalowaniu pakietów natywnych przy "gem install"
Name:		ruby-%{pkgname}
Version:	1.0.9
Release:	2
License:	LGPL v3+
Group:		Development/Languages
# tarballs: https://github.com/ruby-gnome2/native-package-installer/releases
# gems: https://rubygems.org/gems/native-package-installer
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	e31f13f221831458ed5c05f7b12111de
URL:		https://github.com/ruby-gnome2/native-package-installer
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Users need to install native packages to install an extension library
that depends on native packages. It bores users because users need to
install native packages and an extension library separately.
native-package-installer helps to install native packages on "gem
install". Users can install both native packages and an extension
library by one action, "gem install".

%description -l pl.UTF-8
Użytkownicy potrzebują instalować pakiety natywne, aby zainstalować
od nich zależące biblioteki rozszerzeń. Nudzi to użytkowników,
ponieważ muszą instalować osobno pakiety natywne i biblioteki
rozszerzeń. native-package-installer pomaga instalować pakiety natywne
w trakcie procesu "gem install". Użytkownicy mogą zainstalować
jednocześnie natywne pakiety, jak i bibliotekę rozszerzeń tym
pojedynczym poleceniem.

%package rdoc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for %{pkgname}.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%package ri
Summary:	ri documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for %{pkgname}.

%description ri -l pl.UTF-8
Dokumentacji w formacie ri dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}-%{version}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

#'

rdoc --ri --op ri lib
rdoc --op rdoc lib
%{__rm} ri/cache.ri
%{__rm} ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md doc/text/news.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/NativePackageInstaller
%endif
