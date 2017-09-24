%define _disable_lto 1

%bcond_without lvm2app
%bcond_with cluster
%bcond_without dmeventd
%bcond_without lvmetad
%bcond_without crosscompile
%bcond_without lvmdbusd

%define _udevdir /lib/udev/rules.d
%define lvmversion	2.02.174
%define dmversion	1.02.144
%define dmmajor		1.02
%define cmdmajor	2.02
%define appmajor	2.2

%define dmlibname	%mklibname devmapper %{dmmajor}
%define dmdevname	%mklibname devmapper -d
%define event_libname	%mklibname devmapper-event %{dmmajor}
%define event_devname	%mklibname devmapper-event -d
%define cmdlibname	%mklibname lvm2cmd %{cmdmajor}
%define cmddevname	%mklibname lvm2cmd -d
%if %{with lvm2app}
%define applibname	%mklibname lvm2app %{appmajor}
%define appdevname	%mklibname -d lvm2
%endif

#requirements for cluster
%define corosync_version 1.2.0
%define openais_version 1.1.1
%define cluster_version 3.0.6

%if %{with dmeventd}
%define dm_req %{event_libname}
%define dm_req_d %{event_devname}
%else
%define dm_req %{dmlibname}
%define dm_req_d %{dmdevname}
%endif

Summary:	Logical Volume Manager administration tools
Name:		lvm2
Version:	%{lvmversion}
Release:	2
License:	GPLv2 and LGPL2.1
Group:		System/Kernel and hardware
Url:		http://sources.redhat.com/lvm2/
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{lvmversion}.tgz
Source2:	%{name}-tmpfiles.conf
Patch0:		LVM2.2.02.98-alternatives.patch
Patch1:		lvm2-2.02.77-qdiskd.patch
#Patch2:		lvm2-2.02.107-vgmknodes-man.patch
#Fedora
Patch4:		lvm2-set-default-preferred_names.patch
Patch5:		lvm2-lvmetad-timeout.patch

#Patch7:		thin-perfomance-norule.patch
Patch8:		LVM2.2.02.120-link-against-libpthread-and-libuuid.patch

BuildRequires:	sed
#BuildConflicts:	device-mapper-devel < %{dmversion}
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	glibc-static-devel
BuildRequires:	intltool
BuildRequires:	autoconf-archive
BuildRequires:	pkgconfig(systemd)
BuildRequires:	thin-provisioning-tools
Requires(post):	rpm-helper
%if %{with dmeventd}
# install plugins as well
Requires:	%{cmdlibname} = %{lvmversion}-%{release}
%endif
Requires:	%{dm_req} >= %{dmversion}
Conflicts:	lvm
Conflicts:	lvm1

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
Requires:	%{dm_req} >= %{dmversion}
# Avoid devel deps on library due to autoreq picking these plugins up as devel libs
%define __noautoreqfiles	'libdevmapper-event-lvm2(mirror|raid|snapshot|thin).so'

%description -n	%{cmdlibname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.

%package -n	%{cmddevname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{cmdlibname} = %{lvmversion}-%{release}
Requires:	%{dm_req_d} = %{dmversion}-%{release}
Provides:	liblvm2cmd-devel = %{lvmversion}-%{release}
Obsoletes:	%{mklibname lvm2cmd %cmdmajor -d} < %{lvmversion}-%{release}

%description -n	%{cmddevname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.
This package contains the header files for building with lvm2cmd and lvm2app.

%if %{with lvm2app}
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

%if %{with cluster}
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
%if %{with dmeventd}
Provides:	dmeventd = %{dmversion}-%{release}
%endif
Requires:	%{dm_req} = %{dmversion}-%{release}
BuildRequires:	pkgconfig(udev) >= 195
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

%package -n	%{dmdevname}
Summary:	Device mapper development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-devel = %{dmversion}-%{release}
Provides:	libdevmapper-devel = %{dmversion}-%{release}
Requires:	%{dmlibname} = %{dmversion}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper %dmmajor -d}

%description -n	%{dmdevname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the header files and development libraries
for building programs which use device-mapper.

%if %{with dmeventd}
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

%package -n	%{event_devname}
Summary:	Device mapper event development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-event-devel = %{dmversion}-%{release}
Requires:	%{event_libname} = %{dmversion}-%{release}
Requires:	%{dmdevname} = %{dmversion}-%{release}
Conflicts:	device-mapper-event-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper-event %dmmajor -d}

%description -n	%{event_devname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the header files and development libraries
for building programs which use device-mapper-event.
%endif

##############################################################################
# LVM D-Bus daemon
##############################################################################
%if %{with lvmdbusd}
%package	dbusd
Summary:	LVM2 D-Bus daemon
License:	GPLv2
Group:		System/Base
Requires:	lvm2 >= %{version}-%{release}
BuildRequires:	python-devel
BuildRequires:	pyudev
BuildRequires:	python-dbus
Requires:	dbus
Requires:	python-dbus
Requires:	pyudev
Requires:	python-gobject3
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper

%description dbusd
Daemon for access to LVM2 functionality through a D-Bus interface.
%endif

%prep
%setup -qn LVM2.%{lvmversion}
%apply_patches

autoreconf -fiv

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
%if %{with dmeventd}
%define _disable_ld_as_needed 1
%endif
%define common_configure_parameters --with-default-dm-run-dir=/run --with-default-run-dir=/run/lvm --with-default-pid-dir=/run --with-default-locking-dir=/run/lock/lvm --with-user= --with-group= --disable-selinux --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660 --enable-dependency-tracking --disable-python_bindings
export ac_cv_lib_dl_dlopen=no
export MODPROBE_CMD=/sbin/modprobe
export CONFIGURE_TOP="$PWD"

unset ac_cv_lib_dl_dlopen

export LIBS=-lm
export CC=gcc
export CXX=g++

mkdir -p static
pushd static
%configure %{common_configure_parameters} \
	--enable-static_link \
	--disable-readline \
	--with-cluster=none \
	--with-pool=none
sed -e 's/\ -static/ -static -Wl,--no-export-dynamic/' -i tools/Makefile
%make
popd

mkdir -p shared
pushd shared
%configure %{common_configure_parameters} \
	--sbindir=/sbin \
	--disable-static_link \
	--enable-readline \
	--enable-fsadm \
	--enable-pkgconfig \
	--with-usrlibdir=%{_libdir} \
	--enable-notify-dbus \
	--libdir=/%{_lib} \
	--enable-cmdlib \
%if %{with lvmdbusd}
	--enable-dbus-service \
	--enable-notify-dbus \
%endif
%if %{with lvm2app}
	--enable-applib \
%endif
%if %{with cluster}
	--with-clvmd=cman,openais,corosync \
	--enable-cmirrord \
%else
	--with-cluster=none \
	--with-pool=none \
%endif
%if %{with dmeventd}
	--enable-dmeventd \
	--with-dmeventd-path=/sbin/dmeventd \
%endif
%if %{with lvmetad}
	--enable-lvmetad \
%endif
	--enable-udev_sync \
	--enable-udev_rules \
	--enable-udev-systemd-background-jobs \
	--with-udevdir=%{_udevdir} \
	--with-systemdsystemunitdir=%{_systemunitdir}
# 20090926 no translations yet:	--enable-nls
# end of configure options
%make
popd

%install
%makeinstall_std -C shared install_system_dirs install_systemd_units install_systemd_generators install_tmpfiles_configuration

install -m644 %{SOURCE2} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d %{buildroot}/etc/lvm/archive
install -d %{buildroot}/etc/lvm/backup
install -d %{buildroot}/etc/lvm/cache
touch %{buildroot}/etc/lvm/cache/.cache

install -d %{buildroot}/run/lock/lvm

%if %{with cluster}
install shared/scripts/clvmd_init_red_hat %{buildroot}%{_initrddir}/clvmd
install shared/scripts/cmirrord_init_red_hat %{buildroot}%{_initrddir}/cmirrord
%endif

%if %{with cluster}
install -m 0755 scripts/lvmconf.sh %{buildroot}/sbin/lvmconf
%endif

install static/tools/lvm.static -D %{buildroot}/sbin/lvm.static
install static/tools/dmsetup.static -D %{buildroot}/sbin/dmsetup.static

#install -d %{buildroot}/%{_libdir}/
#compatibility links
ln %{buildroot}/sbin/lvm %{buildroot}/sbin/lvm2
ln %{buildroot}/sbin/lvm.static %{buildroot}/sbin/lvm2-static
ln %{buildroot}/sbin/dmsetup.static %{buildroot}/sbin/dmsetup-static

#hack permissions of libs
chmod u+w %{buildroot}/%{_lib}/*.so.* %{buildroot}/sbin/*
%if %{with cluster}
chmod u+w  %{buildroot}/sbin/*
%endif


#hack trick strip_and_check_elf_files
export LD_LIBRARY_PATH=%{buildroot}/%{_lib}:${LD_LIBRARY_PATH}

rm -f %{buildroot}/sbin/dmeventd.static

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-lvm2.preset << EOF
enable blk-availability.service
enable lvm2-monitor.service
enable lvm2-lvmetad.socket
EOF

cat > %{buildroot}%{_presetdir}/86-device-mapper.preset << EOF
enable dm-event.socket
EOF

%pre
if [ -L /sbin/lvm -a -L /etc/alternatives/lvm ]; then
    update-alternatives --remove lvm /sbin/lvm2
fi


%if %{with cluster}
%post -n clvmd
/sbin/clvmd -S || echo "Failed to restart clvmd daemon. Please, try manual restart."

%preun -n clvmd
if [ "$1" = 0 ]; then
    /sbin/lvmconf --disable-cluster
fi
%endif

%if %{with dmeventd}
%post -n dmsetup
/sbin/dmeventd -R || echo "Failed to restart dmeventd daemon. Please, try manual restart."
%endif

%files
%doc INSTALL README VERSION WHATS_NEW
/sbin/blkdeactivate
/sbin/fsadm
/sbin/lvchange
/sbin/lvconvert
/sbin/lvcreate
/sbin/lvdisplay
/sbin/lvextend
/sbin/lvm
/sbin/lvm.static
/sbin/lvm2
/sbin/lvm2-static
/sbin/lvmconf
/sbin/lvmconfig
/sbin/lvmdiskscan
/sbin/lvmdump
/sbin/lvmetad
/sbin/lvmsadc
/sbin/lvmsar
/sbin/lvreduce
/sbin/lvremove
/sbin/lvrename
/sbin/lvresize
/sbin/lvs
/sbin/lvscan
/sbin/pv*
/sbin/vg*
%dir %{_sysconfdir}/lvm
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/lvmlocal.conf
%{_sysconfdir}/lvm/profile/command_profile_template.profile
%{_sysconfdir}/lvm/profile/metadata_profile_template.profile
%{_sysconfdir}/lvm/profile/thin-generic.profile
%{_sysconfdir}/lvm/profile/thin-performance.profile
%{_sysconfdir}/lvm/profile/cache-mq.profile
%{_sysconfdir}/lvm/profile/cache-smq.profile
%{_sysconfdir}/lvm/profile/lvmdbusd.profile
%config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%attr(700,root,root) %dir %{_sysconfdir}/lvm/archive
%attr(700,root,root) %dir %{_sysconfdir}/lvm/backup
%attr(700,root,root) %dir %{_sysconfdir}/lvm/cache
%attr(600,root,root) %ghost %{_sysconfdir}/lvm/cache/.cache
%attr(700,root,root) %dir %{_rundir}/lock/lvm
%{_presetdir}/86-lvm2.preset
%{_systemunitdir}/blk-availability.service
%{_systemunitdir}/lvm2-monitor.service
%{_systemgeneratordir}/lvm2-activation-generator
%if %{with lvmetad}
%{_systemunitdir}/lvm2-lvmetad.socket
%{_systemunitdir}/lvm2-lvmetad.service
%{_systemunitdir}/lvm2-pvscan@.service
%endif
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man5/*
%{_mandir}/man7/lvmthin.7*
%{_mandir}/man7/lvmcache.7*
%{_mandir}/man7/lvmsystemid.7*
%{_mandir}/man7/lvmraid.7.*
%{_mandir}/man7/lvmreport.7.*
%{_mandir}/man8/*
%{_udevdir}/11-dm-lvm.rules
%{_udevdir}/69-dm-lvm-metad.rules

%files -n %{cmdlibname}
/%{_lib}/liblvm2cmd.so.%{cmdmajor}
%if %{with dmeventd}
%dir /%{_lib}/device-mapper
/%{_lib}/device-mapper/libdevmapper-event-lvm2mirror.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2raid.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2snapshot.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2thin.so
/%{_lib}/libdevmapper-event-lvm2.so.%{cmdmajor}
/%{_lib}/libdevmapper-event-lvm2mirror.so
/%{_lib}/libdevmapper-event-lvm2raid.so
/%{_lib}/libdevmapper-event-lvm2snapshot.so
/%{_lib}/libdevmapper-event-lvm2thin.so
%endif

%files -n %{cmddevname}
%{_includedir}/lvm2cmd.h
%{_libdir}/liblvm2cmd.so

%if %{with lvm2app}
%files -n %{applibname}
/%{_lib}/liblvm2app.so.*

%files -n %{appdevname}
%{_includedir}/lvm2app.h
%{_libdir}/liblvm2app.so
%{_libdir}/pkgconfig/lvm2app.pc
%endif

%if %{with cluster}
%files -n clvmd
/sbin/clvmd
/sbin/lvmconf
%attr(644,root,root) %{_mandir}/man8/clvmd.8*

%files -n cmirror
/sbin/cmirrord
%attr(644,root,root) %{_mandir}/man8/cmirrord.8*
%endif

%files -n dmsetup
%doc INSTALL README VERSION_DM WHATS_NEW_DM
/sbin/dmsetup
/sbin/dmstats
/sbin/dmsetup.static
/sbin/dmsetup-static
%if %{with dmeventd}
/sbin/dmeventd
%endif
%{_presetdir}/86-device-mapper.preset
%{_systemunitdir}/dm-event.service
%{_systemunitdir}/dm-event.socket
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%files -n %{dmlibname}
/%{_lib}/libdevmapper.so.%{dmmajor}*

%files -n %{dmdevname}
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%if %{with dmeventd}
%files -n %{event_libname}
/%{_lib}/libdevmapper-event.so.*

%files -n %{event_devname}
%{_includedir}/libdevmapper-event.h
%{_libdir}/libdevmapper-event.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_libdir}/pkgconfig/devmapper-event.pc
%endif

##############################################################################
# LVM D-Bus daemon
##############################################################################
%if %{with lvmdbusd}
%files dbusd
%defattr(555,root,root,-)
/sbin/lvmdbusd
%defattr(444,root,root,-)
%{_sysconfdir}/dbus-1/system.d/com.redhat.lvmdbus1.conf
%{_datadir}/dbus-1/system-services/com.redhat.lvmdbus1.service
%{_unitdir}/lvm2-lvmdbusd.service
%{python_sitelib}/lvmdbusd/*
%endif
