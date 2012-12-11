# Doesnt build with -j16, does with -j12 or lower, we choose -j8
%global make %(cpus=%_smp_mflags;if [ "${cpus##-j}" -gt 8 ];then echo make -j8;else echo make $cpus;fi)

#define _requires_exceptions .*libgrass_.*
%define __noautoreq '.*libgrass_.*'

Name:		qgis
Version:	1.8.0
Release:	3
Summary:	Geographic Information System for Linux/Unix
Group:		Sciences/Geosciences
URL:		http://www.qgis.org/
Source0:	http://qgis.org/downloads/qgis-%{version}.tar.bz2
Patch0:		qgis-1.8.0-datasource-crash.patch
Patch1:		qgis-1.8.0-sip410.patch
License:	GPLv2+
Requires:	python-BioSQL
Requires:	postgis
Obsoletes:	%{name}-theme-gis < 1.8.0
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	flex
BuildRequires:	grass
BuildRequires:	imagemagick
BuildRequires:	mlocate
BuildRequires:	postgis
BuildRequires:	python-sip
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(proj)
BuildRequires:	pkgconfig(spatialite)
BuildRequires:	gdal-devel
BuildRequires:	geos-devel
BuildRequires:	libqwt-devel
BuildRequires:	netcdf-devel
BuildRequires:	postgresql-devel
BuildRequires:	python-BioSQL
BuildRequires:	python-qt4-devel
BuildRequires:	qt4-devel
BuildRequires:	qt4-linguist
BuildRequires:	spatialindex-devel
%py_requires -d

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
%doc BUGS README TODO
%{_bindir}/qbrowser
%{_bindir}/qgis_bench
%{_libdir}/%{name}/crssync
%{_bindir}/%{name}
%{_libdir}/%{name}/qgis_help
%{_libdir}/lib%{name}_*.so.*
# this might go in its own subpkg???
%{_libdir}/lib%{name}sqlanyconnection*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%exclude %{_libdir}/%{name}/libgrass*.so
%{_datadir}/%{name}/doc
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/i18n
%{_datadir}/%{name}/images
%{_datadir}/%{name}/resources
%{_datadir}/%{name}/svg
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/*

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
%{_libdir}/libqgisgrass.so
%{_libdir}/libqgispython.so
%{_libdir}/lib%{name}sqlanyconnection*.so
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
%{_libdir}/libqgisgrass.so.*
%{_libdir}/%{name}/libgrass*.so
%{_libdir}/%{name}/grass
%{_datadir}/%{name}/grass

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
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1

%build
%cmake_qt4 \
	-DQGIS_LIB_SUBDIR=%{_lib} \
	-DQGIS_PLUGIN_SUBDIR=%{_lib}/qgis \
	-DGRASS_PREFIX=%{_libdir}/%{grass}

%make

%install
%makeinstall_std -C build

mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_datadir}

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Quantum GIS
Comment=Quantum Geographic Information System
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Science;Geoscience;Qt;
EOF

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 %{buildroot}%{_datadir}/%{name}/doc/images/qgis_new_80pct.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{buildroot}%{_datadir}/%{name}/doc/images/qgis_new_80pct.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}%{_datadir}/%{name}/doc/images/qgis_new_80pct.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
