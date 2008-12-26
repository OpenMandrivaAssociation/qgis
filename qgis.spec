%define libmsexport %mklibname msexport 1
%define libnamegrass %mklibname %{name}grass 0
%define libqgis %mklibname qgis 0
%define grass grass62

%define _requires_exceptions .*libgrass_.*

Name: qgis
Version: 0.11.0
Release: %mkrel 2
Summary: Geographic Information System for Linux/Unix
Group: Sciences/Geosciences
URL: http://www.qgis.org/
Source:	http://download.osgeo.org/qgis/src/qgis_%{version}.tar.gz
License: GPLv2+
Obsoletes: %{libqgis}
Obsoletes: %{libmsexport}
Requires: python-BioSQL
Requires: postgis
BuildRequires: cmake
BuildRequires: grass 
BuildRequires: gdal-devel 
BuildRequires: geos-devel
BuildRequires: proj-devel
BuildRequires: expat-devel
BuildRequires: gsl-devel
BuildRequires: cfitsio-devel 
BuildRequires: imagemagick
BuildRequires: flex 
BuildRequires: bison
BuildRequires: mlocate
BuildRequires: postgresql-devel
BuildRequires: postgis-devel
BuildRequires: netcdf-devel
BuildRequires: qt4-devel 
BuildRequires: qt4-linguist
BuildRequires: python-sip
BuildRequires: python-qt4
BuildRequires: python-BioSQL
BuildRequires: imagemagick
%py_requires -d
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}_help
%{_libdir}/lib%{name}_*.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libcopyrightlabelplugin.so
%{_libdir}/%{name}/libdelimitedtextplugin.so
%{_libdir}/%{name}/libdelimitedtextprovider.so
%{_libdir}/%{name}/libgeorefplugin.so
%{_libdir}/%{name}/libgpsimporterplugin.so
%{_libdir}/%{name}/libgpxprovider.so
%{_libdir}/%{name}/libgridmakerplugin.so
%{_libdir}/%{name}/libmemoryprovider.so
%{_libdir}/%{name}/libnortharrowplugin.so
%{_libdir}/%{name}/libogrprovider.so
%{_libdir}/%{name}/libpggeoprocessingplugin.so
%{_libdir}/%{name}/libpostgresprovider.so
%{_libdir}/%{name}/libquickprintplugin.so
%{_libdir}/%{name}/libscalebarplugin.so
%{_libdir}/%{name}/libspitplugin.so
%{_libdir}/%{name}/libwfsplugin.so
%{_libdir}/%{name}/libwfsprovider.so
%{_libdir}/%{name}/libwmsprovider.so
%{_datadir}/%{name}/doc
%{_datadir}/applications/mandriva-%{name}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/i18n
%{_datadir}/%{name}/images
%{_datadir}/%{name}/resources
%{_datadir}/%{name}/svg
%dir %{_datadir}/%{name}/themes
%dir %{_datadir}/%{name}/themes/default
%{_datadir}/%{name}/themes/default/*.png
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/*
%doc AUTHORS BUGS ChangeLog README TODO

#---------------------------------------------------------

%package devel
Summary: Development libraries and headers for QGIS
Group: Sciences/Geosciences
Requires: qgis
Obsoletes: %{_lib}qgis-devel
Conflicts: qgis < 0.11.0
Conflicts: qgiss-grass < 0.11.0
%description devel
Development headers for QGIS

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/lib%{name}_*.so
%{_libdir}/libqgisgrass.so
%{_libdir}/libqgispython.so

#---------------------------------------------------------

%package grass
Summary: QGIS plugins for accessing GRASS data
Group: Sciences/Geosciences
Obsoletes: %{libnamegrass}
Requires: grass
Conflicts: qgis < 0.11.0

%description grass
This package provides plugins for QGIS that provide access to GRASS data from
within QGIS.

%files grass
%defattr(-,root,root)
%{_libdir}/libqgisgrass.so.*
%{_libdir}/%{name}/libgrass*.so
%{_datadir}/%{name}/grass
%{_datadir}/%{name}/themes/default/grass

#---------------------------------------------------------

%package python
Summary: Python integration and plugins for qgis
Group: Sciences/Geosciences
Requires: %{name} = %{version}-%{release}
Requires: python-sip
Requires: python-qt4
Conflicts: qgis < 0.11.0

%description python
Python integration and plugins for qgis

%files python
%defattr(-,root,root)
%{_libdir}/libqgispython.so.*
%{_datadir}/%{name}/python

#---------------------------------------------------------

%package theme-nkids
Summary: Addtional theme for qgis - nkids
Group: Sciences/Geosciences
Requires: %{name} = %{version}-%{release}
Conflicts: qgis < 0.11.0

%description theme-nkids
Addtional theme for qgis - nkids

%files theme-nkids
%defattr(-, root, root, -)
%{_datadir}/%{name}/themes/nkids

#---------------------------------------------------------

%prep
%setup -q -n %{name}_%{version}

%build

%cmake_qt4 \
	-DQGIS_LIB_SUBDIR=%{_lib} \
	-DQGIS_PLUGIN_SUBDIR=%{_lib}/qgis \
	-DGRASS_PREFIX=%{_libdir}/%{grass}

%make

%install
rm -rf %{buildroot}
make -C build DESTDIR=%{buildroot} install

mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_datadir}

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Quantum GIS
Comment=Quantum Geographic Information System
Exec=LD_LIBRARY_PATH=%{_libdir}/%{grass}/lib GISBASE=%{_libdir}/%{grass} %{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Science;Geoscience;
EOF

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
convert -scale 48 %{buildroot}%{_datadir}/%{name}/doc/images/qgis_new_80pct.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{buildroot}%{_datadir}/%{name}/doc/images/qgis_new_80pct.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{buildroot}%{_datadir}/%{name}/doc/images/qgis_new_80pct.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%clean
rm -rf %{buildroot}


