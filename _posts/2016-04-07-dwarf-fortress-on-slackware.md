---
layout: post
title: 'Dwarf Fortress on Slackware 14.1'
---

This post will explain how to run Dwarf Fortress on 64 bit Slackware 14.1.

Enable multilib by following the instructions [here][instrs].

The default multilib installation doesn’t include OpenAL, so we’ll need to compile that for 32 bit separately.

```
wget http://www.slackware.com/~alien/slackbuilds/OpenAL/pkg/14.1/OpenAL-1.17.1-i486-1alien.tgz
convertpkg-compat32 -i OpenAL-1.17.1-i486-1alien.tgz
upgradepkg --install-new /tmp/OpenAL-compat32-1.17.1-i486-1aliencompat32.txz
```

Download and run the Linux version of [Dwarf Fortress][df].

```
tar xvf df_*_linux.tar.bz2
cd df_linux
./df
```

Thanks to [AlienBOB][ab] for providing these resources.

[instrs]: http://alien.slackbook.org/dokuwiki/doku.php?id=slackware:multilib
[df]: http://www.bay12games.com/dwarves/
[ab]: http://www.slackware.com/~alien/
