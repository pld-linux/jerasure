#
# Conditional build:
%bcond_without	static_libs	# static libraries
#

%define		gitref	505ccb4b

Summary:	A Library in C Facilitating Erasure Coding for Storage
Name:		jerasure
Version:	2.0
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	https://git.sr.ht/~thestr4ng3r/jerasure/archive/%{gitref}.tar.gz#/%{name}-%{version}.tar.gz
# Source0-md5:	1070a05a2d2bc20b9e518eecaff7012a
Patch0:		opt.patch
URL:		https://web.eecs.utk.edu/~jplank/plank/www/software.html
BuildRequires:	gf-complete-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Library in C Facilitating Erasure Coding for Storage.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -n %{name}-%{gitref}
%patch -P 0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%ifarch %{ix86}
	--disable-sse \
%endif
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc License.txt README Manual.pdf
%attr(755,root,root) %{_libdir}/libJerasure.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libJerasure.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libJerasure.so
%{_libdir}/libJerasure.la
%{_includedir}/jerasure
%{_includedir}/jerasure.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libJerasure.a
%endif
