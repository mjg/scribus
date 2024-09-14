## Pull in upstream source:
# {{{ git submodule update --init 1>&2; git submodule }}}
%global svnversion	{{{ git -C source svn find-rev HEAD }}}
%global gitversion	{{{ git -C source rev-parse HEAD }}}
%global gitshortversion	{{{ git -C source rev-parse --short HEAD }}}
%global	origname	scribus
Name:		scribus170
%global targetversion	1.7.0
%global fullname	%{origname}-%{targetversion}.svn
Version:	%{targetversion}~svn^%{svnversion}.g%{gitshortversion}
Release:	1%{?dist}
Summary:	Open Source Page Layout
License:	GPLv2+
URL:		http://www.scribus.net/
## The following script removes non free contents:
# make-free-archive.sh {{{ cd source && ../make-free-archive.sh 1>&2 }}}
Source:		{{{ GIT_DIRTY=1 git_pack path=source dir_name=scribus }}}
Patch:		0001-fix-missing-qApp-definition.patch

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
BuildRequires:	pkgconfig(libpodofo) >= 0.9.0
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
BuildRequires:	pkgconfig(Qt6) >= 6.2
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	qt6-qtbase-private-devel
BuildRequires:	pkgconfig(tk)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python3dist(pillow)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3-tkinter


%filter_provides_in %{_libdir}/%{fullname}/plugins
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
%autosetup -n scribus -p1

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

rm -rf %{buildroot}/%{_includedir}/qt6advanceddocking
rm -rf %{buildroot}/%{_libdir}/cmake/qt6advanceddocking
rm -rf %{buildroot}/usr/license/ads
rm -f  %{buildroot}/%{_libdir}/libqt6advanceddocking_static.a
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{fullname}.desktop
appstream-util validate-relax --nonet \
	%{buildroot}/%{_metainfodir}/%{fullname}.appdata.xml


%files
%license %{_defaultdocdir}/%{fullname}/COPYING
%doc %{_defaultdocdir}/%{fullname}/AUTHORS
%doc %{_defaultdocdir}/%{fullname}/ChangeLog
%doc %{_defaultdocdir}/%{fullname}/LINKS
%doc %{_defaultdocdir}/%{fullname}/README
%doc %{_defaultdocdir}/%{fullname}/TRANSLATION
%{_bindir}/%{fullname}
%{_libdir}/%{fullname}/
%{_metainfodir}/%{fullname}.appdata.xml
%{_datadir}/applications/%{fullname}.desktop
%{_datadir}/mime/packages/%{fullname}.xml
%{_datadir}/icons/hicolor/16x16/apps/%{fullname}.png
%{_datadir}/icons/hicolor/32x32/apps/%{fullname}.png
%{_datadir}/icons/hicolor/128x128/apps/%{fullname}.png
%{_datadir}/icons/hicolor/256x256/apps/%{fullname}.png
%{_datadir}/icons/hicolor/512x512/apps/%{fullname}.png
%{_datadir}/icons/hicolor/1024x1024/apps/%{fullname}.png
%{_datadir}/icons/hicolor/16x16/mimetypes/application-vnd.%{origname}.png
%{_datadir}/icons/hicolor/32x32/mimetypes/application-vnd.%{origname}.png
%{_datadir}/icons/hicolor/64x64/mimetypes/application-vnd.%{origname}.png
%{_datadir}/icons/hicolor/128x128/mimetypes/application-vnd.%{origname}.png
%{_datadir}/icons/hicolor/256x256/mimetypes/application-vnd.%{origname}.png
%{_datadir}/%{fullname}/
%{_mandir}/man1/*
%{_mandir}/pl/man1/*
%{_mandir}/de/man1/*


%changelog
* Mon Mar 07 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.7.0~svn^24990.g9f617d817-1
- base 1.7.0 off 1.5.9
- 1.7.0 requires Qt6
- disable OSG until ported to Qt6

* Sun Mar 06 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.5.9~svn^24971.ga68d616dd-1
- use current version scheme
- build off source as submodule
- clean source on srpm creation

* Wed Mar 02 2022 Michael J Gruber <mjg@fedoraproject.org> - 1.5.9-0.20220302git
- base 1.5.9 off 1.5.8

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
