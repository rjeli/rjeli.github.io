---
layout: post
title: 'Ugly debian packaging: Just put my binary in a .deb, dammit'
---

I recently wanted to put some shared libraries and executables in `.deb` files, so end-users could just `apt install ./the-package.deb`. This task is straightforward but it's surprisingly hard to find instructions. I found Vincent Bernat's [Pragmatic Debian packaging][1] quite useful, and I recommend you go read that first. However, his methods are still too reasonable and maintainable for me. I just want to put my binary in a .deb, dammit. 

Assume we work at a company called CoolSoft. CoolSoft has a program called `sayhi` that says hi. It can be a binary, shell script, whatever.

```sh
$ ./sayhi
hi
```

We would like to install it into `/usr/local/bin`. First create a script called `make_sayhi_deb.sh`:

```sh
#!/bin/bash
set -euo pipefail

pkgname=sayhi
version=0.0.1
arch=all

tmpdir=$(mktemp -d)
pkgdir=$tmpdir/pkg
mkdir -p $pkgdir $pkgdir/DEBIAN 

# this is the part where it installs your files
install -Dm 755 sayhi $pkgdir/usr/local/bin/sayhi

cat <<EOF >$pkgdir/DEBIAN/control
Package: $pkgname
Version: $version
Architecture: $arch
Maintainer: CoolSoft (admin@coolsoft.com)
Description: It says hi
Depends:

EOF
dpkg -b $pkgdir ./${pkgname}_${version}_${arch}.deb
rm -rf $tmpdir
```

Then just run it and install the package.

```sh
$ bash make_sayhi_deb.sh
dpkg-deb: building package 'sayhi' in './sayhi_0.0.1_all.deb'.
$ sudo apt install ./sayhi_0.0.1_all.deb
...
$ sayhi
hi
```

**Architectures**: My `sayhi` is actually a shell script, so I chose `arch=all` above. If yours is a binary, set it to `amd64`, `arm64`, or another [Debian architecture][2].

**More files**: See above where it says `# this is the part where it installs your files`? Well, just keep installing your other files. 755 for executables, 644 otherwise. `-D` creates leading folders automatically.

```sh
# this is the part where it installs your files
install -Dm 755 sayhi $pkgdir/usr/local/bin/sayhi
install -Dm 644 libsayhi.so $pkgdir/usr/local/lib/libsayhi.so
```

[1]: https://vincent.bernat.ch/en/blog/2019-pragmatic-debian-packaging
[2]: https://wiki.debian.org/SupportedArchitectures
