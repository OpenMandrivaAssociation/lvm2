%bcond_without dmeventd
%bcond_without crosscompile
%bcond_without lvmdbusd

%define lvmversion 2.03.13
%define dmversion 1.02.179
%define dmmajor 1.02
%define cmdmajor %(echo %{lvmversion} |cut -d. -f1-2)
%define appmajor 2.2

%define dmlibname %mklibname devmapper %{dmmajor}
%define dmdevname %mklibname devmapper -d
%define event_libname %mklibname devmapper-event %{dmmajor}
%define event_devname %mklibname devmapper-event -d
%define cmdlibname %mklibname lvm2cmd %{cmdmajor}
%define cmddevname %mklibname lvm2cmd -d
%define oldcmdlibname %mklibname lvm2cmd 2.02

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
Release:	1
License:	GPLv2 and LGPL2.1
Group:		System/Kernel and hardware
Url:		https://sourceware.org/lvm2/
Source0:	https://sourceware.org/ftp/lvm2/releases/LVM2.%{lvmversion}.tgz
Source1:	%{name}-tmpfiles.conf
# Dracut config
Source2:	60-dracut-distro-lvm.conf
Source3:	70-dracut-distro-dm.conf

# (tpg) patch from ClearLinux
Patch20:	trim.patch

# Furgalware
Patch30:	https://raw.githubusercontent.com/frugalware/frugalware-current/master/source/base/lvm2/stop-the-flood-by-default.patch
Patch31:	https://raw.githubusercontent.com/frugalware/frugalware-current/master/source/base/lvm2/fix-service-files.patch

BuildRequires:	sed
#BuildConflicts:	device-mapper-devel < %{dmversion}
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	intltool
BuildRequires:	autoconf-archive
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	thin-provisioning-tools
BuildRequires:	libaio-devel
BuildRequires:	%mklibname aio -d -s
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

%package -n %{cmdlibname}
Summary:	LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{dm_req} >= %{dmversion}
Obsoletes:	%{oldcmdlibname} < %{EVRD}
# Avoid devel deps on library due to autoreq picking these plugins up as devel libs
%global __requires_exclude devel\\(libdevmapper

%description -n %{cmdlibname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.

%package -n %{cmddevname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{cmdlibname} = %{lvmversion}-%{release}
Requires:	%{dm_req_d} = %{dmversion}-%{release}
Provides:	liblvm2cmd-devel = %{lvmversion}-%{release}
Obsoletes:	%{mklibname lvm2cmd %cmdmajor -d} < %{lvmversion}-%{release}

%description -n %{cmddevname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.

%package -n dmsetup
Summary:	Device mapper setup tool
Version:	%{dmversion}
Group:		System/Kernel and hardware
Provides:	device-mapper = %{dmversion}-%{release}
%if %{with dmeventd}
Provides:	dmeventd = %{dmversion}-%{release}
%endif
Requires:	%{dm_req} = %{dmversion}-%{release}
BuildRequires:	pkgconfig(udev) >= 195
Requires:	systemd
Requires:	util-linux

%description -n dmsetup
Dmsetup manages logical devices that use the device-mapper driver.
Devices are created by loading a table that specifies a target for
each sector (512 bytes) in the logical device.

%package -n %{dmlibname}
Summary:	Device mapper library
Version:	%{dmversion}
Group:		System/Kernel and hardware

%description -n %{dmlibname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the shared libraries required for running
programs which use device-mapper.

%package -n %{dmdevname}
Summary:	Device mapper development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-devel = %{dmversion}-%{release}
Provides:	libdevmapper-devel = %{dmversion}-%{release}
Requires:	%{dmlibname} = %{dmversion}-%{release}
Requires:	pkgconfig
Conflicts:	device-mapper-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper %dmmajor -d}

%description -n %{dmdevname}
The device-mapper driver enables the definition of new block
devices composed of ranges of sectors of existing devices.  This
can be used to define disk partitions - or logical volumes.

This package contains the header files and development libraries
for building programs which use device-mapper.

%if %{with dmeventd}
%package -n %{event_libname}
Summary:	Device mapper event library
Version:	%{dmversion}
Group:		System/Kernel and hardware
Provides:	device-mapper-event = %{dmversion}-%{release}
Provides:	libdevmapper-event = %{dmversion}-%{release}
Requires:	%{dmlibname} >= %{dmversion}

%description -n %{event_libname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the shared libraries required for running
programs which use device-mapper-event.

%package -n %{event_devname}
Summary:	Device mapper event development library
Version:	%{dmversion}
Group:		Development/C
Provides:	device-mapper-event-devel = %{dmversion}-%{release}
Requires:	%{event_libname} = %{dmversion}-%{release}
Requires:	%{dmdevname} = %{dmversion}-%{release}
Conflicts:	device-mapper-event-devel < %{dmversion}-%{release}
Obsoletes:	%{mklibname devmapper-event %dmmajor -d}

%description -n %{event_devname}
The device-mapper-event library allows monitoring of active mapped devices.

This package contains the header files and development libraries
for building programs which use device-mapper-event.
%endif

##############################################################################
# LVM D-Bus daemon
##############################################################################
%if %{with lvmdbusd}
%package dbusd
Summary:	LVM2 D-Bus daemon
License:	GPLv2
Group:		System/Base
Requires:	lvm2 >= %{version}-%{release}
BuildRequires:	pkgconfig(python3)
BuildRequires:	pyudev
BuildRequires:	pkgconfig(dbus-python)
Requires:	dbus
Requires:	python-dbus
Requires:	pyudev
Requires:	python-gobject3

%description dbusd
Daemon for access to LVM2 functionality through a D-Bus interface.
%endif

%prep
%autosetup -p1 -n LVM2.%{lvmversion}

%config_update
autoreconf -fiv
autoconf

%build
%if %{with crosscompile}
export ac_cv_func_malloc_0_nonnull=yes
export ac_cv_func_realloc_0_nonnull=yes
%endif
%ifarch %arm
export ac_cv_func_malloc_0_nonnull=yes
%endif
datelvm=$(awk -F '[.() ]*' '{printf "%s.%s.%s:%s\n", $1,$2,$3,$(NF-1)}' VERSION)
datedm=$(awk -F '[.() ]*' '{printf "%s.%s.%s:%s\n", $1,$2,$3,$(NF-1)}' VERSION_DM)
%if %{with dmeventd}
%define _disable_ld_as_needed 1
%endif
%define common_configure_parameters --with-default-dm-run-dir=%{_rundir} --with-default-run-dir=%{_rundir}/lvm --with-default-pid-dir=%{_rundir} --with-default-locking-dir=%{_rundir}/lock/lvm --with-user= --with-group= --disable-selinux --with-device-uid=0 --with-device-gid=6 --with-device-mode=0660 --enable-dependency-tracking
export MODPROBE_CMD=/sbin/modprobe
export LDFLAGS="%{optflags} -flto"

%configure \
	%{common_configure_parameters} \
	--sbindir=/sbin \
	--disable-static_link \
	--enable-readline \
	--enable-fsadm \
	--enable-blkid_wiping \
	--enable-pkgconfig \
	--with-usrlibdir=%{_libdir} \
	--libdir=/%{_lib} \
	--enable-cmdlib \
	--enable-lvmpolld \
%if %{with lvmdbusd}
	--enable-dbus-service \
	--enable-notify-dbus \
%endif
%if %{with dmeventd}
	--enable-dmeventd \
	--with-dmeventd-path=/sbin/dmeventd \
%endif
	--enable-udev_sync \
	--enable-udev_rules \
	--enable-udev-systemd-background-jobs \
	--with-udevdir=%{_udevrulesdir} \
	--with-systemdsystemunitdir=%{_unitdir}
# 20090926 no translations yet:	--enable-nls
# end of configure options
%make_build

%install
%make_install install_system_dirs install_systemd_units install_systemd_generators install_tmpfiles_configuration

install -m644 %{S:1} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d %{buildroot}/etc/lvm/archive
install -d %{buildroot}/etc/lvm/backup
install -d %{buildroot}/etc/lvm/cache
touch %{buildroot}/etc/lvm/cache/.cache

install -d %{buildroot}%{_rundir}/lock/lvm

#install -d %{buildroot}/%{_libdir}/
#compatibility links
ln %{buildroot}/sbin/lvm %{buildroot}/sbin/lvm2

#hack permissions of libs
chmod u+w %{buildroot}/%{_lib}/*.so.* %{buildroot}/sbin/*

#hack trick strip_and_check_elf_files
export LD_LIBRARY_PATH=%{buildroot}/%{_lib}:${LD_LIBRARY_PATH}

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-lvm2.preset << EOF
enable blk-availability.service
enable lvm2-monitor.service
enable lvm2-lvmpolld.socket
EOF

cat > %{buildroot}%{_presetdir}/86-device-mapper.preset << EOF
enable dm-event.socket
EOF

# Add lvm support to initramfs
mkdir -p %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d
cp %{S:2} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/
cp %{S:3} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/

%if %{with dmeventd}
%post -n dmsetup
if [ -e %{_rundir}/dmeventd.pid ]; then
    /sbin/dmeventd -R || echo "Failed to restart dmeventd daemon. Please, try manual restart."	
fi

%endif

%triggerpostun -- %{name} < 2.03.11-3
# lvmetad is gone...
sed -i -e 's,use_lvmetad[[:space:]]*=.*,use_lvmetad = 0,' %{_sysconfdir}/lvm/*.conf ||:

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
/sbin/lvmpolld
/sbin/lvm2
/sbin/lvmconfig
/sbin/lvmdiskscan
/sbin/lvmdump
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
%{_sysconfdir}/lvm/profile/vdo-small.profile
%config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%attr(700,root,root) %dir %{_sysconfdir}/lvm/archive
%attr(700,root,root) %dir %{_sysconfdir}/lvm/backup
%attr(700,root,root) %dir %{_sysconfdir}/lvm/cache
%attr(600,root,root) %ghost %{_sysconfdir}/lvm/cache/.cache
%attr(700,root,root) %dir %{_rundir}/lock/lvm
%{_presetdir}/86-lvm2.preset
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-monitor.service
%{_unitdir}/lvm2-lvmpolld.service
%{_unitdir}/lvm2-lvmpolld.socket
%{_systemdgeneratordir}/lvm2-activation-generator
%{_tmpfilesdir}/%{name}.conf
%doc %{_mandir}/man5/*
%doc %{_mandir}/man7/lvmthin.7*
%doc %{_mandir}/man7/lvmcache.7*
%doc %{_mandir}/man7/lvmvdo.7*
%doc %{_mandir}/man7/lvmsystemid.7*
%doc %{_mandir}/man7/lvmraid.7.*
%doc %{_mandir}/man7/lvmreport.7.*
%doc %{_mandir}/man8/*
%{_udevrulesdir}/11-dm-lvm.rules
%{_udevrulesdir}/69-dm-lvm-metad.rules
%{_prefix}/lib/dracut/dracut.conf.d/60-dracut-distro-lvm.conf

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
/%{_lib}/libdevmapper-event-lvm2vdo.so
/%{_lib}/device-mapper/libdevmapper-event-lvm2vdo.so

%files -n %{cmddevname}
%{_includedir}/lvm2cmd.h
%{_libdir}/liblvm2cmd.so

%files -n dmsetup
%doc INSTALL README VERSION_DM WHATS_NEW_DM
/sbin/dmsetup
/sbin/dmstats
%if %{with dmeventd}
/sbin/dmeventd
%endif
%{_presetdir}/86-device-mapper.preset
%{_unitdir}/dm-event.service
%{_unitdir}/dm-event.socket
%{_udevrulesdir}/10-dm.rules
%{_udevrulesdir}/13-dm-disk.rules
%{_udevrulesdir}/95-dm-notify.rules
%{_prefix}/lib/dracut/dracut.conf.d/70-dracut-distro-dm.conf

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
%{_unitdir}/lvm2-pvscan@.service
%{python_sitelib}/lvmdbusd/*
%endif
