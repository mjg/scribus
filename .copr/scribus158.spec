%global build_timestamp %{lua: print(os.date("%Y%m%d"))}
%global	origname	scribus
Name:		scribus158
Version:	1.5.8
%global fversion	%{version}.svn
Release:	0.%{build_timestamp}git%{?dist}
Summary:	Open Source Page Layout
License:	GPLv2+
URL:		http://www.scribus.net/
# svn export svn://scribus.net/trunk/Scribus scribus
# tar --exclude-vcs -cJf scribus-1.5.0-20161204svn21568.tar.xz scribus
## The following script removes non free contents
# .copr/make-free-archive %%{version}
Source0:	https://github.com/mjg/%{origname}/archive/fedora158.tar.gz#/%{origname}-%{version}-%{build_timestamp}git.tar.gz
#Source0:	https://github.com/mjg/%%{origname}-svn/archive/trunk.tar.gz#/%%{origname}-%%{version}-%%{build_timestamp}git.tar.gz

BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	cups-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gcc-c++
BuildRequires:	ghostscript
BuildRequires:	hyphen-devel
BuildRequires:	libappstream-glib
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(GraphicsMagick++)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(hunspell)
BuildRequires:	pkgconfig(icu-uc)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libcdr-0.1)
BuildRequires:	pkgconfig(libfreehand-0.1)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libmspub-0.1)
BuildRequires:	pkgconfig(libpagemaker-0.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libpodofo)
BuildRequires:	pkgconfig(libqxp-0.0)
BuildRequires:	pkgconfig(librevenge-0.0)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libvisio-0.1)
BuildRequires:	pkgconfig(libwpd-0.10)
BuildRequires:	pkgconfig(libwpg-0.3)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libzmf-0.0)
BuildRequires:	pkgconfig(openscenegraph)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(poppler-cpp)
BuildRequires:	pkgconfig(poppler-data)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(Qt5) > 5.14
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5UiTools)
BuildRequires:	pkgconfig(Qt5WebKit)
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python3dist(pillow)
BuildRequires:	python3-qt5-devel
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3-tkinter


%filter_provides_in %{_libdir}/%{origname}-%{version}/plugins
%filter_setup


%description
Scribus is an desktop open source page layout program with
the aim of producing commercial grade output in PDF and
Postscript, primarily, though not exclusively for Linux.

While the goals of the program are for ease of use and simple easy to
understand tools, Scribus offers support for professional publishing
features, such as CMYK color, easy PDF creation, Encapsulated Postscript
import/export and creation of color separations.


%prep
%autosetup -n %{origname}-fedora158 -p1

# fix permissions
chmod a-x scribus/pageitem_latexframe.h

# drop shebang lines from python scripts
%py3_shebang_fix %{origname}/plugins/scriptplugin/{samples,scripts}/*.py

%build
%cmake	\
	-DCMAKE_CXX_STANDARD=17 \
	-DWANT_CPP17=ON \
	-DWANT_CCACHE=YES \
	-DWANT_DISTROBUILD=YES \
	-DWANT_GRAPHICSMAGICK=1 \
	-DWANT_HUNSPELL=1 \
%if "%{_lib}" == "lib64"
	-DWANT_LIB64=YES \
%endif
	-DWANT_NORPATH=1 \
	-DWANT_VERSIONING=YES \
	-DWITH_BOOST=1 \
	-DWITH_PODOFO=1

%cmake_build

%install
%cmake_install

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{origname}-%{fversion}.desktop
appstream-util validate-relax --nonet \
	%{buildroot}/%{_metainfodir}/%{origname}-%{fversion}.appdata.xml


%files
%license %{_defaultdocdir}/%{origname}-%{fversion}/COPYING
%doc %{_defaultdocdir}/%{origname}-%{fversion}/AUTHORS
%doc %{_defaultdocdir}/%{origname}-%{fversion}/ChangeLog
%doc %{_defaultdocdir}/%{origname}-%{fversion}/LINKS
%doc %{_defaultdocdir}/%{origname}-%{fversion}/README
%doc %{_defaultdocdir}/%{origname}-%{fversion}/TRANSLATION
%{_bindir}/%{origname}-%{fversion}
%{_libdir}/%{origname}-%{fversion}/
%{_metainfodir}/%{origname}-%{fversion}.appdata.xml
%{_datadir}/applications/%{origname}-%{fversion}.desktop
%{_datadir}/mime/packages/%{origname}-%{fversion}.xml
%{_datadir}/icons/hicolor/16x16/apps/%{origname}-%{fversion}.png
%{_datadir}/icons/hicolor/32x32/apps/%{origname}-%{fversion}.png
%{_datadir}/icons/hicolor/128x128/apps/%{origname}-%{fversion}.png
%{_datadir}/icons/hicolor/256x256/apps/%{origname}-%{fversion}.png
%{_datadir}/icons/hicolor/512x512/apps/%{origname}-%{fversion}.png
%{_datadir}/icons/hicolor/1024x1024/apps/%{origname}-%{fversion}.png
%{_datadir}/%{origname}-%{fversion}/
%{_mandir}/man1/*
%{_mandir}/pl/man1/*
%{_mandir}/de/man1/*


%changelog
* Thu Jan 20 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.5.8-0.20220120git
- really build with CPP17

* Tue Jan 18 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.5.8-0.20220118git
- sync with Fedora rawhide spec (sub packages)
- adjust source to my fedora branch

* Sun Jan 02 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.5.8-0.20220102git
- sync with Fedora rawhide spec (for the main package)

* Tue Sep 21 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.5.8-0.20210921git
- cto patch is upstreamed now

* Wed May 05 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.5.8-0.20210505git
- trunk is 1.5.8svn now

* Sun Apr 25 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.5.7-1
- release of 1.5.7

* Tue Apr 20 2021 Michael J Gruber <mjg@fedoraproject.org> - 1.5.7-0.20210420git
- build off my own git-svn repo

* Wed Nov 11 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.5.7-0.20201111git
- rebase with fedora spec file for 1.5.6-0.13

* Mon Nov 09 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.5.7-0.20201109git
- trunk is 1.5.7svn now

* Wed Jul 22 2020 Michael J Gruber <mjg@fedoraproject.org> - 1.5.6-0.20200722git
- adjust to new cmake macros

* Mon Nov 04 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.5.6-0.20191104git
- remove upstreamed patch

* Sat Nov 02 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.5.6-0.20191102git
- fix build with python 3.8

* Fri Nov 01 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.5.6-0.20191101git
- scribus scripter uses py3 now, hooray!

* Wed Aug 14 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.5.6-0.20190814git
- make scribus fit for rawhide (py == py3) until they kill off py2

* Mon Aug 12 2019 Michael J Gruber <mjg@fedoraproject.org> - 1.5.6-0.20190812git
- 1.5.5 is released, svn is 1.5.6 now

* Fri Dec 07 2018 Michael J Gruber <mjg@fedoraproject.org> - 1.5.5-0.20181207git
- rename to allow easier parallel install

* Thu Nov 22 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20181122git
- Snapshot svn 22773

* Wed Nov 14 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20181114git
- Snapshot svn 22756

* Sat Nov 03 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20181101git
- Snapshot svn 22751

* Thu Oct 25 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20181022git
- Snapshot svn 22741

* Thu Oct 25 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20181021git
- Snapshot svn 22740

* Sat Oct 13 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0.20181013git
- Snapshot svn 22730

* Mon Oct 01 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20181001git
- Snapshot svn 22716

* Mon Sep 24 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180924git
- Snapshot svn 22704

* Fri Sep 07 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180907git
- Snapshot svn 22672

* Fri Aug 24 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180824git
- Snapshot svn 22649

* Wed Aug 22 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180822git
- Snapshot svn 22641

* Tue Aug 07 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180807git
- Snapshot svn 22620
- Add gcc-c++ dependencies

* Sun Jul 22 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180722git
- Snapshot svn 22597 

* Thu Jun 21 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180621git
- New snapshot

* Wed Jun 06 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180606git
- Snapshot svn 22578

* Tue May 29 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180529git
- Snapshot svn 22563

* Fri May 04 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180504git
- Snapshot svn 22522

* Wed May 02 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0-20180502git
- Snapshot svn 22514

* Mon Apr 30 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.5-0.20180430git
- Snapshot svn 22496

* Mon Apr 23 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.4-0.20180423git
- Snapshot svn 22473

* Wed Apr 18 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.4-0-20180418git
- Snapshot svn 22469

* Tue Apr 10 2018 Luya Tshimbalanga <luya@fedoraproject.org> - 1.5.4-0.20180410git
- Snapshot svn 22466
