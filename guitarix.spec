%define name            guitarix
%define version         0.10.0
%define release         %mkrel 1

%define ladspadir       %{_libdir}/ladspa

Name:           %{name}
Summary:        Guitar effect processor for JACK
Version:        %{version} 
Release:        %{release}

Source:         http://prdownloads.sourceforge.net/guitarix/%{name}-%{version}.tar.bz2
URL:            http://guitarix.sourceforge.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        GPLv2
Group:          Sound
BuildRequires:  sigc++2.0-devel fftw3-devel ladspa-devel
BuildRequires:  gtk+2-devel
BuildRequires:  sndfile-devel jackit-devel
BuildRequires:  libzita-convolver-devel
BuildRequires:  faust 
Requires:       ladspa

%description
guitarix is a simple Linux Rock Guitar Amplifier for the Jack Audio 
Connektion Kit with one input and two outputs. Designed to get nice 
thrash/metal/rock/blues guitar sounds. There are controls for bass, 
middle, treble, gain (in/out), compressor, preamp, tube's, drive, 
overdrive, oversample, anti-aliase, fuzz, balance, distortion, freeverb,
impulse response, vibrato, chorus, delay , crybaby(wah) and echo.

%prep 
%setup -q

%build
./waf configure --prefix=%{_prefix} --ladspadir=%ladspadir --faust
./waf build

%install
rm -rf %{buildroot}
./waf install --destdir=%{buildroot}
desktop-file-install --add-category="X-MandrivaLinux-Multimedia-Sound;" \
                     --remove-category="X-Jack;" \
                     --remove-category="Midi;" \
                     --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/guitarix
%{_datadir}/pixmaps/*.png
%{_datadir}/%{name}/skins/*.jpg
%{_datadir}/%{name}/skins/*.rc
%{_datadir}/%{name}/builder/*.glade
%{_datadir}/applications/%{name}.desktop
%ladspadir/*.so
%{_datadir}/ladspa/rdf/*.rdf
