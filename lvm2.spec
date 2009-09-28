%define	name	lvm2
%define	lvmversion	2.02.53
%define dmversion 1.02.38
%define	release	%manbo_mkrel 1
%define	_usrsbindir	%{_prefix}/sbin
%define	_sbindir	/sbin
%define	dmmajor		1.02
%define	cmdmajor	2.02
%define	appmajor	2.1

%define	dmlibname	%mklibname devmapper %dmmajor
%define	dmdevelname	%mklibname devmapper -d
%define	event_libname	%mklibname devmapper-event %dmmajor
%define	event_develname	%mklibname devmapper-event -d
%define cmdlibname	%mklibname lvm2cmd %cmdmajor
%define cmddevelname	%mklibname lvm2cmd -d

%define	build_lvm2app 0
%define	build_cluster 1
%define	build_dmeventd 1

%{?_with_dmeventd: %{expand: %%global build_dmeventd 1}}
%{?_without_dmeventd: %{expand: %%global build_dmeventd 0}}
%{?_with_lvm2app: %{expand: %%global build_lvm2app 1}}
%{?_without_lvm2app: %{expand: %%global build_lvm2app 0}}
%{?_with_cluster: %{expand: %%global build_cluster 1}}
%{?_without_cluster: %{expand: %%global build_cluster 0}}

%if %build_lvm2app
%define	applibname	%mklibname lvm2app 2.1
%define appdevelname	%mklibname -d lvm2
%endif

Summary:	Logical Volume Manager administration tools
Name:		%{name}
Version:	%{lvmversion}
Release:	%{release}
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{lvmversion}.tgz
Source1:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{lvmversion}.tgz.asc
Patch0:		lvm2-2.02.53-alternatives.patch
Patch1:		lvm2-2.02.53-pkgconfig.patch
Patch2:		lvm2-2.02.53-vgmknodes-man.patch
Patch3:		lvm2-2.02.33-lvmconf-clvm-type3.patch
License:	GPL
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-%{lvmversion}-%{release}-buildroot
URL:		http://sources.redhat.com/lvm2/
BuildConflicts:	device-mapper-devel >= %{dmversion}
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
#BuildRequires:	autoconf
Conflicts:	lvm
Conflicts:	lvm1
BuildRequires:	glibc-static-devel
%if %build_dmeventd
Requires:	%{cmdlibname} = %{lvmversion}-%{release}
%endif

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.

%package -n	%{cmdlibname}
Summary:	LVM2 command line library
Group:		System/Kernel and hardware

%description -n	%{cmdlibname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.

%package -n	%{cmddevelname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{cmdlibname} = %{version}-%{release}
Provides:	liblvm2cmd-devel = %{version}-%{release}
Obsoletes:	%{mklibname lvm2cmd %cmdmajor -d}

%description -n	%{cmddevelname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.
This package contains the header files for building with lvm2cmd and lvm2app.

%if %build_lvm2app
%package -n	%{applibname}
Summary:	LVM2 application api library
Group:		System/Kernel and hardware

%description -n	%{applibname}
LVM2 application API

%package -n	%{appdevelname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	pkgconfig
Requires:	%{applibname} = %{version}-%{release}
Provides:	liblvm2app-devel = %{version}-%{release}
Obsoletes:	%{mklibname lvm2app %appmajor -d}

%description -n	%{appdevelname}
LVM2 application API
This package contains the header files for building with lvm2app.
%endif

%if %build_cluster
%package -n	clvmd
Summary:	cluster LVM daemon
Group:		System/Kernel and hardware
BuildRequires:	cluster-devel
#bluca 200909 openais support requires 1.0 openais/corosync
#BuildRequires:	openais-devel > 1.0
#BuildRequires:	corosync-devel > 1.0

%description -n	clvmd
clvmd is the daemon that distributes LVM metadata updates around a
cluster. It must be running on all nodes in the cluster and will give
an error if a node in the cluster does not have this daemon running.
%endif

%package -n	dmsetup
Summary:	Device mapper setup tool
Version:	%{dmversion}
Group:		System/Kernel and hardware
Provides:	device-mapper = %{dmversion}-%{release}
Provides:	dmeventd = %{dmversion}-%{release}
Requires:	%{dmlibname} = %{dmversion}-%{release}

%description -n	dmsetup
Dmsetup manages logical devices that use the device-mapper driver.  
Devices are created by loading a table that specifies a target for
each sector (512 bytes) in the logical device.

%package -n	%{dmlibname}
Summary:	Device mapper library
Version:	%{dmversion}
Group:		System/Kernel and hardware

%description -n	%{dmlibname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the shared libraries required for running
programs which use device-mapper.

%package -n	%{dmdevelname}
Summary:	Device mapper development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-devel = %{dmversion}-%{release}
Provides:	libdevmapper-devel = %{dmversion}-%{release}
Requires:	%{dmlibname} = %{dmversion}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper %dmmajor -d}

%description -n	%{dmdevelname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the header files and development libraries
for building programs which use device-mapper.

%if %{build_dmeventd}
%package -n	%{event_libname}
Summary:	Device mapper event library
Version:	%{dmversion}
Group:		System/Kernel and hardware

%description -n	%{event_libname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the shared libraries required for running
programs which use device-mapper-event.

%package -n	%{event_develname}
Summary:	Device mapper event development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-event-devel = %{dmversion}-%{release}
Provides:	libdevmapper-event-devel = %{dmversion}-%{release}
Requires:	%{event_libname} = %{dmversion}-%{release}
Requires:	%{dmdevelname} = %{dmversion}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-event-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper-event %dmmajor -d}

%description -n	%{event_develname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the header files and development libraries
for building programs which use device-mapper-event.
%endif

%prep
%setup -q -n LVM2.%{lvmversion}
%patch0 -p1 -b .alternatives
%patch1 -p1 -b .pkgconfig
%patch2 -p1 -b .vgmknodes-man
%patch3 -p1 -b .fixlvmconf

%build
%define common_configure_parameters --with-user=`id -un` --with-group=`id -gn` --disable-selinux --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660
export ac_cv_lib_dl_dlopen=no
%configure %{common_configure_parameters} \
	--enable-static_link --disable-readline \
	--with-cluster=none --with-pool=none
unset ac_cv_lib_dl_dlopen
%make
mv tools/dmsetup.static .
mv tools/lvm.static .
mv libdm/ioctl/libdevmapper.a .
%make clean

%configure %{common_configure_parameters} \
	--disable-static_link --enable-readline \
	--enable-fsadm --enable-pkgconfig \
	--enable-cmdlib \
%if %build_lvm2app
	--enable-applib \
%endif
%if %build_cluster
	--with-clvmd=cman \
%else
	--with-cluster=none \
	--with-pool=none \
%endif
%if %{build_dmeventd}
	--enable-dmeventd \
%endif
# 20090926 no translations yet:	--enable-nls
# 20090926 disabled for now: --enable-udev_sync --enable-udev_rules
# end of configure options
%make

%install
rm -rf %{buildroot}
%makeinstall sbindir=%{buildroot}/%{_sbindir} libdir=%{buildroot}/%{_lib} usrsbindir=%{buildroot}/%{_usrsbindir} confdir=%{buildroot}/etc/lvm/

install -d %{buildroot}/etc/lvm/archive
install -d %{buildroot}/etc/lvm/backup
install -d %{buildroot}/etc/lvm/cache
touch %{buildroot}/etc/lvm/cache/.cache

install -d %{buildroot}/var/lock/lvm

install -d %{buildroot}/%{_initrddir}

install scripts/lvm2_monitoring_init_red_hat %{buildroot}/%{_initrddir}/lvm2-monitor
%if %build_cluster
install scripts/clvmd_init_red_hat %{buildroot}/%{_initrddir}/clvmd
install -m 0755 scripts/lvmconf.sh %{buildroot}/%{_usrsbindir}/lvmconf
%endif

install lvm.static %{buildroot}/%{_sbindir}/lvm.static
install dmsetup.static %{buildroot}/%{_sbindir}/dmsetup.static
install -m 644 libdevmapper.a %{buildroot}/%{_libdir}
#compatibility links
ln %{buildroot}/%{_sbindir}/lvm %{buildroot}/%{_sbindir}/lvm2
ln %{buildroot}/%{_sbindir}/lvm.static %{buildroot}/%{_sbindir}/lvm2-static
ln %{buildroot}/%{_sbindir}/dmsetup.static %{buildroot}/%{_sbindir}/dmsetup-static

#move .so links in /usr/lib
for solink in %{buildroot}/%{_lib}/*.so; do
	if [ "${solink%%libdevmapper-event-lvm2*.so}" == "${solink}" ]; then
		_target=`readlink ${solink}`
		ln -s ../../%{_lib}/${_target##*/} %{buildroot}/%{_libdir}/${solink##*/}
		rm ${solink}
	fi
done

#hack permissions of libs
chmod u+w %{buildroot}/%{_lib}/*.so.* %{buildroot}/%{_sbindir}/* %{buildroot}/%{_usrsbindir}/*

%find_lang %name

#hack trick strip_and_check_elf_files
export LD_LIBRARY_PATH=%{buildroot}/%{_lib}:${LD_LIBRARY_PATH}

%pre
if [ -L /sbin/lvm -a -L /etc/alternatives/lvm ]; then
	update-alternatives --remove lvm /sbin/lvm2
fi

%if %mdkversion < 200900
%if %build_lvm2app
%post -n %{applibname} -p /sbin/ldconfig
%postun -n %{applibname} -p /sbin/ldconfig
%endif
%post -n %{dmlibname} -p /sbin/ldconfig
%postun -n %{dmlibname} -p /sbin/ldconfig
%post -n %{cmdlibname} -p /sbin/ldconfig
%postun -n %{cmdlibname} -p /sbin/ldconfig
%if %{build_dmeventd}
%post -n %{event_libname} -p /sbin/ldconfig
%postun -n %{event_libname} -p /sbin/ldconfig
%endif
%endif

%if %build_cluster
%post -n clvmd
%_post_service clvmd
%{_usrsbindir}/lvmconf --lockinglibdir %{_libdir}

%preun -n clvmd
%_preun_service clvmd
if [ "$1" = 0 ]; then
        %{_usrsbindir}/lvmconf --disable-cluster
fi
%endif

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(644,root,root,755)
%doc INSTALL README VERSION WHATS_NEW
%attr(755,root,root) %{_sbindir}/fsadm
%attr(755,root,root) %{_sbindir}/lv*
%attr(755,root,root) %{_sbindir}/pv*
%attr(755,root,root) %{_sbindir}/vg*
%config(noreplace) %{_initrddir}/lvm2-monitor
%dir %{_sysconfdir}/lvm
%config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%attr(700,root,root) %dir %{_sysconfdir}/lvm/archive
%attr(700,root,root) %dir %{_sysconfdir}/lvm/backup
%attr(700,root,root) %dir %{_sysconfdir}/lvm/cache
%attr(600,root,root) %ghost %{_sysconfdir}/lvm/cache/.cache
%attr(700,root,root) %dir /var/lock/lvm
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{cmdlibname}
%defattr(644,root,root,755)
/%{_lib}/liblvm2cmd.so.*
%if %{build_dmeventd}
/%{_lib}/libdevmapper-event-lvm2mirror.so*
/%{_lib}/libdevmapper-event-lvm2snapshot.so*
%endif

%files -n %{cmddevelname}
%defattr(644,root,root,755)
%{_includedir}/lvm2cmd.h
%attr(755,root,root) %{_libdir}/liblvm2cmd.so

%if %build_lvm2app
%files -n %{applibname}
%defattr(644,root,root,755)
/%{_lib}/liblvm2app.so.*

%files -n %{appdevelname}
%defattr(644,root,root,755)
%{_includedir}/lvm2app.h
%attr(755,root,root) %{_libdir}/liblvm2app.so
%{_libdir}/pkgconfig/lvm2app.pc
%endif

%if %build_cluster
%files -n clvmd
%defattr(755, root,root)
%config(noreplace) %{_initrddir}/clvmd
%{_usrsbindir}/clvmd
%{_usrsbindir}/lvmconf
%attr(644,root,root) %{_mandir}/man8/clvmd.8*
%endif

%files -n dmsetup
%defattr(644,root,root,755)
%doc INSTALL README VERSION_DM WHATS_NEW_DM
%attr(755,root,root) %{_sbindir}/dmsetup
%attr(755,root,root) %{_sbindir}/dmsetup.static
%attr(755,root,root) %{_sbindir}/dmsetup-static
%if %{build_dmeventd}
%attr(755,root,root) %{_sbindir}/dmeventd
%endif
%{_mandir}/man8/dmsetup.8*

%files -n %{dmlibname}
%defattr(755,root,root)
/%{_lib}/libdevmapper.so.*

%files -n %{dmdevelname}
%defattr(644,root,root,755)
%{_libdir}/libdevmapper.so
%{_libdir}/libdevmapper.a*
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%if %{build_dmeventd}
%defattr(755,root,root)
%files -n %{event_libname}
/%{_lib}/libdevmapper-event.so.*

%files -n %{event_develname}
%defattr(644,root,root,755)
%{_includedir}/libdevmapper-event.h
%{_libdir}/libdevmapper-event.so
%{_libdir}/pkgconfig/devmapper-event.pc
%endif

