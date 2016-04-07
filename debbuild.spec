%include	/usr/lib/rpm/macros.perl
Summary:	Build Debian-compatible .deb packages from RPM .spec files
Name:		debbuild
Version:	0.11.3
Release:	0.1
License:	GPL v2+
Group:		Applications/File
Source0:	https://secure.deepnet.cx/releases/debbuild/%{name}-%{version}.tar.gz
# Source0-md5:	adddf00c1ed1bc062f25accd2b479946
URL:		https://secure.deepnet.cx/trac/debbuild
#BuildRequires:	perl-podlators
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	bash
Requires:	bzip2
Requires:	dpkg
Requires:	fakeroot
Requires:	patch
Requires:	pax
Requires:	xz
Suggests:	dpkg-dev
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
debbuild attempts to build Debian-friendly semi-native packages from
RPM spec files, RPM-friendly tarballs, and RPM source packages
(.src.rpm files). It accepts most of the options rpmbuild does, and
should be able to interpret most spec files usefully.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*
