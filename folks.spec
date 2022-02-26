%global folks_module_version 26

Name:           folks
Epoch:          1
Version:        0.15.2
Release:        3
Summary:        Library aggregates people from multiple sources
License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Folks
Source0:        http://ftp.gnome.org/pub/GNOME/sources/folks/0.15/folks-%{version}.tar.xz
Patch0:        folks-eds-test-timeout.patch

BuildRequires:  intltool vala-devel >= 0.17.6
BuildRequires:  libxml2-devel GConf2-devel
BuildRequires:  gcc meson gettext
BuildRequires:  pkgconfig(dbus-glib-1) evolution-data-server-devel >= 3.33.2 pkgconfig(gee-0.8) >= 0.8.4
BuildRequires:  glib2-devel gobject-introspection-devel libxml2-devel
BuildRequires:  python3-dbusmock python3-devel readline-devel
BuildRequires:  telepathy-glib-devel telepathy-glib-vala vala

%description
libfolks is a library that aggregates people from multiple sources
(eg, Telepathy connection managers) to create metacontacts.

%package        telepathy
Summary:        Folks telepathy backend
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    telepathy
%{name}-telepathy contains the folks telepathy backend.

%package        tools
Summary:        Tools for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    tools
%{name}-tools contains a database and import tool.

%package        devel
Summary:        Development files for folks
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       %{name}-tools = %{epoch}:%{version}-%{release}

%description    devel
This package contains libraries and header files.


%prep
%autosetup -p1


%build
%define _lto_cflags %{nil}

%meson
%meson_build

%install
%meson_install

%find_lang %{name}

%check
%ifarch riscv64
%meson_test --timeout-multiplier=10
%else
%meson_test
%endif

%files -f folks.lang
%license COPYING
%doc AUTHORS NEWS
%{_libdir}/libfolks-dummy.so.26*
%{_libdir}/libfolks-eds.so.26*
%{_libdir}/libfolks.so.26*
%dir %{_libdir}/folks
%dir %{_libdir}/folks/%{folks_module_version}
%dir %{_libdir}/folks/%{folks_module_version}/backends
%{_libdir}/folks/%{folks_module_version}/backends/bluez/
%{_libdir}/folks/%{folks_module_version}/backends/dummy/
%{_libdir}/folks/%{folks_module_version}/backends/eds/
%{_libdir}/folks/%{folks_module_version}/backends/key-file/
%{_libdir}/folks/%{folks_module_version}/backends/ofono/
%{_libdir}/girepository-1.0/Folks-0.7.typelib
%{_libdir}/girepository-1.0/FolksDummy-0.7.typelib
%{_libdir}/girepository-1.0/FolksEds-0.7.typelib
%{_datadir}/GConf/gsettings/folks.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml

%files telepathy
%{_libdir}/libfolks-telepathy.so.26*
%{_libdir}/folks/%{folks_module_version}/backends/telepathy
%{_libdir}/girepository-1.0/FolksTelepathy-0.7.typelib

%files tools
%{_bindir}/%{name}-import
%{_bindir}/%{name}-inspect

%files devel
%{_includedir}/folks
%{_libdir}/*.so
%{_libdir}/pkgconfig/folks*.pc
%{_datadir}/gir-1.0/Folk*.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/folks*


%changelog
* Sun Feb 27 2022 YukariChiba <i@0x7f.cc> - 3.38.3-2
- Expand timeout value for RISC-V in tests

* Mon Jun 28 2021 weijin deng <weijin.deng@turbolinux.com.cn> - 3.38.3-1
- Get rid of repeated build dependency that may cause fault

* Fri Jun 25 2021 Wenlong Ding <wenlong.ding@turbolinux.com.cn> - 1:0.15.2-1
- Update to 1:0.15.2

* Wed Dec 25 2019 Ling Yang <lingyang2@huawei.com> - 1:0.11.4-10
- Add epoch for providing folks-tools

* Sat Dec 21 2019 Senlin Xia <xiasenlin1@huawei.com> - 1:0.11.4-9
- Package init
