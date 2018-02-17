%{?_javapackages_macros:%_javapackages_macros}

Name:           guava
Version:        24.0
Release:        2%{?dist}.1
Group:          Development/Java
Summary:        Google Core Libraries for Java
License:        ASL 2.0
URL:            https://github.com/google/guava
BuildArch:      noarch

Source0:        https://github.com/google/guava/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)

%description
Guava is a suite of core and expanded libraries that include
utility classes, Google’s collections, io classes, and much
much more.
This project is a complete packaging of all the Guava libraries
into a single jar.  Individual portions of Guava can be used
by downloading the appropriate module and its dependencies.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%package testlib
Summary:        The guava-testlib artifact

%description testlib
guava-testlib provides additional functionality for conveninent unit testing

%prep
%setup -q

find . -name '*.jar' -delete

%pom_disable_module guava-gwt
%pom_disable_module guava-tests

%pom_remove_plugin -r :animal-sniffer-maven-plugin
# Downloads JDK source for doc generation
%pom_remove_plugin :maven-dependency-plugin guava

%pom_remove_dep :caliper guava-tests

%mvn_package :guava-parent guava

# javadoc generation fails due to strict doclint in JDK 1.8.0_45
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_xpath_inject /pom:project/pom:build/pom:plugins/pom:plugin/pom:configuration/pom:instructions "<_nouses>true</_nouses>" guava/pom.xml

%pom_remove_dep -r :animal-sniffer-annotations
%pom_remove_dep -r :error_prone_annotations
%pom_remove_dep -r :j2objc-annotations
%pom_remove_dep -r org.checkerframework:

annotations=$(
    find -name '*.java' \
    | xargs fgrep -h \
        -e 'import com.google.j2objc.annotations' \
        -e 'import com.google.errorprone.annotation' \
        -e 'import org.codehaus.mojo.animal_sniffer' \
        -e 'import org.checkerframework' \
    | sort -u \
    | sed 's/.*\.\([^.]*\);/\1/' \
    | paste -sd\|
)
# guava started using quite a few annotation libraries for code quality, which
# we don't have. This ugly regex is supposed to remove their usage from the code
find -name '*.java' | xargs sed -ri \
    "s/^import .*\.($annotations);//;s/@($annotations)"'\>\s*(\((("[^"]*")|([^)]*))\))?//g'

%build
# Tests fail on Koji due to insufficient memory,
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332971
%mvn_build -s -f

%install
%mvn_install

%files -f .mfiles-guava
%doc CONTRIBUTORS README*
%doc COPYING

%files javadoc -f .mfiles-javadoc
%doc COPYING

%files testlib -f .mfiles-guava-testlib

%changelog
* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 24.0-2
- Escape macros in %%changelog

* Mon Feb 05 2018 Michael Simacek <msimacek@redhat.com> - 24.0-1
- Update to upstream version 24.0

* Mon Nov 06 2017 Michael Simacek <msimacek@redhat.com> - 20.0-1
- Update to upstream version 20.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 18.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 18.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 18.0-9
- Allow conditional builds without testlib

* Thu Jun 16 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 18.0-8
- Cleanup package

* Tue May 10 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 18.0-7
- Disable tests due to insufficient memory on Koji

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 18.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 22 2015 Noa Resare <noa@resare.com> - 18.0-5
- enable module guava-testlib
- enable tests in guava-testlib
- backport fix to HashMap related test from 19.0-SNAPSHOT

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 18.0-3
- Remove maven-javadoc-plugin execution

* Fri Feb  6 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 18.0-2
- Update upstream website URL

* Wed Jan  7 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 18.0-1
- Update to v. 18 (#1175401)
- Use %%doc

* Wed Oct  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 17.0-2
- Add alias for com.google.guava:guava-jdk5

* Fri Jun 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 17.0-1
- Add patch for Java 8

* Tue Jun 17 2014 Roland Grunberg <rgrunber@redhat.com> - 15.0-4
- Do not generate uses directive for exports.

* Fri Jun 13 2014 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> 17.0-1
- Update to latest upstream version (#1109442).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 15.0-2
- Use Requires: java-headless rebuild (#1067528)

* Wed Jan  8 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 15.0-1
- Update to upstream version 15.0

* Mon Aug 12 2013 gil cattaneo <puntogil@libero.it> 13.0-6
- fix rhbz#992456
- update to current packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-4
- Replace BR on ant-nodeps with ant

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-4
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 13.0-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 13.0-1
- Update to upstream version 13.0
- Remove RPM bug workaround
- Convert patches to pom macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 gil cattaneo <puntogil@libero.it> 11.0.2-1
- Update to 11.0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 09-1
- Update to 09
- Packaging fixes
- Build with maven

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 14 2010 Hui wang <huwang@redhat.com> - 05-4
- Patch pom

* Fri Jun 18 2010 Hui Wang <huwang@redhat.com> - 05-3
- Fixed jar name in install section
- Removed spaces in description

* Thu Jun 17 2010 Hui Wang <huwang@redhat.com> - 05-2
- Fixed summary
- Fixed description
- Fixed creating symlink insturctions
- add depmap

* Thu Jun 10 2010 Hui Wang <huwang@redhat.com> - 05-1
- Initial version of the package
