%define	name	lvm2
%define	version	2.02.33
%define	release	%manbo_mkrel 2

%ifarch %{ix86} x86_64 ppc ppc64 %{sunsparc}
%define	use_dietlibc 1
%else
%define	use_dietlibc 0
%endif

%define	build_lvm2cmd 0
%define	build_cluster 0
%define	build_dmeventd 0

%{?_with_lvm2cmd: %{expand: %%global build_lvm2cmd 1}}
%{?_without_lvm2cmd: %{expand: %%global build_lvm2cmd 0}}
%{?_with_cluster: %{expand: %%global build_cluster 1}}
%{?_without_cluster: %{expand: %%global build_cluster 0}}
%{?_with_dietlibc: %{expand: %%global use_dietlibc 1}}
%{?_without_dietlibc: %{expand: %%global use_dietlibc 0}}
%{?_with_dmeventd: %{expand: %%global build_dmeventd 1}}
%{?_without_dmeventd: %{expand: %%global build_dmeventd 0}}

%if %build_lvm2cmd
%define	libname	%mklibname lvm2cmd 2
%define develname %mklibname -d lvm2cmd
%endif

Summary:	Logical Volume Manager administration tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://sources.redhat.com/pub/lvm2/LVM2.%{version}.tgz
Source1:	clvmd.init.bz2
Patch0:		lvm2-2.02.27-alternatives.patch
Patch1:		lvm2-2.02.27-diet.patch
Patch2:		lvm2-2.01.15-stdint.patch
Patch4:		lvm2-ignorelock.patch
Patch5:		lvm2-fdlog.patch
# fixes a 'conflicting types for '__daddr_t'' error caused by it also
# being declared in dietlibc - AdamW 2007/08
Patch6:		lvm2-2.02.27-types.patch
Patch7:		LVM2.2.02.31-uint64_max.patch
License:	GPL
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://sources.redhat.com/lvm2/
BuildRequires:	device-mapper-devel >= 1.02.23
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	autoconf
Conflicts:	lvm
Conflicts:	lvm1
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel
%else
BuildRequires:	glibc-static-devel
%endif
%if %{build_dmeventd}
BuildRequires:	device-mapper-event-devel >= 1.02
%endif

%description
LVM includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see losetup(8)),
creating volume groups (kind of virtual disks) from one or more physical
volumes and creating one or more logical volumes (kind of logical partitions)
in volume groups.

%if %build_lvm2cmd
%package -n	%{libname}
Summary:	LVM2 command line library
Group:		System/Kernel and hardware

%description -n	%{libname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.

%package -n	%{develname}
Summary:	Development files for LVM2 command line library
Group:		System/Kernel and hardware
Requires:	%{libname} = %{version}-%{release}
Provides:	lvm2cmd-devel = %{version}-%{release}
Obsoletes:	%{mklibname lvm2cmd 2 -d}

%description -n	%{develname}
The lvm2 command line library allows building programs that manage
lvm devices without invoking a separate program.
This package contains the header files for building with lvm2cmd.
%endif

%if %build_cluster
%package -n	clvmd
Summary:	cluster LVM daemon
Group:		System/Kernel and hardware
BuildRequires:	cluster-devel

%description -n	clvmd
clvmd is the daemon that distributes LVM metadata updates around a
cluster. It must be running on all nodes in the cluster and will give
an error if a node in the cluster does not have this daemon running.
%endif

%prep
%setup -q -n LVM2.%{version}
%patch0 -p1 -b .alternatives
%if %{use_dietlibc}
%patch1 -p1 -b .diet
%patch2 -p1 -b .stdint
%patch6 -p1 -b .types
%patch7 -p1 -b .uint64_max
%endif
%patch4 -p1 -b .ignorelock
%patch5 -p1 -b .fdlog

%build
autoconf # required by dietlibc patch
export ac_cv_lib_dl_dlopen=no
%if %{use_dietlibc}
# build fails with stack-protector enabled - 2007/08
export CFLAGS="%{optflags} -fno-stack-protector"
%endif
%configure --with-user=`id -un` --with-group=`id -gn` \
	--enable-static_link --disable-readline \
	--disable-selinux --with-cluster=none --with-pool=none
unset ac_cv_lib_dl_dlopen
%if %{use_dietlibc}
CC="diet gcc -DWRAPPER -D_BSD_SOURCE"
LVMLIBS="-llvm -ldevmapper-diet"
%else
CC="gcc -DWRAPPER"
LVMLIBS="-static -llvm -ldevmapper"
%endif
%make CC="$CC" LVMLIBS="$LVMLIBS"
cd tools
$CC -o lvm-static lvm.o lvmcmdline.o vgchange.o vgscan.o toollib.o vgmknodes.o pvmove.o polldaemon.o -L ../lib $LVMLIBS
cd ..
%make clean
%configure --with-user=`id -un` --with-group=`id -gn` \
	--disable-static_link --enable-readline \
	--disable-selinux  --enable-fsadm \
	--enable-nls --with-pool=internal \
%if %build_lvm2cmd
	--enable-cmdlib \
%endif
%if %build_cluster
	--with-clvmd=all --with-cluster=shared \
%endif
%if %{build_dmeventd}
	--enable-dmeventd \
%endif
# end of configure options
%make

%install
rm -rf %{buildroot}
%makeinstall sbindir=%{buildroot}/sbin confdir=%{buildroot}%{_sysconfdir}/lvm

install tools/lvm-static %{buildroot}/sbin/lvm.static
#compatibility links
ln %{buildroot}/sbin/lvm %{buildroot}/sbin/lvm2
ln %{buildroot}/sbin/lvm.static %{buildroot}/sbin/lvm2-static

%find_lang %name

%pre
if [ -L /sbin/lvm -a -L /etc/alternatives/lvm ]; then
	update-alternatives --remove lvm /sbin/lvm2
fi

%if %build_lvm2cmd
%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif
%endif

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/fsadm
%attr(755,root,root) /sbin/lv*
%attr(755,root,root) /sbin/pv*
%attr(755,root,root) /sbin/vg*
#{_libdir}/liblvm2format1.so*
#{_libdir}/liblvm2formatpool.so*
#{_libdir}/liblvm2mirror.so*
#{_libdir}/liblvm2snapshot.so*
%dir %{_sysconfdir}/lvm/
%config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%{_mandir}/man5/*
%{_mandir}/man8/*
%doc INSTALL README VERSION WHATS_NEW

%if %build_lvm2cmd
%files -n %{libname}
%defattr(644,root,root,755)
%{_libdir}/liblvm2cmd.so*

%files -n %{develname}
%defattr(644,root,root,755)
%{_includedir}/lvm2cmd.h
%attr(755,root,root) %{_libdir}/liblvm2cmd.so
%endif
%if %build_cluster
%files -n clvmd
%defattr(755, root,root)
%config(noreplace) %{_initrddir}/clvmd
%{_sbindir}/clvmd
%{_libdir}/liblvm2clusterlock.so*
%attr(644,root,root) %{_mandir}/man8/clvmd.8*
%endif

