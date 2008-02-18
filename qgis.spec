%define libmsexport %mklibname msexport 1
%define libnamegrass %mklibname %{name}grass 0
%define libqgis %mklibname qgis 0

%define _requires_exceptions .*libgrass_.*

Name: qgis
Version: 0.9.1
Release: %mkrel 3
Summary: Geographic Information System for Linux/Unix
Group: Sciences/Geosciences
URL: http://qgis.sourceforge.net/
Source:	http://prdownloads.sourceforge.net/qgis/%{name}_%{version}.tar.gz
License: GPL
Obsoletes: %{libqgis}
Obsoletes: %{libmsexport}
Requires: python-sip
Requires: python-qt4
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
BuildRequires: ImageMagick
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

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/*
# Shared libs. No more devel libs
%{_libdir}/*.so
%doc AUTHORS BUGS COPYING ChangeLog INSTALL README TODO
%exclude %{_libdir}/%{name}/*grass*.so
%exclude %_datadir/qgis/grass
%exclude %_libdir/libqgisgrass.so

#---------------------------------------------------------

%package devel
Summary: Development libraries and headers for QGIS
License: GPL
Group: Sciences/Geosciences
Requires: qgis
Obsoletes: %{_lib}qgis-devel

%description devel
Development headers for QGIS

%files devel
%defattr(-,root,root)
%{_includedir}/*

#---------------------------------------------------------

%package grass
Summary: QGIS plugins for accessing GRASS data
License: GPL
Group: Sciences/Geosciences
Obsoletes: %{libnamegrass}
Requires: grass

%description grass
This package provides plugins for QGIS that provide access to GRASS data from
within QGIS.

%files grass
%defattr(-,root,root)
%{_libdir}/%{name}/*grass*.so
%_datadir/qgis/grass
%_libdir/libqgisgrass.so

#---------------------------------------------------------

%prep
%setup -q -n %{name}_%{version}

%build

%cmake_qt4 \
	-DQGIS_LIB_SUBDIR=%_lib \
	-DQGIS_PLUGIN_SUBDIR=%_lib/qgis \
	-DGRASS_PREFIX=%_libdir/grass62 

%make

%install
rm -rf %buildroot
make -C build DESTDIR=%buildroot install

mv %buildroot/%_prefix/man %buildroot/%_datadir

mkdir -p %{buildroot}/%{_datadir}/applications
cat > %{buildroot}/%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Quantum GIS
Comment=Quantum Geographic Information System
Exec=LD_LIBRARY_PATH=%{_libdir}/%{grass}/lib GISBASE=%{_libdir}/%{grass} %{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Sciences-Geosciences;Science;
EOF

%clean
rm -rf $RPM_BUILD_ROOT


