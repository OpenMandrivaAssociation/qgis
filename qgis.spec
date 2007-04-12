%define name	qgis
%define major	0
%define libname %mklibname %name %major
%define libnamegrass %mklibname %{name}grass %major
%define __libtoolize /bin/true
%define release %mkrel 5
%{!?grass:%global grass grass62}
%define _requires_exceptions devel\(lib.*qgsprojectionselector.*\)

Name:         	qgis
Version: 	0.8.0
Release:	%release
License:	GPL
Group:		Sciences/Geosciences
Source:		http://prdownloads.sourceforge.net/qgis/%{name}-%{version}.tar.gz
URL:		http://qgis.sourceforge.net/
Summary:	Quantum GIS is a Geographic Information System for Linux/Unix
BuildRequires:	qt4-devel grass gdal-devel cfitsio-devel ImageMagick
BuildRequires:	flex netcdf-devel qt4-linguist
Requires:	%{libname} = %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Patch:		qgis-0.7.4-gcc41.patch
Patch1:		qgis-0.7.4-gcc41-2.patch
Patch2:		qgis-0.8-python2.5.patch
Patch3:		qgis-fix-lib64-grass-link-path.patch

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

%package -n %{libname}
Summary:	Library package for QGIS
License:	GPL
Group:		Sciences/Geosciences

%description -n %{libname}
Library package for QGIS

%package -n %{libname}-devel
Summary:	Development libraries and headers for QGIS
License:	GPL
Group:		Sciences/Geosciences
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
Development libraries and headers for QGIS

%package -n %{libnamegrass}
Summary:	QGIS plugins for accessing GRASS data
License:	GPL
Group:		Sciences/Geosciences

%description -n %{libnamegrass}
This package provides plugins for QGIS that provide access to GRASS data from
within QGIS.

%prep
%setup -q
#patch -p1 -b .gcc41
#patch1 -b .gcc41-2
%patch2 -p1 -b .python25
%patch3 -p0 -b .fix-lib64-grass-link-path
automake
autoconf

%build
export QTDIR=%{_prefix}/lib/qt4
export PATH="$PATH:%{_libdir}/qt4/bin"
export GISLIB=%{_libdir}/%{grass}/lib/libgrass_gis.so
%configure --with-grass=%{_libdir}/%{grass} --with-qtdir=$QTDIR \
#--with-python
make
#strip src/qgis

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

find %{buildroot} -size 0 -exec rm -f {} \;

mkdir -p %{buildroot}/%{_menudir}
cat >> %{buildroot}/%{_menudir}/%{name} << EOF
?package(%{name}):\
command="LD_LIBRARY_PATH=%{_libdir}/%{grass}/lib GISBASE=%{_libdir}/%{grass} %{_bindir}/%{name}" \
icon="%{name}.png" \
needs="x11" \
section="More Applications/Sciences/Geosciences" \
title="Quantum GIS" \
longtitle="Quantum Geographic Information System" \
xdg="true"
EOF

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

mkdir -p %{buildroot}/{%{_iconsdir},%{_miconsdir},%{_liconsdir}}
convert -resize 48x48 %{buildroot}/%{_datadir}/%{name}/images/icons/qgis-icon.png %{buildroot}/%{_liconsdir}/%{name}.png
convert -resize 32x32 %{buildroot}/%{_datadir}/%{name}/images/icons/qgis-icon.png %{buildroot}/%{_iconsdir}/%{name}.png
convert -resize 16x16 %{buildroot}/%{_datadir}/%{name}/images/icons/qgis-icon.png %{buildroot}/%{_miconsdir}/%{name}.png

sed -i -e "s,-L`pwd`/providers/grass ,,g" %{buildroot}/%{_libdir}/%{name}/grassplugin.la

%post
%update_menus

%postun
%clean_menus

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_bindir}/%{name}_help
#%{_bindir}/gridmaker
#%{_bindir}/spit
#%{_bindir}/gpsimporter
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%exclude %{_libdir}/%{name}/*grass*.so
%{_datadir}/%{name}
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/*
%doc AUTHORS BUGS COPYING ChangeLog INSTALL README TODO

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{name}_*.so.*
%{_libdir}/*%{name}_*.la
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/libqgsprojectionselector.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_libdir}/*%{name}_*.so
%{_libdir}/*%{name}_*.a
%{_libdir}/%{name}/*.a
#%{_libdir}/%{name}/designer
%{_includedir}/%{name}
%{_datadir}/aclocal/%{name}.m4

%files -n %{libnamegrass}
%defattr(-,root,root)
%{_libdir}/*%{name}grass.so.*
%exclude %{_libdir}/*%{name}grass.so
%{_libdir}/%{name}/*grass*.so
%{_libdir}/*%{name}grass.la
%exclude %{_libdir}/*%{name}grass.a


