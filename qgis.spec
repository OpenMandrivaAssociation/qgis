%{!?grass:%global grass grass62}
%define _requires_exceptions devel\(lib.*qgsprojectionselector.*\)
%global build_msexport 0

Name: qgis
Version: 0.8.1
Release: %mkrel 1
Summary: Quantum GIS is a Geographic Information System for Linux/Unix
Group: Sciences/Geosciences
URL: http://qgis.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/qgis/%{name}-%{version}.tar.gz
Patch0: qgis-0.8-python2.5.patch
Patch1: qgis-fix-lib64-grass-link-path.patch
Patch2: qgis-0.8.0-qt4.3_buildfix.patch	
License: GPL
BuildRequires: qt4-devel 
BuildRequires: qt4-linguist
BuildRequires: grass 
BuildRequires: gdal-devel 
BuildRequires: geos-devel
BuildRequires: proj-devel
BuildRequires: expat-devel
BuildRequires: gsl-devel
BuildRequires: cfitsio-devel 
BuildRequires: ImageMagick
BuildRequires: flex 
BuildRequires: byacc
BuildRequires: bison
BuildRequires: mlocate
BuildRequires: postgresql-devel
BuildRequires: netcdf-devel
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

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}_help
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/*
%doc AUTHORS BUGS COPYING ChangeLog INSTALL README TODO
%exclude %{_libdir}/%{name}/*grass*.so

#---------------------------------------------------------

%define major	0
%define libname %mklibname %name %major

%package -n %{libname}
Summary:	Library package for QGIS
License:	GPL
Group:		Sciences/Geosciences

%description -n %{libname}
Library package for QGIS

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{name}_*.so.*
%{_libdir}/%{name}/libqgsprojectionselector.so

#---------------------------------------------------------

%package -n %{libname}-devel
Summary:	Development libraries and headers for QGIS
License:	GPL
Group:		Sciences/Geosciences
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
Development libraries and headers for QGIS

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/%{name}/*.la
%{_includedir}/%{name}
%{_datadir}/aclocal/%{name}.m4

#---------------------------------------------------------

%define libnamegrass %mklibname %{name}grass %major

%package -n %{libnamegrass}
Summary:	QGIS plugins for accessing GRASS data
License:	GPL
Group:		Sciences/Geosciences

%description -n %{libnamegrass}
This package provides plugins for QGIS that provide access to GRASS data from
within QGIS.

%files -n %{libnamegrass}
%defattr(-,root,root)
%{_libdir}/*%{name}grass.so.*
%exclude %{_libdir}/*%{name}grass.so
%{_libdir}/%{name}/*grass*.so
%{_libdir}/*%{name}grass.la

#---------------------------------------------------------

%define libmsexport %mklibname msexport 1
%if %build_msexport
%package -n %libmsexport
Summary: QGIS export library
License: GPL
Group: Sciences/Geosciences
Provides: msexport

%description -n %libmsexport
Summary: QGIS export library

%post -n %libmsexport -p /sbin/ldconfig
%postun -n %libmsexport -p /sbin/ldconfig

%files -n %libmsexport
%defattr(-,root,root,-)
%_bindir/msexport
%_libdir/libmsexport.so.*
%endif

#---------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .python25
%patch1 -p0 -b .fix-lib64-grass-link-path
%patch2 -p1 -b .qt4.3_buildfix

%build
export QTDIR=%{qt4dir}
export PATH=%{qt4dir}/bin:${PATH}
export PKG_CONFIG_PATH=%{qt4lib}/pkgconfig
export GISLIB=%{_libdir}/%{grass}/lib/libgrass_gis.so

aclocal && libtoolize -c -f && autoheader && automake -a -c && autoconf

%configure  \
    --with-grass=%{_libdir}/%{grass} \
    --with-qtdir=%{qt4dir} \
    --with-python \
    --disable-static

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

find %{buildroot} -size 0 -exec rm -f {} \;

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

sed -i -e "s,-L`pwd`/providers/grass ,,g" %{buildroot}/%{_libdir}/%{name}/grassplugin.la


%clean
rm -rf $RPM_BUILD_ROOT


