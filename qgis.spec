%global optflags %{optflags} -DPROTOBUF_USE_DLLS -flto=thin

%define __noautoreq '.*libgrass_.*'

Summary:	Geographic Information System for Linux/Unix
Name:		qgis
Version:	3.36.0
Release:	1
License:	GPLv2+
Group:		Sciences/Geosciences
Url:		http://www.qgis.org/
Source0:	http://qgis.org/downloads/%{name}-%{version}.tar.bz2
Patch0:		qgis-3.30.0-protobuf-absl-linkage.patch
Source100:	%{name}.rpmlintrc
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	dos2unix
BuildRequires:	flex
BuildRequires:	grass
BuildRequires:	imagemagick
BuildRequires:	mlocate
BuildRequires:	postgis
BuildRequires:  qscintilla-qt5-devel
BuildRequires:	python-sip-qt5
BuildRequires:	python-qt5-core
BuildRequires:	python-qt5-quick
BuildRequires:	python-qt5-xml
BuildRequires:	python-qt5-xmlpatterns
BuildRequires:	python-qt5-quickwidgets
BuildRequires:	python-qt5-bluetooth
BuildRequires:	python-qt5-dbus
BuildRequires:	python-qt5-designer
BuildRequires:	python-qt5-enginio
BuildRequires:	python-qt5-gui
BuildRequires:	python-qt5-location
BuildRequires:	python-qt5-multimedia
BuildRequires:	python-qt5-multimediawidgets
BuildRequires:	python-qt5-network
BuildRequires:	python-qt5-nfc
BuildRequires:	python-qt5-opengl
BuildRequires:	python-qt5-positioning
BuildRequires:	python-qt5-printsupport
BuildRequires:	python-qt5-qml
BuildRequires:	python-qt5-remoteobjects
BuildRequires:	python-qt5-sensors
BuildRequires:	python-qt5-serialport
BuildRequires:	python-qt5-sql
BuildRequires:	python-qt5-svg
BuildRequires:	python-qt5-test
BuildRequires:	python-qt5-webchannel
BuildRequires:	python-qt5-webengine
BuildRequires:	python-qt5-webengine-widgets
BuildRequires:	python-qt5-websockets
BuildRequires:	python-qt5-widgets
BuildRequires:	python-qt5-x11extras
BuildRequires:	python-qt5
BuildRequires:	python-qt5-devel
BuildRequires:	python-qt5-qscintilla
BuildRequires:	python-qt-builder
BuildRequires:	pkgconfig(gdal)
BuildRequires:	geos-devel
BuildRequires:	cmake(Qt5)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5Positioning)
BuildRequires:	cmake(Qt5Qml)
BuildRequires:	cmake(Qt5Quick)
BuildRequires:	cmake(Qt5QuickWidgets)
BuildRequires:	cmake(Qt5SerialPort)
BuildRequires:	cmake(Qt5Sql)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5UiTools)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	cmake(Qt5WebEngine)
BuildRequires:	cmake(Qt5WebEngineWidgets)
BuildRequires:	cmake(Qt5Xml)
BuildRequires:	cmake(Qt53DCore)
BuildRequires:	cmake(Qt53DRender)
BuildRequires:	cmake(Qt53DInput)
BuildRequires:	cmake(Qt53DLogic)
BuildRequires:	cmake(Qt53DExtras)
BuildRequires:	cmake(Qt5Multimedia)
BuildRequires:	cmake(Qt5MultimediaWidgets)
BuildRequires:	cmake(Qt5Keychain)
BuildRequires:	qmake5
BuildRequires:	pkgconfig(qca2-qt5)
BuildRequires:	pkgconfig(Qt5Qwt6)
BuildRequires:	pkgconfig(spatialite)
BuildRequires:	spatialindex-devel
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(draco)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(pdal)
BuildRequires:	pkgconfig(proj)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	cmake(libzip)
Obsoletes:	%{name}-theme-gis < 1.8.0

%description
Quantum GIS (QGIS) is designed to be a Geographic Information System (GIS)
built for Linux/Unix. QGIS will offer support for vector and raster formats.
Currently QGIS supports shapefiles and PostgreSQL/PostGIS layers.

Planned features include:

    * Read and edit shapefiles
    * Display georeferenced rasters (tiff, png, geotiff)
    * Plugins to dynamically add new functionality to the application
    * Support for database tables
    * Support for spatially enabled tables in PostgreSQL using PostGIS
    * Map output
    * Script engine
    * Metadata support

%files
%doc BUGS
%{_bindir}/qgis_bench
%{_bindir}/qgis_process
%{_bindir}/%{name}
%{_libdir}/lib%{name}_*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/crssync
%{_libdir}/%{name}/qgiscrashhandler
%{_libdir}/%{name}/*.so
%{_datadir}/%{name}/doc
%{_datadir}/applications/*.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/i18n
%{_datadir}/%{name}/images
%{_datadir}/%{name}/resources
%{_datadir}/%{name}/svg
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/*
%{_iconsdir}/hicolor/*/mimetypes/*
%{_datadir}/metainfo/org.qgis.qgis.appdata.xml

#---------------------------------------------------------

%package devel
Summary:	Development libraries and headers for QGIS
Group:		Sciences/Geosciences
Requires:	qgis
Obsoletes:	%{_lib}qgis-devel < 1.8.0
Conflicts:	qgis < 0.11.0
Conflicts:	qgiss-grass < 0.11.0

%description devel
Development headers for QGIS

%files devel
%{_includedir}/*
%{_libdir}/lib%{name}_*.so
%{_libdir}/libqgispython.so
%{_datadir}/%{name}/FindQGIS.cmake

#---------------------------------------------------------

%package grass
Summary:	QGIS plugins for accessing GRASS data
Group:		Sciences/Geosciences
Requires:	grass
Conflicts:	qgis < 0.11.0

%description grass
This package provides plugins for QGIS that provide access to GRASS data from
within QGIS.

%files grass

#---------------------------------------------------------

%package python
Summary:	Python integration and plugins for qgis
Group:		Sciences/Geosciences
Requires:	%{name} = %{version}-%{release}
Requires:	python-sip-qt5
Requires:	python-qt5
Conflicts:	qgis < 0.11.0

%description python
Python integration and plugins for qgis

%files python
%{_libdir}/libqgispython.so.*
%{_datadir}/%{name}/python

#---------------------------------------------------------

%prep
%autosetup -p1
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}
%cmake \
	-DQGIS_LIB_SUBDIR=%{_lib} \
	-DQGIS_PLUGIN_SUBDIR=%{_lib}/qgis \
	-DGRASS_PREFIX=%{_libdir}/%{grass} \
	-DWITH_QTWEBKIT=FALSE \
	-DWITH_QTWEBENGINE=TRUE \
	-DWITH_PDF4QT=TRUE \
	-G Ninja

%build
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}
%ninja_build -C build

%install
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}
%ninja_install -C build

mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_datadir}
