# Doesnt build with -j16, does with -j12 or lower, we choose -j8
%global make %(cpus=%_smp_mflags;if [ "${cpus##-j}" -gt 8 ];then echo make -j8;else echo make $cpus;fi)

%define __noautoreq '.*libgrass_.*'

Summary:	Geographic Information System for Linux/Unix
Name:		qgis
Version:	3.16.1
Release:	1
License:	GPLv2+
Group:		Sciences/Geosciences
Url:		http://www.qgis.org/
Source0:	http://qgis.org/downloads/%{name}-%{version}.tar.bz2
Source1:        %{name}-mime.xml
Source100:	%{name}.rpmlintrc
#Patch1:		qgis-2.4.0-sip.patch
#Patch2:		qgis-2.4.0-grass.patch
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	flex
BuildRequires:	imagemagick
BuildRequires:	mlocate

BuildRequires:	python-sip
BuildRequires:	gdal-devel
BuildRequires:	geos-devel

BuildRequires:  pkgconfig(OpenCL)
#BuildRequires:  pkgconfig(Qt5Qwt6)
BuildRequires:  pkgconfig(Qt53DCore)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Positioning)
BuildRequires:  pkgconfig(Qt5QuickWidgets)
BuildRequires:  pkgconfig(Qt5SerialPort)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(Qt5UiTools)
BuildRequires:  pkgconfig(Qt5WebKit)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5XmlPatterns)
BuildRequires:	pkgconfig(libzip)
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(libpq)
BuildRequires:	pkgconfig(netcdf)
BuildRequires:	pkgconfig(proj)
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(pyqt5)
BuildRequires:	python-sip-qt5
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(qca2-qt5)
BuildRequires:	qscintilla-qt5-devel
BuildRequires:	python-qt5-qscintilla
BuildRequires:	pkgconfig(exiv2)
BuildRequires:	pkgconfig(proj)

Requires:	python-BioSQL
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
%{_datadir}/applications/*.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/i18n
%{_datadir}/%{name}/images
%{_datadir}/%{name}/resources
%{_datadir}/%{name}/svg
%{_datadir}/mime/packages/*
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/*
%{_iconsdir}/hicolor/*/mimetypes/*

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


%build
%cmake \
	-DQGIS_LIB_SUBDIR=%{_lib} \
	-DQGIS_PLUGIN_SUBDIR=%{_lib}/qgis \
	-DGRASS_PREFIX=%{_libdir}/%{grass}

%make

%install
%makeinstall_std -C build

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

mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_datadir}

desktop-file-install \
    --remove-mime-type="application/x-raster-ecw" \
    --remove-mime-type="application/x-raster-mrsid" \
    --dir=%{buildroot}%{_datadir}/applications \
    debian/qgis.desktop

desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    debian/qbrowser.desktop

# Install MIME type definitions
install -d %{buildroot}%{_datadir}/mime/packages
install -pm0644 %{SOURCE1} \
    %{buildroot}%{_datadir}/mime/packages/%{name}.xml

# Install application and MIME icons
install -pd %{buildroot}%{_datadir}/pixmaps
install -pd %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
install -pd %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pd %{buildroot}%{_datadir}/icons/hicolor/128x128/mimetypes
install -pm0644 \
    %{buildroot}%{_datadir}/%{name}/images/icons/%{name}-icon.png \
    %{buildroot}%{_datadir}/pixmaps/%{name}-icon.png
install -pm0644 \
    images/icons/%{name}-icon-16x16.png \
    %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}-icon.png
install -pm0644 \
    images/icons/%{name}_icon.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-icon.svg
install -pm0644 \
    %{buildroot}%{_datadir}/%{name}/images/icons/%{name}-mime-icon.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/mimetypes/application-x-qgis-layer-settings.png
install -pm0644 \
    %{buildroot}%{_datadir}/%{name}/images/icons/%{name}-mime-icon.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/mimetypes/application-x-qgis-project.png
