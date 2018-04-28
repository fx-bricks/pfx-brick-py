#!/bin/sh
rm -f ./target/docs/.doctrees/*
sphinx-build -b html doc target/docs
# replace the rtd theme css with an "orange" flavoured version
cp target/docs/_static/css/theme.css target/docs/_static/css/oldtheme.css
cp doc/theme_orange.css target/docs/_static/css/theme.css
