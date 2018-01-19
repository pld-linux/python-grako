#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_with	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		grako
%define		egg_name	grako
%define		pypi_name	grako
Summary:	Python grammar compiler, EBNF input, PEG/Packrat parser output
Name:		python-%{pypi_name}
Version:	3.18.1
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	bef4c0b4013a452507b0121c31b46b03
URL:		https://pypi.python.org/pypi/grako
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Grako (for "grammar compiler") takes a grammar in a variation of EBNF
as input, and outputs a memoizing PEG/Packrat parser in Python.

%package -n python3-%{pypi_name}
Summary:	%{summary}
Group:		Libraries/Python
#Requires:	python3-pygraphviz

%description -n python3-%{pypi_name}
Grako (for "grammar compiler") takes a grammar in a variation of EBNF
as input, and outputs a memoizing PEG/Packrat parser in Python.

%prep
%setup -q -n %{pypi_name}-%{version}

# Edit Makefiles to invoke python3 explicitly, rather than just python.
# This ensures that we run the tests using the python3 interpreter.
#find . -name Makefile -exec sed -i 's/python[ \t]/python3 /g' {} +

# Fix Python shebang lines
#find -type f -exec sed -i '1s=^#!%{_prefix}\(/env\|/bin\)* python[23]\?=#!%{__python}3=' {} +

# Don't package examples/antlr2grako/.ropeproject
rm -r examples/antlr2grako/.ropeproject

%build
%py3_build

%if %{with tests}
# make directory needed for bootstrap test
install -d tmp
%{__make} test
%endif

# Examples are packaged as documentation, not intended to run in place
# from the doc dir, so they should not be prebuilt. After check, clean
# and remove bytecode.
for e in antlr2grako calc regex; do
	cd examples/$e
	%{__make} clean
	rm -rf __pycache__ */__pycache__
	cd -
done

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/%{module}/test

# install loses the executable permission on bootstrap.py, so fix
#chmod a+x $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{pypi_name}/bootstrap.py

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc DESCRIPTION.rst README.md LICENSE.txt examples
%attr(755,root,root) %{_bindir}/grako
%dir %{py3_sitedir}/%{module}
%dir %{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/codegen
%dir %{py3_sitedir}/%{module}/codegen/__pycache__
%{py3_sitedir}/%{module}/__pycache__/*.pyc
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/codegen/*.py
%{py3_sitedir}/%{module}/codegen/__pycache__/*.pyc
%attr(755,root,root) %{py3_sitedir}/%{module}/*.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/%{module}/codegen/*.cpython-*.so
%{py3_sitedir}/%{egg_name}-%{version}-py*.egg-info
