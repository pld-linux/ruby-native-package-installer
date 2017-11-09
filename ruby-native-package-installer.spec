#
# Conditional build:
%bcond_without	doc			# don't build ri/rdoc

%define pkgname native-package-installer
Summary:	Helps installing native packages on "gem install".freeze
Name:		ruby-%{pkgname}
Version:	1.0.4
Release:	1
License:	LGPL v3+
#Source0:	http://rubyforge.org/frs/download.php/18699/%{pkgname}-%{version}.tgz
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	84f4c35d5c9e858c94b4f650a24ff8c2
Group:		Development/Languages
URL:		https://github.com/ruby-gnome2/native-package-installer
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
# optional locale BR, see ri/rdoc building below
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Users need to install native packages to install an extension library
that depends on native packages. It bores users because users need to
install native packages and an extension library separately.
native-package-installer helps to install native packages on
"gem install". Users can install both native packages and
an extension library by one action, "gem install".freeze

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

# with rdoc/ri:
# optional locale force, see BR above as well
# UTF8 locale needed for doc generation
export LC_ALL=en_US.UTF-8

rdoc --ri --op ri lib
rdoc --op rdoc lib
# rm -r ri/NOT_THIS_MODULE_RELATED_DIRS
rm ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
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
