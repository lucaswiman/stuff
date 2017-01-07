# Setup

```
brew upgrade graphviz
rm -rf .venv
virtualenv -p `which python3.5` .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```
$ brew list --versions | grep graphviz
graphviz 2.40.1

$ dot -V
dot - graphviz version 2.40.1 (20161225.0304)

$ python --version
Python 3.5.1

$ pip freeze
pygraphviz==1.3.1
wheel==0.26.0
```


# Now verify it does work on older version

```
brew uninstall graphviz
cd /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core

git checkout a5307ebabb4d969ae851737ef19a77425565441e Formula/graphviz.rb
brew install graphviz  # graphviz-2.38.0_1.el_capitan works
```