Name:           folks
Epoch:          1
Version:        0.11.4
Release:        9
Summary:        Library aggregates people from multiple sources
License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Folks
Source0:        http://ftp.gnome.org/pub/GNOME/sources/folks/0.11/folks-%{version}.tar.xz

BuildRequires:  chrpath telepathy-glib-devel >= 0.19.0 telepathy-glib-vala
BuildRequires:  glib2-devel gobject-introspection-devel intltool vala-devel >= 0.17.6
BuildRequires:  vala libxml2-devel GConf2-devel evolution-data-server-devel >= 3.13.90
BuildRequires:  readline-devel pkgconfig(gee-0.8) >= 0.8.4

Provides:       %{name}-tools = %{version}-%{release}
Obsoletes:      %{name}-tools < %{version}-%{release}

%description
libfolks is a library that aggregates people from multiple sources
(eg, Telepathy connection managers) to create metacontacts.

%package        devel
Summary:        Development files for folks
Requires:       folks = %{epoch}:%{version}-%{release}
Requires:       folks-tools = %{epoch}:%{version}-%{release}

%description    devel
This package contains libraries and header files.


%prep
%autosetup -p1


%build
%configure --disable-fatal-warnings --enable-eds-backend \
  --enable-bluez-backend --disable-zeitgeist --enable-vala \
  --enable-inspect-tool --disable-libsocialweb-backend
%make_build V=1


%install
%make_install
%delete_la
for fpath in $RPM_BUILD_ROOT%{_libdir}/libfolks-dummy.so \
            $RPM_BUILD_ROOT%{_libdir}/libfolks-eds.so \
            $RPM_BUILD_ROOT%{_libdir}/libfolks-telepathy.so
do
    chrpath --delete ${fpath}
done
find %{buildroot}%{_libdir}/folks/43/backends -name '*.so' -exec chrpath --delete {} \;
find %{buildroot}%{_bindir} -name 'folks-*' -exec chrpath --delete {} \;


%find_lang folks

%check
VERBOSE=1 make check


%post
/sbin/ldconfig


%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f folks.lang
%license COPYING
%doc AUTHORS README NEWS
%{_libdir}/*.so.*
%{_libdir}/folks
%{_libdir}/girepository-1.0/Folks*.typelib
%{_datadir}/GConf/gsettings/folks.convert
%{_datadir}/glib-2.0/schemas/org.freedesktop.folks.gschema.xml
%{_bindir}/folks-import
%{_bindir}/folks-inspect

%files devel
%{_includedir}/folks
%{_libdir}/*.so
%{_libdir}/pkgconfig/folks*.pc
%{_datadir}/gir-1.0/Folk*.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/folks*


%changelog
* Fri Dec 21 2019 Senlin Xia <xiasenlin1@huawei.com> - 1:0.11.4-9
- Package init
