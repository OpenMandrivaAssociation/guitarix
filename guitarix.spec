# guitarix has merged with gx_head branch and tarball is distributed as guitarix2
# project name remains guitarix however
%global altname gx_head
%global altname2 guitarix2

Name:           guitarix
Version:        0.17.0
Release:        %mkrel 1
Summary:        Mono amplifier to JACK
Group:          Sound
License:        GPLv2+
URL:            http://guitarix.sourceforge.net/
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{altname2}-%{version}.tar.bz2
# remove O3 compile option and fix build of ladspa plugins (included upstream)
Patch0:         guitarix-fix-ladspa-O3.patch
# Correct FSF address - included upstream
Patch1:         guitarix-fsf-address.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  faust
BuildRequires:  fftw-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtkmm2.4-devel
BuildRequires:  libjack-devel
BuildRequires:  ladspa-devel
BuildRequires:  sigc++2.0-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libzita-convolver-devel
BuildRequires:  libzita-resampler-devel
BuildRequires:  gettext-devel
BuildRequires:  intltool

Requires:       jack_capture
Requires:       libjconv
Requires:       jackit
Requires:       ladspa-%{name}-plugins = %{version}-%{release}
Requires:       qjackctl
Requires:       vorbis-tools
Provides:       gx_head = %{version}-%{release}
Obsoletes:      gx_head < 0.14.0-4

%description
Guitarix is a simple mono amplifier to be used in a 'JACKified' environment,
i.e. a system using the JACK Audio Connection Kit, a professionally-capable
audio/MIDI server and master transport control.

Guitarix provides one JACK input port and two JACK output ports. It is designed
to produce nice trash/metal/rock/blues guitar sounds. Controls for bass, treble,
gain, compressor, preamp, balance, distortion, freeverb, crybaby (wah) and echo
are available. A fixed resonator is used when distortion is disabled. To modify
the sound 'pressure', you can use the feedback and feedforward sliders.

Guitarix includes an experimental tuner and a JACK MIDI output port with 3
channels. They are fed by a mix from a pitch tracker and a beat detector. You
can pitch the octave (2 octaves up or down), choose the MIDI channel, the MIDI
program, the velocity and the sensitivity, which translates into how fast the
note will read after the beat detector emits a signal. Values for the beat
detector can be set for all channels.

%package -n ladspa-%{name}-plugins
Summary:        Collection of Ladspa plug-ins
Group:          Sound
# ladspa/distortion.cpp and ladspa/guitarix-ladspa.cpp are BSD
# The rest of ladspa/* is GPLv+
License:        GPL+ and BSD
Requires:       ladspa

%description -n ladspa-%{name}-plugins
This package contains the crybaby, distortion, echo, impulseresponse, monoamp,
and monocompressor ladspa plug-ins that come together with guitarix, but can
also be used by any other ladspa host.

%prep
%setup -q -n %{altname2}-%{version}
%patch0 -p1 
%patch1 -p1

# The build system does not use these bundled libraries by default. But
# just to make sure:
rm -fr src/zita-convolver src/zita-resampler

%build
./waf -vv configure --prefix=%{_prefix}                                      \
      --cxxflags="-std=c++0x -fomit-frame-pointer -ftree-loop-linear         \
      -ffinite-math-only -fno-math-errno -fno-signed-zeros -fstrength-reduce \
%ifarch %ix86 x86_64
      -msse                                                                  \
%endif
      %{optflags}"                                                           \
      --ladspadir=%{_libdir}/ladspa
./waf -vv build %{?_smp_mflags}

%install
rm -rf %{buildroot}
./waf -vv install --destdir="%{buildroot}"

desktop-file-install                                    \
--add-category="X-DigitalProcessing"                    \
--dir=%{buildroot}%{_datadir}/applications              \
%{buildroot}/%{_datadir}/applications/%{name}.desktop

chmod 644 %{buildroot}/%{_datadir}/%{altname}/sounds/*
chmod 644 %{buildroot}/%{_datadir}/%{altname}/skins/*

%find_lang %{name}

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc changelog COPYING README
%{_bindir}/%{name}
%{_datadir}/%{altname}/
%{_datadir}/ladspa/rdf/%{name}.rdf
%{_datadir}/pixmaps/*
%{_datadir}/applications/%{name}.desktop

%files -n ladspa-%{name}-plugins
%defattr(-,root,root,-)
%{_libdir}/ladspa/*.so
