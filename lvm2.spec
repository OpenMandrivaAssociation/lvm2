%define name lvm2
%define lvmversion 2.02.97
%define dmversion 1.02.76
%define release %mkrel 1
%define _usrsbindir %{_prefix}/sbin
%define _sbindir /sbin
%define _udevdir /lib/udev/rules.d
%define dmmajor 1.02
%define cmdmajor 2.02
%define appmajor 2.2

%define dmlibname %mklibname devmapper %{dmmajor}
%define dmdevelname %mklibname devmapper -d
%define event_libname %mklibname devmapper-event %{dmmajor}
%define event_develname %mklibname devmapper-event -d
%define cmdlibname %mklibname lvm2cmd %{cmdmajor}
%define cmddevelname %mklibname lvm2cmd -d

%define build_lvm2app 1
%define build_cluster 0
%define build_dmeventd 1

#requirements for cluster
%define corosync_version 1.2.0
%define openais_version 1.1.1
%define cluster_version 3.0.6

%{?_with_dmeventd: %{expand: %%global build_dmeventd 1}}
%{?_without_dmeventd: %{expand: %%global build_dmeventd 0}}
%{?_with_lvm2app: %{expand: %%global build_lvm2app 1}}
%{?_without_lvm2app: %{expand: %%global build_lvm2app 0}}
%{?_with_cluster: %{expand: %%global build_cluster 1}}
%{?_without_cluster: %{expand: %%global build_cluster 0}}

%bcond_without uclibc

%if %build_lvm2app
%define applibname %mklibname lvm2app %{appmajor}
%define appdevelname %mklibname -d lvm2
%endif

%if %build_dmeventd
%define dm_req %{event_libname}
%define dm_req_d %{event_develname}
%else
%define dm_req %{dmlibname}
%define dm_req_d %{dmdevelname}
%endif

Summary:	Logical Volume Manager administration tools
Name:		%{name}
Version:	%{lvmversion}
Release:	%{release}
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{lvmversion}.tgz
Source1:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{lvmversion}.tgz.asc
Source2:	%{name}-tmpfiles.conf
Patch0:		lvm2-2.02.53-alternatives.patch
Patch1:		lvm2-2.02.77-qdiskd.patch
Patch2:		lvm2-2.02.97-vgmknodes-man.patch
Patch5:		lvm2-2.02.77-preferred_names.patch
License:	GPLv2 and LGPL2.1
Group:		System/Kernel and hardware
URL:		http://sources.redhat.com/lvm2/
BuildConflicts:	device-mapper-devel < %{dmversion}
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
#BuildRequires:	autoconf
BuildRequires:	sed
Conflicts:	lvm
Conflicts:	lvm1
BuildRequires:	glibc-static-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel
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

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.

%package -n %{cmdlibname}
Summary:	LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{dm_req} >= %{dmversion}
# Avoid devel deps on library due to autoreq picking these plugins up as devel libs
%define _exclude_files_from_autoreq libdevmapper-event-.\\+\\.so$

%description -n	%{cmdlibname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.

%package -n %{cmddevelname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{cmdlibname} = %{lvmversion}-%{release}
Requires:	%{dm_req_d} = %{dmversion}-%{release}
Provides:	liblvm2cmd-devel = %{lvmversion}-%{release}
Obsoletes:	%{mklibname lvm2cmd %cmdmajor -d}

%description -n	%{cmddevelname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.
This package contains the header files for building with lvm2cmd and lvm2app.

%if %build_lvm2app
%package -n %{applibname}
Summary:	LVM2 application api library
Group:		System/Kernel and hardware
Requires:	%{dm_req} >= %{dmversion}
Obsoletes:	%{mklibname lvm2app 2.1}

%description -n	%{applibname}
LVM2 application API.

%package -n %{appdevelname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	pkgconfig
Requires:	%{applibname} = %{lvmversion}-%{release}
Requires:	%{dm_req_d} = %{dmversion}-%{release}
Provides:	liblvm2app-devel = %{lvmversion}-%{release}
Obsoletes:	%{mklibname lvm2app %appmajor -d}

%description -n	%{appdevelname}
LVM2 application API
This package contains the header files for building with lvm2app.
%endif

%if %build_cluster
%package -n clvmd
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

%package -n cmirror
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

%package -n dmsetup
Summary:	Device mapper setup tool
Version:	%{dmversion}
Group:		System/Kernel and hardware
Provides:	device-mapper = %{dmversion}-%{release}
%if %{build_dmeventd}
Provides:	dmeventd = %{dmversion}-%{release}
%endif
Requires:	%{dm_req} = %{dmversion}-%{release}
%if %mdvver >= 201200
BuildRequires:	pkgconfig(udev) >= 186
%else
BuildRequires:	pkgconfig(udev)
%endif
Requires:	udev
Requires(pre):	rpm-helper

%description -n	dmsetup
Dmsetup manages logical devices that use the device-mapper driver.  
Devices are created by loading a table that specifies a target for
each sector (512 bytes) in the logical device.

%package -n %{dmlibname}
Summary:	Device mapper library
Version:	%{dmversion}
Group:		System/Kernel and hardware

%description -n	%{dmlibname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the shared libraries required for running
programs which use device-mapper.

%package -n %{dmdevelname}
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
%package -n %{event_libname}
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

%package -n %{event_develname}
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
%patch1 -p1 -b .qdiskd
%patch2 -p1 -b .vgmknodes-man
%patch5 -p1 -b .preferred

%build
datelvm=`awk -F '[.() ]*' '{printf "%s.%s.%s:%s\n", $1,$2,$3,$(NF-1)}' VERSION`
datedm=`awk -F '[.() ]*' '{printf "%s.%s.%s:%s\n", $1,$2,$3,$(NF-1)}' VERSION_DM`
if [ "${datelvm%:*}" != "%{lvmversion}" -o "${datedm%:*}" != "%{dmversion}" -o \
 "%{release}" = "%{mkrel 1}" -a "${datelvm#*:}" != "${datedm#*:}" ]; then
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

mkdir -p static
pushd static
%configure2_5x %{common_configure_parameters} \
	--enable-static_link --disable-readline \
	--with-cluster=none --with-pool=none
sed -ie 's/\ -static/ -static -Wl,--no-export-dynamic/' tools/Makefile
%if %{with uclibc}
%make libdm.device-mapper
popd

mkdir -p uclibc
pushd uclibc
%configure2_5x CFLAGS="%{uclibc_cflags}" CC="%{uclibc_cc}" %{common_configure_parameters} \
	--enable-static_link --disable-readline \
	--with-cluster=none --with-pool=none
%endif
sed -ie 's/\ -static/ -static -Wl,--no-export-dynamic/' tools/Makefile
%make
popd

unset ac_cv_lib_dl_dlopen

mkdir -p shared
pushd shared
%configure2_5x %{common_configure_parameters} \
	--disable-static_link --enable-readline \
	--enable-fsadm --enable-pkgconfig \
	--with-usrlibdir=%{_libdir} --libdir=/%{_lib} \
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
	--enable-udev_sync --enable-udev_rules \
	--with-udevdir=%{_udevdir} \
# 20090926 no translations yet:	--enable-nls
# end of configure options
%make
popd

%install
pushd shared
%makeinstall_std
%if %mdvver >= 201200
make install_systemd_units DESTDIR=%{buildroot}
make install_tmpfiles_configuration DESTDIR=%{buildroot}
%endif
popd

install -m644 %{SOURCE2} -D %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
install -d %{buildroot}/etc/lvm/archive
install -d %{buildroot}/etc/lvm/backup
install -d %{buildroot}/etc/lvm/cache
touch %{buildroot}/etc/lvm/cache/.cache

install -d %{buildroot}/run/lock/lvm

%if %mdvver >= 201200
%else
install -d %{buildroot}/%{_initrddir}
install shared/scripts/lvm2_monitoring_init_red_hat %{buildroot}/%{_initrddir}/lvm2-monitor
%if %build_cluster
install shared/scripts/clvmd_init_red_hat %{buildroot}/%{_initrddir}/clvmd
install shared/scripts/cmirrord_init_red_hat %{buildroot}/%{_initrddir}/cmirrord
%endif
%endif

%if %build_cluster
install -m 0755 scripts/lvmconf.sh %{buildroot}/%{_usrsbindir}/lvmconf
%endif

%if %{with uclibc}
install uclibc/tools/lvm.static %{buildroot}%{_sbindir}/lvm.static
install uclibc/tools/dmsetup.static %{buildroot}%{_sbindir}/dmsetup.static
install -m644 uclibc/libdm/ioctl/libdevmapper.a -D %{buildroot}%{uclibc_root}%{_libdir}/libdevmapper.a
%else
install static/tools/lvm.static %{buildroot}/%{_sbindir}/lvm.static
install static/tools/dmsetup.static %{buildroot}/%{_sbindir}/dmsetup.static
%endif

#install -d %{buildroot}/%{_libdir}/
install -m 644 static/libdm/ioctl/libdevmapper.a %{buildroot}/%{_libdir}
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
chmod u+w %{buildroot}/%{_lib}/*.so.* %{buildroot}/%{_sbindir}/*
%if %build_cluster
chmod u+w  %{buildroot}/%{_usrsbindir}/*
%endif


#hack trick strip_and_check_elf_files
export LD_LIBRARY_PATH=%{buildroot}/%{_lib}:${LD_LIBRARY_PATH}

%pre
if [ -L /sbin/lvm -a -L /etc/alternatives/lvm ]; then
	update-alternatives --remove lvm /sbin/lvm2
fi

%if %build_cluster
%post -n clvmd
%_post_service clvmd
%{_usrsbindir}/lvmconf --lockinglibdir %{_libdir}

%preun -n clvmd
%_preun_service clvmd
if [ "$1" = 0 ]; then
        %{_usrsbindir}/lvmconf --disable-cluster
fi

%post -n cmirror
%_post_service cmirror

%preun -n cmirror
%_preun_service cmirror
%endif

%files
%doc INSTALL README VERSION WHATS_NEW
%attr(755,root,root) %{_sbindir}/fsadm
%attr(755,root,root) %{_sbindir}/lv*
%attr(755,root,root) %{_sbindir}/pv*
%attr(755,root,root) %{_sbindir}/vg*
%dir %{_sysconfdir}/lvm
%config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%attr(700,root,root) %dir %{_sysconfdir}/lvm/archive
%attr(700,root,root) %dir %{_sysconfdir}/lvm/backup
%attr(700,root,root) %dir %{_sysconfdir}/lvm/cache
%attr(600,root,root) %ghost %{_sysconfdir}/lvm/cache/.cache
%attr(700,root,root) %dir /run/lock/lvm
%if %mdvver >= 201200
%{_unitdir}/lvm2-monitor.service
%endif
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_udevdir}/11-dm-lvm.rules

%files -n %{cmdlibname}
%defattr(644,root,root,755)
/%{_lib}/liblvm2cmd.so.*
%if %{build_dmeventd}
%dir /%{_lib}/device-mapper
/%{_lib}/device-mapper/libdevmapper-event-lvm2mirror.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2raid.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2snapshot.so
/%{_lib}/libdevmapper-event-lvm2.so.*
/%{_lib}/libdevmapper-event-lvm2mirror.so
/%{_lib}/libdevmapper-event-lvm2raid.so
/%{_lib}/libdevmapper-event-lvm2snapshot.so
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
%if %mdvver < 201200
%config(noreplace) %{_initrddir}/clvmd
%endif
%{_usrsbindir}/clvmd
%{_usrsbindir}/lvmconf
%attr(644,root,root) %{_mandir}/man8/clvmd.8*

%files -n cmirror
%defattr(755,root,root,-)
%if %mdvver < 201200
%config(noreplace) %{_initrddir}/cmirrord
%endif
%{_usrsbindir}/cmirrord
%attr(644,root,root) %{_mandir}/man8/cmirrord.8*
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
%if %mdvver >= 201200
%{_unitdir}/dm-event.service
%{_unitdir}/dm-event.socket
%endif
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%files -n %{dmlibname}
%defattr(755,root,root)
/%{_lib}/libdevmapper.so.*

%files -n %{dmdevelname}
%defattr(644,root,root,755)
%{_libdir}/libdevmapper.so
%{_libdir}/libdevmapper.a*
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libdevmapper.a
%endif
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
%{_libdir}/libdevmapper-event-lvm2.so
%{_libdir}/pkgconfig/devmapper-event.pc
%endif
