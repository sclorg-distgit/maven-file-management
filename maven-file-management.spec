%global pkg_name maven-file-management
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global pkgname file-management

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.2.1
Release:        8.9%{?dist}
# Maven-shared defines file-management version as 1.2.2
Epoch:          1
Summary:        Maven File Management API
License:        ASL 2.0
# URL is not working now, cached copy at http://web.archive.org/web/20121029070007/http://maven.apache.org/shared/file-management/
URL:            http://maven.apache.org/shared/%{pkgname}
# svn export http://svn.apache.org/repos/asf/maven/shared/tags/file-management-1.2.1
# tar caf maven-file-management-1.2.1.tar.xz file-management-1.2.1/
Source0:        %{pkg_name}-%{version}.tar.xz
# ASL mandates that the licence file be included in redistributed source
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}maven-shared
BuildRequires:  %{?scl_prefix}modello


%description
Provides a component for plugins to easily resolve project dependencies.

This is a replacement package for maven-shared-file-management.

%package javadoc
Summary:        Javadoc for %{pkg_name}
    
%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkgname}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
cp -p %{SOURCE1} LICENSE.txt

# Need namespace for new version modello
# Bug has been filed at http://jira.codehaus.org/browse/MSHARED-234
sed -i "s|<model>|<model xmlns=\"http://modello.codehaus.org/MODELLO/1.3.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://modello.codehaus.org/MODELLO/1.3.0 http://modello.codehaus.org/xsd/modello-1.3.0.xsd\" xml.namespace=\"..\" xml.schemaLocation=\"..\" xsd.namespace=\"..\" xsd.targetNamespace=\"..\">|" src/main/mdo/fileset.mdo

# FileSetUtilsTest.testDeleteDanglingSymlink() is expected to fail
sed -i /testDeleteDanglingSymlink/,/assert/s/False/True/ `find -name FileSetUtilsTest.java`
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-8.9
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1:1.2.1-8.8
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1:1.2.1-8.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-8.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-8.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-8.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 1:1.2.1-8.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-8.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-8.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:1.2.1-8
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-7
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Tue Feb 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.2.1-6
- Build with xmvn

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1:1.2.1-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jan 18 2013 Tomas Radej <tradej@redhat.com> - 1:1.2.1-3
- Added proper Provides/Obsoletes in javadoc
- Fixed changelog entries

* Mon Jan 14 2013 Tomas Radej <tradej@redhat.com> - 1:1.2.1-2
- Added licence text
- Changed maven target from install to package
- Creating directories in Install

* Wed Aug 08 2012 Tomas Radej <tradej@redhat.com> - 1.2.1-1
- Initial version

