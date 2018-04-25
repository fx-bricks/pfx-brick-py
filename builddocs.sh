#!/bin/sh
rm -f ./target/docs/.doctrees/*
sphinx-build -b html doc target/docs
