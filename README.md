from scratch:

```
$ curl -fsSL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-installer | bash
$ export PATH="$HOME/.rbenv/bin:$PATH"
$ eval "$(rbenv init -)"
$ rbenv install
$ gem install bundler
$ bundle install
```

serve:

```
$ bundle exec jekyll serve
```
