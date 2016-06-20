# TODO
# - not sure why %post can't be done at package time?
%include	/usr/lib/rpm/macros.perl
Summary:	Build Debian-compatible .deb packages from RPM .spec files
Name:		debbuild
Version:	16.6.0
Release:	0.2
License:	GPL v2+
Group:		Applications/File
Source0:	https://github.com/ascherer/debbuild/archive/%{name}-%{version}.tar.gz
# Source0-md5:	22a3c34035b3a2f1d086c0ecbb7c6180
URL:		https://github.com/ascherer/debbuild
#BuildRequires:	perl-podlators
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	bash
Requires:	bzip2
Requires:	dpkg
Requires:	fakeroot
Requires:	patch
Requires:	pax
Requires:	xz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir	%{_prefix}/lib

%description
debbuild attempts to build Debian-friendly semi-native packages from
RPM spec files, RPM-friendly tarballs, and RPM source packages
(.src.rpm files). It accepts most of the options rpmbuild does, and
should be able to interpret most spec files usefully.

%prep
%setup -qn %{name}-%{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/macros.d
cp -p macros/macros.in $RPM_BUILD_ROOT%{_libdir}/%{name}/macros
cp -p macros/macros.perl $RPM_BUILD_ROOT%{_libdir}/%{name}/macros.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -p macros/macros.sysutils $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -p macros/macros.texlive $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# this sciptlet originates from scripts/post.sh from sourcecode
%define darch %{__dpkg_architecture}

if [ -x %{darch} ]; then
	DEB_HOST_CPU=$(%{darch} -qDEB_HOST_GNU_CPU 2>/dev/null)
	DEB_HOST_OS=$(%{darch} -qDEB_HOST_ARCH_OS 2>/dev/null)
	DEB_HOST_SYSTEM=$(%{darch} -qDEB_HOST_GNU_SYSTEM 2>/dev/null)
	DEB_HOST_ARCH=$(%{darch} -qDEB_HOST_ARCH_CPU 2>/dev/null)
	DEB_BUILD_ARCH=$(%{darch} -qDEB_BUILD_ARCH 2>/dev/null)

	%{__sed} -e "s/@HOST_ARCH@/${DEB_HOST_ARCH}/g" \
			 -e "s/@BUILD_ARCH@/${DEB_BUILD_ARCH}/g" \
			 -e "s/@HOST_CPU@/${DEB_HOST_CPU}/g" \
			 -e "s/@HOST_OS@/${DEB_HOST_OS}/g" \
			 -e "s/@HOST_SYSTEM@/${DEB_HOST_SYSTEM}/g" \
			 -i %{_libdir}/%{name}/macros
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/macros.*
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/macros
%{_libdir}/%{name}/macros.d
