%define distname up-%{name}
%define _ssldir %{_sysconfdir}/ssl/imapproxy

Summary:	Proxy for the IMAP protocol
Name:		imapproxy
Version:	1.2.7
Release:	5
License:	GPLv2+
Group:		System/Servers
URL:		http://www.imapproxy.org/
Source0:	http://www.imapproxy.org/downloads/%{distname}-%{version}.tar.gz
Source1:	%{name}.service
Patch0:		%{name}-1.2.4-conf.patch
BuildRequires:	tcp_wrappers-devel openssl-devel ncurses-devel
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	tcp_wrappers

%description
Imapproxy proxies IMAP transactions between an IMAP client and an IMAP
server. The connection to the server is kept open and cached for a
time after the client closes its side, in order to reuse it when the
client tries to open another one to the same IMAP server with the same
user ID.

%prep

%setup -q -n %{distname}-%{version}
%patch0 -p1 -b .service

%build
%serverbuild

# fixes https://qa.mandriva.com/show_bug.cgi?id=37974
CFLAGS="`echo $CFLAGS | sed 's/-Wp,-D_FORTIFY_SOURCE=2//'`"

# kerberos include is needed (because of openssl-0.9.7 ?)
export CPPFLAGS="$CPPFLAGS -I%{_prefix}/kerberos/include"
%configure2_5x
%make

%install

mkdir -p %{buildroot}%{_sbindir} \
	%{buildroot}%{_unitdir} \
	%{buildroot}%{_ssldir}

install -m 755 bin/in.imapproxyd %{buildroot}%{_sbindir}/
install -m 755 bin/pimpstat %{buildroot}%{_sbindir}/
install -m 644 scripts/%{name}.conf %{buildroot}%{_sysconfdir}/
install -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/imapproxy.service

%clean

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc copyright ChangeLog README README.ssl README.known_issues
%dir %{_ssldir}
%attr(0755,root,root) %{_sbindir}/in.imapproxyd
%attr(0755,root,root) %{_sbindir}/pimpstat
%attr(0755,root,root) %{_unitdir}/%{name}*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf
