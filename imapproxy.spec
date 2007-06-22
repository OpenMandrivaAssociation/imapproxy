%define name		imapproxy
%define distname	up-%{name}
%define version		1.2.4
%define release		%mkrel 6
%define _ssldir		%{_sysconfdir}/ssl/imapproxy

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Imapproxy is a proxy for the IMAP protocol
License:	GPL
Group:		System/Servers
URL:		http://www.imapproxy.org/
Source0:	http://www.imapproxy.org/downloads/%{distname}-%{version}.tar.bz2
Source1:	%{name}.init
Patch0:		%{name}-1.2.4-conf.patch
Patch1:		%{name}-1.2.4-md5.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	tcp_wrappers-devel openssl-devel ncurses-devel
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
Imapproxy proxies IMAP transactions between an IMAP client and an IMAP
server. The connection to the server is kept open and cached for a
time after the client closes its side, in order to reuse it when the
client tries to open another one to the same IMAP server with the same
user ID.

%prep
%setup -q -n %{distname}-%{version}
%patch0 -p1 -b .init
%patch1 -p0

%build
%serverbuild
# kerberos include is needed (because of openssl-0.9.7 ?)
export CPPFLAGS="$CPPFLAGS -I%{_prefix}/kerberos/include"
%configure2_5x
%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir} \
	%{buildroot}%{_initrddir} \
	%{buildroot}%{_ssldir}

install -m 755 bin/in.imapproxyd %{buildroot}%{_sbindir}/
install -m 755 bin/pimpstat %{buildroot}%{_sbindir}/
install -m 644 scripts/%{name}.conf %{buildroot}%{_sysconfdir}/
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(-,root,root)
%doc COPYING copyright ChangeLog README README.ssl README.known_issues
%dir %{_ssldir}
%attr(0755,root,root) %{_sbindir}/in.imapproxyd
%attr(0755,root,root) %{_sbindir}/pimpstat
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf

