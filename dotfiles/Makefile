SHELL := /bin/bash

.PHONY: default
default: ~/.gitconfig ~/.ondirrc ~/.gitignore_global

~/.gitconfig: git/.gitconfig
	rm -f ~/.gitconfig
	ln git/.gitconfig ~/.gitconfig

~/.gitignore_global: git/.gitignore_global
	rm -f ~/.gitignore_global
	ln git/.gitignore_global ~/.gitignore_global

~/.ondirrc: .ondirrc  # https://makandracards.com/makandra/19549-how-to-set-git-user-and-email-per-directory
	rm -f ~/.ondirrc
	ln .ondirrc ~/.ondirrc
