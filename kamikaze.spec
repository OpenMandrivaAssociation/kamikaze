%define tag	0_2

Name:		    kamikaze
Version:	    0.2
Release:	    12
Summary:	    An SCM query tool similar to Mozilla's tool, Bonsai
License:	    Apache License
Group:		    Networking/WWW
URL:		    http://kamikaze-qscm.tigris.org/
Source0:	    http://kamikaze-qscm.tigris.org/files/documents/2030/17053/%{name}.v%{tag}.tar.bz2
Patch0:		    %{name}-0.2.fhs.patch.bz2
Patch1:		    %{name}-0.2.fix-db-access.patch.bz2
Requires:	    mod_php
BuildArch:	    noarch

%description
Kamikaze-qscm is a tool that allows developers and CM related personnel to
query the commits made to one or more source control repositories. It is very
similar to Mozilla's bonsai tool. Kamikaze-qscm currently works with
Subversion, but a modular approach is planned for other SCM systems.

Kamikaze for Subversion currently consists of a perl back-end hook for
inserting commit information into a MySQL database. (In the future, a modular
approach to data storage is planned - allowing the use of many different data
storage implementations. ) A PHP front-end is used to perform repository
queries and display results. (In the future a web service API (XML-RPC and/or
SOAP) will be provided to access the same information for incorporation into
other tools.) 

%prep
%setup -q -n %{name}
%patch0 -p 1
%patch1 -p 0

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -m 644 html/index.php %{buildroot}%{_var}/www/%{name}

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}/lib
install -d -m 755 %{buildroot}%{_datadir}/%{name}/db
install -d -m 755 %{buildroot}%{_datadir}/%{name}/hooks
install -m 644 html/query.php %{buildroot}%{_datadir}/%{name}/lib
install -m 644 db/{author,repository,resource,revision}.sql %{buildroot}%{_datadir}/%{name}/db
install -m 755 hooks/commit2db.pl %{buildroot}%{_datadir}/%{name}/hooks

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 html/config.inc %{buildroot}%{_sysconfdir}/%{name}/web.conf
install -m 644 hooks/config.inc %{buildroot}%{_sysconfdir}/%{name}/hook.conf

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration
Alias /%{name} %{_var}/www/%{name}

<Directory %{_var}/www/%{name}>
    Order allow,deny
    Allow from all
</Directory>
EOF

cat > README.mdv <<EOF
Mandriva RPM specific notes

setup
-----
The setup used here differs from default one, to achieve better FHS compliance.
- the files accessibles from the web are in /var/www/kamikaze
- the files non accessibles from the web are in /usr/share/kamikaze
- the configuration file is /etc/kamikaze.conf

post-installation
-----------------
You have to create the MySQL database, and import all files from
/usr/share/kamikaze/db
EOF

%clean
rm -rf %{buildroot}



%files
%defattr(-,root,root)
%doc *.txt README.mdv
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}
%{_var}/www/%{name}
%{_datadir}/%{name}



%changelog
* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2-10mdv2011.0
+ Revision: 612522
- the mass rebuild of 2010.1 packages

* Tue Feb 23 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.2-9mdv2010.1
+ Revision: 510415
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0.2-8mdv2010.0
+ Revision: 429657
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tv@mandriva.org> 0.2-7mdv2009.0
+ Revision: 247494
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.2-5mdv2008.1
+ Revision: 132456
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - import kamikaze


* Tue Aug 29 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.2-4mdv2007.0
- use webapps macros
- use herein document for README.mdv

* Sun Mar 19 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.2-3mdk
- fix license

* Sat Mar 18 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.2-2mdk
- better FHS compliance
- backport compatible apache configuration file
- fix db access
- README.mdk
- drop useless DB file

* Mon Mar 13 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.2-1mdk
- first mdk release 
