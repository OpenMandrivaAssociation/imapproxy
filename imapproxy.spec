%define name imapproxy
%define distname up-%{name}
%define _ssldir %{_sysconfdir}/ssl/imapproxy

Summary:	Proxy for the IMAP protocol
Name:		%{name}
Version:	1.2.7
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.imapproxy.org/
Source0:	http://www.imapproxy.org/downloads/%{distname}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-1.2.4-conf.patch
BuildRequires:	tcp_wrappers-devel openssl-devel ncurses-devel
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	tcp_wrappers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Imapproxy proxies IMAP transactions between an IMAP client and an IMAP
server. The connection to the server is kept open and cached for a
time after the client closes its side, in order to reuse it when the
client tries to open another one to the same IMAP server with the same
user ID.

%prep

%setup -q -n %{distname}-%{version}
%patch0 -p1 -b .init

%build
%serverbuild

# fixes https://qa.mandriva.com/show_bug.cgi?id=37974
CFLAGS="`echo $CFLAGS | sed 's/-Wp,-D_FORTIFY_SOURCE=2//'`"

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
%doc copyright ChangeLog README README.ssl README.known_issues
%dir %{_ssldir}
%attr(0755,root,root) %{_sbindir}/in.imapproxyd
%attr(0755,root,root) %{_sbindir}/pimpstat
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}.conf


%changelog
* Mon May 17 2010 Adam Williamson <awilliamson@mandriva.org> 1.2.7-1mdv2011.0
+ Revision: 545041
- drop debian_fix.diff and buffer_overflow_fix.diff, merged upstream
- new release 1.2.7

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 1.2.6-6mdv2010.1
+ Revision: 537365
- rebuild

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.2.6-6mdv2010.0
+ Revision: 429503
- rebuild

* Mon Sep 01 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-5mdv2009.0
+ Revision: 278332
- fix #37974 (Buffer overflow in imapproxy)

* Sat Aug 30 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-4mdv2009.0
+ Revision: 277611
- added two patches to probably fix buffer overflow

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 1.2.6-3mdv2009.0
+ Revision: 247214
- rebuild

* Wed Feb 20 2008 Frederik Himpe <fhimpe@mandriva.org> 1.2.6-1mdv2008.1
+ Revision: 173218
- New upstream version
- Remove patch integrated upstream
- New license policy

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.2.4-7mdv2008.1
+ Revision: 170897
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jun 22 2007 Andreas Hasenack <andreas@mandriva.com> 1.2.4-6mdv2008.0
+ Revision: 43271
- rebuild with serverbuild macro (-fstack-protector)


* Sun Jan 14 2007 Emmanuel Andry <eandry@mandriva.org> 1.2.4-5mdv2007.0
+ Revision: 108736
- buildrequires ncurses-devel
- buildrequires openssl-devel
- uncompress patches
- Import imapproxy

* Mon Aug 14 2006 Emmanuel Andry <eandry@mandriva.org> 1.2.4-4mdv2007.0
- rebuild

* Mon Jul 03 2006 Emmanuel Andry <eandry@mandriva.org> 1.2.4-3mdv2007.0
- %%mkrel
- added patch from netbsd for md5

* Sun Sep 25 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.2.4-2mdk
- Split Requires(post,preun) in Requires(post)+Requires(preun).

* Sun Sep 25 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.2.4-1mdk
- Release 1.2.4.

* Fri Oct 29 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.2-2mdk 
- buildrequires tcp_wrappers-devel
- clean-up service management stuff

* Sat Aug 28 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.2.2-1mdk
- Release 1.2.2.

* Sun May 02 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.2.2-0.rc2.1mdk
- Updated to release 1.2.2rc2.
- Initial Mandrakelinux release.

