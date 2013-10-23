%define build_lvm2app 1
%define build_cluster 0
%define build_dmeventd 1
%bcond_without uclibc
%bcond_without crosscompile

%{?_with_dmeventd: %{expand: %%global build_dmeventd 1}}
%{?_without_dmeventd: %{expand: %%global build_dmeventd 0}}
%{?_with_lvm2app: %{expand: %%global build_lvm2app 1}}
%{?_without_lvm2app: %{expand: %%global build_lvm2app 0}}
%{?_with_cluster: %{expand: %%global build_cluster 1}}
%{?_without_cluster: %{expand: %%global build_cluster 0}}

%define _udevdir /lib/udev/rules.d
%define lvmversion	2.02.98
%define dmversion	1.02.77
%define dmmajor		1.02
%define cmdmajor	2.02
%define appmajor	2.2

%define dmlibname	%mklibname devmapper %{dmmajor}
%define dmdevname	%mklibname devmapper -d
%define event_libname	%mklibname devmapper-event %{dmmajor}
%define event_devname	%mklibname devmapper-event -d
%define cmdlibname	%mklibname lvm2cmd %{cmdmajor}
%define cmddevname	%mklibname lvm2cmd -d
%if %build_lvm2app
%define applibname	%mklibname lvm2app %{appmajor}
%define appdevname	%mklibname -d lvm2
%endif

#requirements for cluster
%define corosync_version 1.2.0
%define openais_version 1.1.1
%define cluster_version 3.0.6

%if %build_dmeventd
%define dm_req %{event_libname}
%define dm_req_d %{event_devname}
%else
%define dm_req %{dmlibname}
%define dm_req_d %{dmdevname}
%endif

Summary:	Logical Volume Manager administration tools
Name:		lvm2
Version:	2.02.98
Release:	5
License:	GPLv2 and LGPL2.1
Group:		System/Kernel and hardware
Url:		http://sources.redhat.com/lvm2/
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{lvmversion}.tgz
Source2:	%{name}-tmpfiles.conf
Patch0:		LVM2.2.02.98-alternatives.patch
Patch1:		lvm2-2.02.77-qdiskd.patch
Patch2:		lvm2-2.02.97-vgmknodes-man.patch
Patch5:		lvm2-2.02.77-preferred_names.patch
Patch6:		lvm2-2.02.97-make-sure-variable-gets-set.patch

BuildRequires:	sed
BuildConflicts:	device-mapper-devel < %{dmversion}
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif
%if %build_dmeventd
# install plugins as well
Requires:	%{cmdlibname} = %{lvmversion}-%{release}
%endif
Requires:	%{dm_req} >= %{dmversion}
%if %mdvver >= 201200
BuildRequires:	systemd-units
Requires(post): systemd
%endif
Conflicts:	lvm
Conflicts:	lvm1

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.

%if %{with uclibc}
%package -n	uclibc-%{name}
Summary:	Logical Volume Manager administration tools (uClibc linked)
Group:		System/Kernel and hardware

%description -n	uclibc-%{name}
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.
%endif

%package -n	%{cmdlibname}
Summary:	LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{dm_req} >= %{dmversion}
# Avoid devel deps on library due to autoreq picking these plugins up as devel libs
%define __noautoreqfiles	'libdevmapper-event-lvm2(mirror|raid|snapshot).so'

%description -n	%{cmdlibname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.

%if %{with uclibc}
%package -n	uclibc-%{cmdlibname}
Summary:	LVM2 command line library (uClibc linked)
Group:		System/Kernel and hardware
Requires:	uclibc-%{dm_req} >= %{dmversion}
# Avoid devel deps on library due to autoreq picking these plugins up as devel libs
%define __noautoreqfiles	'libdevmapper-event-lvm2(mirror|raid|snapshot).so'

%description -n	uclibc-%{cmdlibname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.
%endif

%package -n	%{cmddevname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{cmdlibname} = %{lvmversion}-%{release}
Requires:	%{dm_req_d} = %{dmversion}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{cmdlibname} = %{lvmversion}-%{release}
%endif
Provides:	liblvm2cmd-devel = %{lvmversion}-%{release}
Obsoletes:	%{mklibname lvm2cmd %cmdmajor -d} < %{lvmversion}-%{release}

%description -n	%{cmddevname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.
This package contains the header files for building with lvm2cmd and lvm2app.

%if %build_lvm2app
%package -n	%{applibname}
Summary:	LVM2 application api library
Group:		System/Kernel and hardware
Requires:	%{dm_req} >= %{dmversion}
Obsoletes:	%{mklibname lvm2app 2.1}

%description -n	%{applibname}
LVM2 application API.

%package -n	%{appdevname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{applibname} = %{lvmversion}-%{release}
Requires:	%{dm_req_d} = %{dmversion}-%{release}
Provides:	liblvm2app-devel = %{lvmversion}-%{release}
Obsoletes:	%{mklibname lvm2app %appmajor -d}

%description -n	%{appdevname}
LVM2 application API
This package contains the header files for building with lvm2app.
%endif

%if %build_cluster
%package -n	clvmd
Summary:	cluster LVM daemon
Group:		System/Kernel and hardware
BuildRequires:	cluster-devel >= %{cluster_version}
BuildRequires:	openais-devel >= %{openais_version}
BuildRequires:	corosync-devel >= %{corosync_version}
Requires:	cman >= %{cluster_version}
Requires:	%{dm_req} >= %{dmversion}

%description -n	clvmd
clvmd is the daemon that distributes LVM metadata updates around a
cluster. It must be running on all nodes in the cluster and will give
an error if a node in the cluster does not have this daemon running.

%package -n	cmirror
Summary:	Daemon for device-mapper-based clustered mirrors
Group:		System/Kernel and hardware
BuildRequires:	cluster-devel >= %{cluster_version}
BuildRequires:	openais-devel >= %{openais_version}
BuildRequires:	corosync-devel >= %{corosync_version}
Requires:	cman >= %{cluster_version}
Requires:	openais >= %{openais_version}
Requires:	corosync >= %{corosync_version}
Requires:	%{dmlibname} >= %{dmversion}

%description -n	cmirror
Daemon providing device-mapper-based mirrors in a shared-storage cluster.
%endif

%package -n	dmsetup
Summary:	Device mapper setup tool
Version:	%{dmversion}
Group:		System/Kernel and hardware
Provides:	device-mapper = %{dmversion}-%{release}
%if %{build_dmeventd}
Provides:	dmeventd = %{dmversion}-%{release}
%endif
Requires:	%{dm_req} = %{dmversion}-%{release}
%if %mdvver >= 201200
BuildRequires:	pkgconfig(udev) >= 195
%else
BuildRequires:	pkgconfig(udev)
%endif
Requires:	udev
Requires(pre):	rpm-helper

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

%if %{with uclibc}
%package -n	uclibc-%{dmlibname}
Summary:	Device mapper library (uClibc linked)
Version:	%{dmversion}
Group:		System/Kernel and hardware
#(tpg) in case of fire...
#ifarch %ix68
#define __noautoreqfiles	'libudev.so.1'
#endif

%description -n	uclibc-%{dmlibname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the shared libraries required for running
programs which use device-mapper.
%endif

%if %{with uclibc}
%package -n	uclibc-dmsetup
Summary:	Device mapper setup tool (uClibc linked)
Version:	%{dmversion}
Group:		System/Kernel and hardware
Requires:	udev

%description -n	uclibc-dmsetup
Dmsetup manages logical devices that use the device-mapper driver.  
Devices are created by loading a table that specifies a target for
each sector (512 bytes) in the logical device.
%endif

%package -n	%{dmdevname}
Summary:	Device mapper development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-devel = %{dmversion}-%{release}
Provides:	libdevmapper-devel = %{dmversion}-%{release}
Requires:	%{dmlibname} = %{dmversion}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{dmlibname} = %{dmversion}-%{release}
%endif
Requires:	pkgconfig
Conflicts:	device-mapper-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper %dmmajor -d}

%description -n	%{dmdevname}
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
Provides:	device-mapper-event = %{dmversion}-%{release}
Provides:	libdevmapper-event = %{dmversion}-%{release}
Requires:	%{dmlibname} >= %{dmversion}

%description -n	%{event_libname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the shared libraries required for running
programs which use device-mapper-event.

%if %{with uclibc}
%package -n	uclibc-%{event_libname}
Summary:	Device mapper event library (uClibc linked)
Version:	%{dmversion}
Group:		System/Kernel and hardware
Requires:	uclibc-%{dmlibname} = %{EVRD}

%description -n	uclibc-%{event_libname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the shared libraries required for running
programs which use device-mapper-event.
%endif

%package -n	%{event_devname}
Summary:	Device mapper event development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-event-devel = %{dmversion}-%{release}
Requires:	%{event_libname} = %{dmversion}-%{release}
Requires:	%{dmdevname} = %{dmversion}-%{release}
%if %{with uclibc}
Requires:	%{event_libname} = %{dmversion}-%{release}
Requires:	%{dmdevname} = %{dmversion}-%{release}
%endif
Conflicts:	device-mapper-event-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper-event %dmmajor -d}

%description -n	%{event_devname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the header files and development libraries
for building programs which use device-mapper-event.
%endif

%prep
%setup -qn LVM2.%{lvmversion}
%apply_patches

%build
%if %{with crosscompile}
export ac_cv_func_malloc_0_nonnull=yes
export ac_cv_func_realloc_0_nonnull=yes
%endif
%ifarch %arm
export ac_cv_func_malloc_0_nonnull=yes
%endif
datelvm=`awk -F '[.() ]*' '{printf "%s.%s.%s:%s\n", $1,$2,$3,$(NF-1)}' VERSION`
datedm=`awk -F '[.() ]*' '{printf "%s.%s.%s:%s\n", $1,$2,$3,$(NF-1)}' VERSION_DM`
if [ "${datelvm%:*}" != "%{lvmversion}" -o "${datedm%:*}" != "%{dmversion}" -o \
 "%{release}" = "1" -a "${datelvm#*:}" != "${datedm#*:}" ]; then
	echo "ERROR:	you should not be touching this package" 1>&2
	echo "	without full understanding of relationship between device-mapper" 1>&2
	echo "	and lvm2 versions" 1>&2
	exit 1
fi
%if %{build_dmeventd}
%define _disable_ld_as_needed 1
%endif
%define common_configure_parameters --with-user=`id -un` --with-group=`id -gn` --disable-selinux --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660
export ac_cv_lib_dl_dlopen=no
export MODPROBE_CMD=/sbin/modprobe
export CONFIGURE_TOP=".."

unset ac_cv_lib_dl_dlopen

%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--with-optimisation="" \
	%{common_configure_parameters} \
	--libdir=%{uclibc_root}/%{_lib} \
	--with-usrlibdir=%{uclibc_root}%{_libdir} \
	--sbindir=%{uclibc_root}/sbin \
	--enable-static_link \
	--disable-readline \
	--with-cluster=none \
	--with-pool=none \
%if %{build_dmeventd}
	--enable-cmdlib \
	--enable-dmeventd \
	--with-dmeventd-path=/sbin/dmeventd \
%endif
	--enable-udev_sync \
	--enable-udev_rules \
	--with-udevdir=%{_udevdir} \
	--with-systemdsystemunitdir=%{_unitdir}
%make V=1
popd

%else
mkdir -p static
pushd static
%configure2_5x %{common_configure_parameters} \
	--enable-static_link \
	--disable-readline \
	--with-cluster=none \
	--with-pool=none
sed -e 's/\ -static/ -static -Wl,--no-export-dynamic/' -i tools/Makefile
%make
popd
%endif

mkdir -p shared
pushd shared
%configure2_5x %{common_configure_parameters} \
	--sbindir=/sbin \
	--disable-static_link \
	--enable-readline \
	--enable-fsadm \
	--enable-pkgconfig \
	--with-usrlibdir=%{_libdir} \
	--libdir=/%{_lib} \
	--enable-cmdlib \
%if %build_lvm2app
	--enable-applib \
%endif
%if %build_cluster
	--with-clvmd=cman,openais,corosync \
	--enable-cmirrord \
%else
	--with-cluster=none \
	--with-pool=none \
%endif
%if %{build_dmeventd}
	--enable-dmeventd \
	--with-dmeventd-path=/sbin/dmeventd \
%endif
	--enable-udev_sync \
	--enable-udev_rules \
	--with-udevdir=%{_udevdir} \
	--with-systemdsystemunitdir=%{_unitdir}
# 20090926 no translations yet:	--enable-nls
# end of configure options
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
rm -f %{buildroot}%{uclibc_root}%{_libdir}/{liblvm2cmd,libdevmapper-event*}.a
%endif

%makeinstall_std -C shared
%if %mdvver >= 201200
make -C shared install_systemd_units DESTDIR=%{buildroot}
make -C shared install_tmpfiles_configuration DESTDIR=%{buildroot}
%endif

install -m644 %{SOURCE2} -D %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
install -d %{buildroot}/etc/lvm/archive
install -d %{buildroot}/etc/lvm/backup
install -d %{buildroot}/etc/lvm/cache
touch %{buildroot}/etc/lvm/cache/.cache

install -d %{buildroot}/run/lock/lvm

%if %mdvver >= 201200
%else
install shared/scripts/lvm2_monitoring_init_red_hat -E %{buildroot}%{_initrddir}/lvm2-monitor
%if %build_cluster
install shared/scripts/clvmd_init_red_hat %{buildroot}%{_initrddir}/clvmd
install shared/scripts/cmirrord_init_red_hat %{buildroot}%{_initrddir}/cmirrord
%endif
%endif

%if %build_cluster
install -m 0755 scripts/lvmconf.sh %{buildroot}/sbin/lvmconf
%endif

%if %{with uclibc}
mv %{buildroot}%{uclibc_root}%{_sbindir}/*static %{buildroot}/sbin
%else
install static/tools/lvm.static -D %{buildroot}/sbin/lvm.static
install static/tools/dmsetup.static -D %{buildroot}/sbin/dmsetup.static
%endif

#install -d %{buildroot}/%{_libdir}/
#compatibility links
ln %{buildroot}/sbin/lvm %{buildroot}/sbin/lvm2
ln %{buildroot}/sbin/lvm.static %{buildroot}/sbin/lvm2-static
ln %{buildroot}/sbin/dmsetup.static %{buildroot}/sbin/dmsetup-static

%if %{with uclibc}
ln %{buildroot}%{uclibc_root}/sbin/lvm %{buildroot}%{uclibc_root}/sbin/lvm2
%endif

#hack permissions of libs
chmod u+w %{buildroot}/%{_lib}/*.so.* %{buildroot}/sbin/*
%if %build_cluster
chmod u+w  %{buildroot}/sbin/*
%endif


#hack trick strip_and_check_elf_files
export LD_LIBRARY_PATH=%{buildroot}/%{_lib}:${LD_LIBRARY_PATH}

rm -f %{buildroot}/sbin/dmeventd.static

%pre
if [ -L /sbin/lvm -a -L /etc/alternatives/lvm ]; then
	update-alternatives --remove lvm /sbin/lvm2
fi

%if %build_cluster
%post -n clvmd
%_post_service clvmd
/sbin/lvmconf --lockinglibdir %{_libdir}

%preun -n clvmd
%_preun_service clvmd
if [ "$1" = 0 ]; then
	/sbin/lvmconf --disable-cluster
fi

%post -n cmirror
%_post_service cmirror

%preun -n cmirror
%_preun_service cmirror
%endif

%files
%doc INSTALL README VERSION WHATS_NEW
/sbin/blkdeactivate
/sbin/fsadm
/sbin/lv*
/sbin/pv*
/sbin/vg*
%dir %{_sysconfdir}/lvm
%config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%attr(700,root,root) %dir %{_sysconfdir}/lvm/archive
%attr(700,root,root) %dir %{_sysconfdir}/lvm/backup
%attr(700,root,root) %dir %{_sysconfdir}/lvm/cache
%attr(600,root,root) %ghost %{_sysconfdir}/lvm/cache/.cache
%attr(700,root,root) %dir /run/lock/lvm
%if %mdvver >= 201200
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-monitor.service
%endif
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_udevdir}/11-dm-lvm.rules

%if %{with uclibc}
%files -n uclibc-%{name}
%doc INSTALL README VERSION WHATS_NEW
%{uclibc_root}/sbin/blkdeactivate
%{uclibc_root}/sbin/fsadm
%{uclibc_root}/sbin/lv*
%{uclibc_root}/sbin/pv*
%{uclibc_root}/sbin/vg*
%endif

%files -n %{cmdlibname}
/%{_lib}/liblvm2cmd.so.%{cmdmajor}
%if %{build_dmeventd}
%dir /%{_lib}/device-mapper
/%{_lib}/device-mapper/libdevmapper-event-lvm2mirror.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2raid.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2snapshot.so
/%{_lib}/libdevmapper-event-lvm2.so.%{cmdmajor}
/%{_lib}/libdevmapper-event-lvm2mirror.so
/%{_lib}/libdevmapper-event-lvm2raid.so
/%{_lib}/libdevmapper-event-lvm2snapshot.so
%endif

%if %{with uclibc}
%files -n uclibc-%{cmdlibname}
%{uclibc_root}/%{_lib}/liblvm2cmd.so.%{cmdmajor}
%if %{build_dmeventd}
%dir %{uclibc_root}/%{_lib}/device-mapper
%{uclibc_root}/%{_lib}/device-mapper/libdevmapper-event-lvm2mirror.so
%{uclibc_root}/%{_lib}/device-mapper/libdevmapper-event-lvm2raid.so
%{uclibc_root}/%{_lib}/device-mapper/libdevmapper-event-lvm2snapshot.so
%{uclibc_root}/%{_lib}/libdevmapper-event-lvm2.so.%{cmdmajor}
%{uclibc_root}/%{_lib}/libdevmapper-event-lvm2mirror.so
%{uclibc_root}/%{_lib}/libdevmapper-event-lvm2raid.so
%{uclibc_root}/%{_lib}/libdevmapper-event-lvm2snapshot.so
%endif
%endif

%files -n %{cmddevname}
%{_includedir}/lvm2cmd.h
%{_libdir}/liblvm2cmd.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/liblvm2cmd.so
%endif

%if %build_lvm2app
%files -n %{applibname}
/%{_lib}/liblvm2app.so.*

%files -n %{appdevname}
%{_includedir}/lvm2app.h
%{_libdir}/liblvm2app.so
%{_libdir}/pkgconfig/lvm2app.pc
%endif

%if %build_cluster
%files -n clvmd
%if %mdvver < 201200
%config(noreplace) %{_initrddir}/clvmd
%endif
/sbin/clvmd
/sbin/lvmconf
%attr(644,root,root) %{_mandir}/man8/clvmd.8*

%files -n cmirror
%if %mdvver < 201200
%config(noreplace) %{_initrddir}/cmirrord
%endif
/sbin/cmirrord
%attr(644,root,root) %{_mandir}/man8/cmirrord.8*
%endif

%files -n dmsetup
%doc INSTALL README VERSION_DM WHATS_NEW_DM
/sbin/dmsetup
/sbin/dmsetup.static
/sbin/dmsetup-static
%if %{build_dmeventd}
/sbin/dmeventd
%endif
%if %mdvver >= 201200
%{_unitdir}/dm-event.service
%{_unitdir}/dm-event.socket
%endif
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%if %{with uclibc}
%files -n uclibc-dmsetup
%{uclibc_root}/sbin/dmsetup
%if %{build_dmeventd}
%{uclibc_root}/sbin/dmeventd
%endif
%endif

%files -n %{dmlibname}
/%{_lib}/libdevmapper.so.%{dmmajor}*

%if %{with uclibc}
%files -n uclibc-%{dmlibname}
%{uclibc_root}/%{_lib}/libdevmapper.so.%{dmmajor}*
%endif

%files -n %{dmdevname}
%{_libdir}/libdevmapper.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libdevmapper.a
%{uclibc_root}%{_libdir}/libdevmapper.so
%endif
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%if %{build_dmeventd}
%files -n %{event_libname}
/%{_lib}/libdevmapper-event.so.*

%if %{with uclibc}
%files -n uclibc-%{event_libname}
%{uclibc_root}/%{_lib}/libdevmapper-event.so.*
%endif

%files -n %{event_devname}
%{_includedir}/libdevmapper-event.h
%{_libdir}/libdevmapper-event.so
%{_libdir}/libdevmapper-event-lvm2.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libdevmapper-event.so
%{uclibc_root}%{_libdir}/libdevmapper-event-lvm2.so
%endif
%{_libdir}/pkgconfig/devmapper-event.pc
%endif

