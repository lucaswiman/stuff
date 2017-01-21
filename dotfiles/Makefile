SHELL := /bin/bash

.PHONY: default
default: ~/.gitconfig

~/.gitconfig: git/.gitconfig
	rm -f ~/.gitconfig
	ln git/.gitconfig ~/.gitconfig
