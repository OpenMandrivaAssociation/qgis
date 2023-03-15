%global optflags %{optflags} -DPROTOBUF_USE_DLLS -flto=thin
# Doesn't build with -j16, does with -j12 or lower, we choose -j8
#global make %(cpus=%_smp_mflags;if [ "${cpus##-j}" -gt 8 ];then echo make -j8;else echo make $cpus;fi)

%define __noautoreq '.*libgrass_.*'

Summary:	Geographic Information System for Linux/Unix
Name:		qgis
Version:	3.30.0
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
BuildRequires:	python-sip
BuildRequires:  qscintilla-qt5-devel
BuildRequires:	python-qt5-qscintilla
BuildRequires:	pkgconfig(gdal)
BuildRequires:	geos-devel
BuildRequires:	cmake(Qt5)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5SerialPort)
BuildRequires:	cmake(Qt5Xml)
BuildRequires:	qmake5
BuildRequires:	pkgconfig(Qt5Qwt6)
BuildRequires:	pkgconfig(spatialite)
BuildRequires:	spatialindex-devel
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(netcdf)
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
Requires:	python-sip
Requires:	python-qt4
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
	-G Ninja

%build
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}
%ninja_build -C build

%install
export LD_LIBRARY_PATH=$(pwd)/build/output/%{_lib}
%ninja_install -C build

mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_datadir}
