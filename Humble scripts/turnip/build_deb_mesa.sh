#!/bin/bash

# Preparing
. /etc/os-release; echo "${UBUNTU_CODENAME}"

echo "
deb http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME} main restricted universe multiverse
deb-src http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME} main restricted universe multiverse

deb http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME}-updates main restricted universe multiverse
deb-src http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME}-updates main restricted universe multiverse

deb http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME}-backports main restricted universe multiverse
deb-src http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME}-backports main restricted universe multiverse

deb http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME}-security main restricted universe multiverse
deb-src http://ports.ubuntu.com/ubuntu-ports ${UBUNTU_CODENAME}-security main restricted universe multiverse
" > /etc/apt/sources.list

#dpkg --add-architecture armhf
apt update
apt upgrade
apt build-dep mesa 
#apt install meson
apt install python3-pip
python3 -m pip install --upgrade pip
python3 -m pip install meson
apt install make cmake git wget vulkan-tools mesa-utils g++-arm-linux-gnueabihf g++-aarch64-linux-gnu
#apt install zlib1g-dev:armhf libexpat1-dev:armhf libdrm-dev:armhf libx11-dev:armhf libx11-xcb-dev:armhf libxext-dev:armhf libxdamage-dev:armhf libxcb-glx0-dev:armhf libxcb-dri2-0-dev:armhf libxcb-dri3-dev:armhf libxcb-shm0-dev:armhf libxcb-present-dev:armhf libxshmfence-dev:armhf libxxf86vm-dev:armhf libxrandr-dev:armhf libwayland-dev:armhf wayland-protocols:armhf libwayland-egl-backend-dev:armhf 
apt install zlib1g-dev:arm64 libexpat1-dev:arm64 libdrm-dev:arm64 libx11-dev:arm64 libx11-xcb-dev:arm64 libxext-dev:arm64 libxdamage-dev:arm64 libxcb-glx0-dev:arm64 libxcb-dri2-0-dev:arm64 libxcb-dri3-dev:arm64 libxcb-shm0-dev:arm64 libxcb-present-dev:arm64 libxshmfence-dev:arm64 libxxf86vm-dev:arm64 libxrandr-dev:arm64 libwayland-dev:arm64 wayland-protocols:arm64 libwayland-egl-backend-dev:arm64  
cp /usr/include/libdrm/drm.h /usr/include/libdrm/drm_mode.h /usr/include/

# Download mesa
BUILD_PREFIX=~/Desktop
MESA_PREFIX=${BUILD_PREFIX}/mesa-main

wget --continue --directory-prefix ${BUILD_PREFIX} https://gitlab.freedesktop.org/mesa/mesa/-/archive/main/mesa-main.tar.gz
tar -xf ${BUILD_PREFIX}/*.tar.gz --directory ${BUILD_PREFIX}

# Set env var

MESA_VER=$(cat ${MESA_PREFIX}/VERSION)
DATE=$(date +"%F" | sed 's/-//g')

MESA_64=${BUILD_PREFIX}/mesa-vulkan-kgsl_${MESA_VER}-${DATE}-${UBUNTU_CODENAME}_arm64
#MESA_32=${BUILD_PREFIX}/mesa-vulkan-kgsl_${MESA_VER}-${DATE}-${UBUNTU_CODENAME}_armhf

# Cross compile

echo "\
[binaries]
c = 'aarch64-linux-gnu-gcc'
cpp = 'aarch64-linux-gnu-g++'
ar = 'aarch64-linux-gnu-ar'
strip = 'aarch64-linux-gnu-strip'
pkgconfig = 'aarch64-linux-gnu-pkg-config'

[host_machine]
system = 'linux'
cpu_family = 'arm'
cpu = 'armv8'
endian = 'little'
" > ${MESA_PREFIX}/arm.txt

# Build mesa 
cd ${MESA_PREFIX}

#meson build --prefix $PREFIX -Dlibdir=$PREFIX/lib -D platforms=x11 -Dgallium-drivers=freedreno -Dfreedreno-kmds=kgsl,msm -D vulkan-drivers= -D dri3=enabled -D egl=enabled -D gles2=disabled -D glvnd=disabled -D glx=dri -D libunwind=disabled -D shared-glapi=enabled -Dshared-llvm=disabled -D microsoft-clc=disabled -D valgrind=disabled -D gles1=disabled

#meson build64/ --prefix /usr --libdir lib/aarch64-linux-gnu/ -D platforms=x11 -D gallium-drivers= -D vulkan-drivers=freedreno -D freedreno-kmds=kgsl -D buildtype=release -D glx=disabled -D egl=disabled -D gles1=disabled -D gles2=disabled -D gallium-xa=disabled -D opengl=false -D shared-glapi=disabled -D b_lto=true -D b_ndebug=true
meson build64/ --prefix /usr --libdir lib/aarch64-linux-gnu/ -D platforms=x11 -D gallium-drivers=freedreno -D vulkan-drivers=freedreno -D freedreno-kmds=kgsl,msm -D buildtype=release -D dri3=enabled -D glx=dri -D egl=enabled -D gles1=enabled -D gles2=enabled -D gallium-xa=enabled -D opengl=enabled -D shared-glapi=enabled -D b_lto=true -D b_ndebug=true -D glvnd=enabled -D libunwind=enabled -Dshared-llvm=disabled -D microsoft-clc=disabled -D valgrind=disabled
meson compile -C build64/
meson install -C build64/ --destdir ${MESA_64}

#meson build32/ --cross-file arm.txt --prefix /usr --libdir lib/arm-linux-gnueabihf/ -D platforms=x11 -D gallium-drivers= -D vulkan-drivers=freedreno -D freedreno-kmds=kgsl -D buildtype=release -D glx=disabled -D egl=disabled -D gles1=disabled -D gles2=disabled -D gallium-xa=disabled -D opengl=false -D shared-glapi=disabled -D b_lto=true -D b_ndebug=true
#meson compile -C build32/
#meson install -C build32/ --destdir ${MESA_32}

# Build deb64
cd ${BUILD_PREFIX}

apt remove -y mesa-vulkan-drivers:arm64
apt download mesa-vulkan-drivers:arm64
dpkg-deb -e mesa-vulkan-drivers_*_arm64.deb ${MESA_64}/DEBIAN/
sed -ie "3s/.*/Version: ${MESA_VER}-${DATE}/g" ${MESA_64}/DEBIAN/control
#rm mesa-vulkan-drivers_*_arm64.deb
rm ${MESA_64}/DEBIAN/md5sums ${MESA_64}/DEBIAN/triggers
rm -rf ${MESA_64}/usr/share/drirc.d
dpkg-deb --build --root-owner-group ${MESA_64}

# Build deb32
#cd ${BUILD_PREFIX}

#apt remove -y mesa-vulkan-drivers:armhf
#apt download mesa-vulkan-drivers:armhf
#dpkg-deb -e mesa-vulkan-drivers_*_armhf.deb ${MESA_32}/DEBIAN/
#sed -ie "3s/.*/Version: ${MESA_VER}-${DATE}/g" ${MESA_32}/DEBIAN/control
#rm mesa-vulkan-drivers_*_armhf.deb
#rm ${MESA_32}/DEBIAN/md5sums ${MESA_32}/DEBIAN/triggers
#rm -rf ${MESA_32}/usr/share/drirc.d
#dpkg-deb --build --root-owner-group ${MESA_32}


dpkg -i mesa-vulkan-kgsl_*_arm64.deb
