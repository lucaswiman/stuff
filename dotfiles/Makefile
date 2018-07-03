SHELL := /bin/bash

.PHONY: default
default: ~/.gitconfig ~/.gitignore_global

~/.gitconfig: git/.gitconfig
	rm -f ~/.gitconfig
	ln git/.gitconfig ~/.gitconfig

~/.gitignore_global: git/.gitignore_global
	rm -f ~/.gitignore_global
	ln git/.gitignore_global ~/.gitignore_global
