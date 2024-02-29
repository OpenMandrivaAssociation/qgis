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
# fixes for finding libs in the place we put them
Patch1:		qgis-3.36.0-qt_find.patch
# dont use the upstream pdf4qt name for our private copy
Patch2:		qgis-3.36.0-pdf4qt_private.patch
Patch3:		qgis-3.36.0-compile.patch
Source100:	%{name}.rpmlintrc
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	dos2unix
BuildRequires:	flex
BuildRequires:	grass
BuildRequires:	imagemagick
BuildRequires:	mlocate
BuildRequires:	opencl-headers
BuildRequires:	cmake(openclicdloader)
BuildRequires:	postgis
BuildRequires:  qscintilla-qt6-devel
BuildRequires:	python-sip-qt6
BuildRequires:	python-qt6-core
BuildRequires:	python-qt6-quick
BuildRequires:	python-qt6-xml
BuildRequires:	python-qt6-quickwidgets
BuildRequires:	python-qt6-bluetooth
BuildRequires:	python-qt6-dbus
BuildRequires:	python-qt6-designer
BuildRequires:	python-qt6-gui
BuildRequires:	python-qt6-multimedia
BuildRequires:	python-qt6-multimediawidgets
BuildRequires:	python-qt6-network
BuildRequires:	python-qt6-nfc
BuildRequires:	python-qt6-opengl
BuildRequires:	python-qt6-positioning
BuildRequires:	python-qt6-printsupport
BuildRequires:	python-qt6-qml
BuildRequires:	python-qt6-remoteobjects
BuildRequires:	python-qt6-sensors
BuildRequires:	python-qt6-serialport
BuildRequires:	python-qt6-sql
BuildRequires:	python-qt6-svg
BuildRequires:	python-qt6-test
BuildRequires:	python-qt6-webchannel
BuildRequires:	python-qt6-webengine
BuildRequires:	python-qt6-websockets
BuildRequires:	python-qt6-widgets
BuildRequires:	python-qt6
BuildRequires:	python-qt6-devel
BuildRequires:	python-qt6-qscintilla
BuildRequires:	python-qt-builder
BuildRequires:	pkgconfig(gdal)
BuildRequires:	geos-devel
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Positioning)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6SerialPort)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6UiPlugin)
BuildRequires:	cmake(Qt6UiTools)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt63DCore)
BuildRequires:	cmake(Qt63DRender)
BuildRequires:	cmake(Qt63DInput)
BuildRequires:	cmake(Qt63DLogic)
BuildRequires:	cmake(Qt63DExtras)
BuildRequires:	cmake(Qt6Multimedia)
BuildRequires:	cmake(Qt6MultimediaWidgets)
BuildRequires:	cmake(Qt6Keychain)
BuildRequires:	cmake(Qt6SvgWidgets)
BuildRequires:	qmake-qt6
BuildRequires:	cmake(qca-qt6)
BuildRequires:	pkgconfig(Qt6Qwt6)
BuildRequires:	pkgconfig(spatialite)
BuildRequires:	spatialindex-devel
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(draco)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(pdal)
BuildRequires:	pkgconfig(proj)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(libjpeg)
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
%{_libdir}/lib%{name}Pdf4QtLibCore.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/crssync
%{_libdir}/%{name}/qgiscrashhandler
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/pdal_wrench
%{_libdir}/%{name}/untwine
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
%{_libdir}/lib%{name}grass*.so
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
%{_libdir}/libqgisgrass*.so.*
%{_libdir}/%{name}/grass
%{_datadir}/%{name}/grass

#---------------------------------------------------------

%package python
Summary:	Python integration and plugins for qgis
Group:		Sciences/Geosciences
Requires:	%{name} = %{version}-%{release}
Requires:	python-sip-qt6
Requires:	python-qt6
Conflicts:	qgis < 0.11.0

%description python
Python integration and plugins for qgis

%files python
%{_libdir}/libqgispython.so.*
%{_datadir}/%{name}/python

#---------------------------------------------------------

%prep
%autosetup -p1
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}:$(pwd)/build/usr/lib
%cmake \
	-DQGIS_LIB_SUBDIR=%{_lib} \
	-DQGIS_PLUGIN_SUBDIR=%{_lib}/qgis \
	-DGRASS_PREFIX=%{_libdir}/%{grass} \
	-DWITH_QTWEBKIT=FALSE \
	-DBUILD_WITH_QT6=TRUE \
	-DWITH_QTWEBENGINE=TRUE \
	-DWITH_PDF4QT=TRUE \
	-G Ninja

%build
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}:$(pwd)/build/usr/lib
%ninja_build -C build

%install
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}:$(pwd)/build/usr/lib
%ninja_install -C build

mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_datadir}

mv %{buildroot}/usr/usr/lib/*.so.* %{buildroot}/%{_libdir}/
rm -Rf %{buildroot}/usr/usr
